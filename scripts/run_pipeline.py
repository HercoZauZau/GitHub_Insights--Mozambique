#!/usr/bin/env python3
"""Actualização mensal dos 6 notebooks, em 3 grupos de 2.

A dependência entre notebooks é respeitada dentro de cada grupo:
  grupo 1: 01 -> 02 (sequencial)
  grupo 2: 03 || 04 (paralelo, kernels separados)
  grupo 3: 05 -> 06 (sequencial)

Intervalos de 90 minutos APENAS após um grupo completo bem-sucedido, antes
 do grupo seguinte. Cada notebook admite até 3 tentativas com 5 minutos
 de intervalo em caso de erro. Todos os ficheiros são produzidos numa
 área temporária; só ficam em data/YYYY_MM/ após sucesso de todos os 6.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import os
import re
import shutil
import sys
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import nbformat
from nbclient import NotebookClient
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TZ = ZoneInfo('Africa/Maputo')
DEFAULT_BATCH_DELAY = 90 * 60
DEFAULT_RETRY_DELAY = 5 * 60

NOTEBOOK_NAMES = (
    '01_get_users_ids.ipynb',
    '02_get_users_data.ipynb',
    '03_get_repos_data.ipynb',
    '04_get_starred_data.ipynb',
    '05_get_issues_data.ipynb',
    '06_get_insights.ipynb',
)
NOTEBOOK_DEPENDENCIES = {
    NOTEBOOK_NAMES[0]: set(),
    NOTEBOOK_NAMES[1]: {NOTEBOOK_NAMES[0]},
    NOTEBOOK_NAMES[2]: {NOTEBOOK_NAMES[1]},
    NOTEBOOK_NAMES[3]: {NOTEBOOK_NAMES[1]},
    NOTEBOOK_NAMES[4]: {NOTEBOOK_NAMES[2]},
    NOTEBOOK_NAMES[5]: {NOTEBOOK_NAMES[1], NOTEBOOK_NAMES[2], NOTEBOOK_NAMES[3], NOTEBOOK_NAMES[4]},
}

EXPECTED_CSV = {
    '01_get_users_ids.ipynb': [('users_ids.csv', {'user_id'}, True)],
    '02_get_users_data.ipynb': [('users_data.csv', {'id', 'login'}, True)],
    '03_get_repos_data.ipynb': [('repos_data.csv', {'id', 'owner_id'}, True)],
    '04_get_starred_data.ipynb': [
        ('starred_repos_data.csv', {'id'}, True),
        ('starred_repos_users_ids.csv', {'user_id', 'repo_id'}, True),
    ],
    '05_get_issues_data.ipynb': [('issues_data.csv', {'id', 'repo_id'}, False)],
}


def validate_month(month: str) -> str:
    if not re.fullmatch(r'\d{4}_(0[1-9]|1[0-2])', month):
        raise ValueError('Mês inválido. Usa o formato AAAA_MM, exemplo: 2026_11.')
    return month


def previous_month(reference: datetime) -> str:
    """Devolve AAAA_MM do mês anterior à data da execução em Maputo.

    Ex.: 2026-11-01 -> 2026_10; 2027-01-01 -> 2026_12.
    """
    first_day = reference.astimezone(DEFAULT_TZ).date().replace(day=1)
    last_day_previous_month = first_day - timedelta(days=1)
    return last_day_previous_month.strftime('%Y_%m')


def read_order(notebooks_dir: Path) -> list[str]:
    order_path = notebooks_dir / 'ORDER.txt'
    names = [line.strip() for line in order_path.read_text(encoding='utf-8').splitlines()
             if line.strip() and not line.lstrip().startswith('#')]
    if tuple(names) != NOTEBOOK_NAMES:
        raise ValueError('ORDER.txt deve conter os seis notebooks na ordem 01 a 06; '
                         'o plano de dependências foi definido para esta sequência.')
    for name in names:
        if not (notebooks_dir / name).is_file():
            raise FileNotFoundError(f'Notebook não encontrado: {name}')
    return names


def get_groups(names: list[str]) -> list[tuple[str, str]]:
    if tuple(names) != NOTEBOOK_NAMES:
        raise ValueError('Para esta versão são necessários exactamente os seis notebooks originais.')
    return [(names[i], names[i + 1]) for i in range(0, 6, 2)]


def validate_csv(path: Path, columns: set[str], must_have_rows: bool) -> None:
    if not path.is_file():
        raise FileNotFoundError(f'Ficheiro não criado: {path.name}')
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        missing = columns - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f'{path.name}: faltam colunas {sorted(missing)}')
        if must_have_rows and next(reader, None) is None:
            raise ValueError(f'{path.name}: ficheiro sem registos.')


def execute_notebook_once(name: str, work_notebooks: Path, completed_dir: Path,
                          cell_timeout: int) -> None:
    """Kernel independente por notebook; seguro para execução concorrente."""
    notebook = nbformat.read(work_notebooks / name, as_version=4)
    client = NotebookClient(
        notebook,
        timeout=cell_timeout,
        kernel_name='python3',
        resources={'metadata': {'path': str(work_notebooks)}},
        allow_errors=False,
    )
    # Executar as células sem gravar outra cópia do notebook (nem em data/, nem temporariamente).
    # Apenas os CSVs exportados pelas células serão preservados.
    client.execute()


def run_with_retries(name: str, work_notebooks: Path, stage: Path, completed_dir: Path,
                     *, max_attempts: int, retry_delay: int, cell_timeout: int) -> int:
    for attempt in range(1, max_attempts + 1):
        # Evitar dar por válido um CSV incompleto deixado por uma tentativa anterior.
        for csv_name, _, _ in EXPECTED_CSV.get(name, []):
            (stage / csv_name).unlink(missing_ok=True)
        (completed_dir / name).unlink(missing_ok=True)

        print(f'[NOTEBOOK] {name} | tentativa {attempt}/{max_attempts}', flush=True)
        try:
            execute_notebook_once(name, work_notebooks, completed_dir, cell_timeout)
            for csv_name, cols, has_rows in EXPECTED_CSV.get(name, []):
                validate_csv(stage / csv_name, cols, has_rows)
            print(f'[OK] {name} | tentativas necessárias: {attempt}', flush=True)
            return attempt
        except Exception as err:
            print(f'[FALHA] {name} | {type(err).__name__}: {err}', file=sys.stderr, flush=True)
            if attempt < max_attempts:
                print(f'[RECUPERAÇÃO] {name}: nova tentativa em {retry_delay // 60} min '
                      f'({retry_delay} s)', flush=True)
                time.sleep(retry_delay)
            else:
                raise RuntimeError(f'{name}: falhou após {max_attempts} tentativas.') from err
    raise AssertionError('Inacessível')


def run_group(group: tuple[str, str], group_number: int, work_notebooks: Path,
              stage: Path, completed_dir: Path, *, max_attempts: int,
              retry_delay: int, cell_timeout: int) -> dict[str, int]:
    first, second = group
    if first in NOTEBOOK_DEPENDENCIES[second]:
        print(f'[GRUPO {group_number}] Execução sequencial: {first} -> {second} '
              '(dependência de dados)', flush=True)
        results = {}
        for name in group:
            results[name] = run_with_retries(
                name, work_notebooks, stage, completed_dir,
                max_attempts=max_attempts, retry_delay=retry_delay, cell_timeout=cell_timeout)
        return results

    if second in NOTEBOOK_DEPENDENCIES[first]:
        raise ValueError(f'Dependência inversa dentro do grupo {group_number}.')

    print(f'[GRUPO {group_number}] Execução paralela: {first} || {second}', flush=True)
    results = {}
    failures = {}
    # Ambos começam, cada qual com um kernel; aguarda a conclusão dos DOIS.
    with ThreadPoolExecutor(max_workers=2, thread_name_prefix='notebook') as pool:
        futures = {
            pool.submit(run_with_retries, name, work_notebooks, stage, completed_dir,
                        max_attempts=max_attempts, retry_delay=retry_delay,
                        cell_timeout=cell_timeout): name
            for name in group
        }
        for future in as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as exc:
                failures[name] = exc
    if failures:
        failed_names = ', '.join(failures)
        raise RuntimeError(f'Grupo {group_number} falhou: {failed_names}.') from next(iter(failures.values()))
    return results


def wait_between_groups(seconds: int, after_group: int) -> None:
    """Espera em blocos para manter registo de progresso no GitHub Actions."""
    print(f'[PAUSA] Grupo {after_group} concluído. Aguardar {seconds // 60} '
          'minutos antes do próximo grupo.', flush=True)
    remaining = seconds
    while remaining > 0:
        chunk = min(300, remaining)
        time.sleep(chunk)
        remaining -= chunk
        print(f'[PAUSA] Restam {remaining // 60} min e {remaining % 60} s.', flush=True)


def execute_pipeline(root: Path, month: str, *, force: bool = False,
                     max_attempts: int = 3, retry_delay: int = DEFAULT_RETRY_DELAY,
                     batch_delay: int = DEFAULT_BATCH_DELAY,
                     cell_timeout: int = 3600) -> bool:
    """Publica de forma atómica em data/AAAA_MM só quando TODOS terminarem.

    Devolve False se todos os CSVs já existirem e --force não for usado.
    """
    validate_month(month)
    if not os.getenv('API_TOKEN'):
        raise ValueError('API_TOKEN não definido. Usa .env local ou GitHub Actions Secrets.')
    if max_attempts < 1 or retry_delay < 0 or batch_delay < 0 or cell_timeout < 1:
        raise ValueError('Tentativas >= 1, intervalos >= 0 e timeout > 0.')

    source_dir = root / 'notebooks'
    names = read_order(source_dir)
    groups = get_groups(names)
    data_root = root / 'data'
    data_root.mkdir(exist_ok=True)
    destination = data_root / month
    if destination.exists() and not force:
        # Como já não publicamos _SUCCESS.json, verificamos os ficheiros esperados.
        # A publicação é atómica: a pasta final só é substituída após sucesso dos 6.
        try:
            for specs in EXPECTED_CSV.values():
                for csv_name, columns, required_rows in specs:
                    validate_csv(destination / csv_name, columns, required_rows)
        except (FileNotFoundError, ValueError) as exc:
            raise RuntimeError(
                f'{destination} já existe mas os CSVs estão incompletos: {exc}. '
                'Para recuperar o mês, executa com --force.'
            ) from exc
        print(f'[SKIP] {month} já contém todos os CSVs esperados. '
              'Para repetir, usa --force.', flush=True)
        return False

    attempts_per_notebook = {}
    with tempfile.TemporaryDirectory(prefix='gh-insights-') as temp_name:
        work_root = Path(temp_name)
        work_notebooks = work_root / 'notebooks'
        work_notebooks.mkdir()
        stage = work_root / 'data' / month
        stage.mkdir(parents=True)
        completed_dir = work_root / 'notebooks_executados'
        completed_dir.mkdir()
        for name in names:
            shutil.copy2(source_dir / name, work_notebooks / name)

        prior_dir = os.environ.get('DIR_NAME')
        os.environ['DIR_NAME'] = month
        try:
            for group_number, group in enumerate(groups, 1):
                attempts_per_notebook.update(run_group(
                    group, group_number, work_notebooks, stage, completed_dir,
                    max_attempts=max_attempts, retry_delay=retry_delay,
                    cell_timeout=cell_timeout))
                print(f'[GRUPO {group_number}] Ambos concluídos com sucesso.', flush=True)
                if group_number < len(groups) and batch_delay:
                    wait_between_groups(batch_delay, group_number)
        finally:
            if prior_dir is None:
                os.environ.pop('DIR_NAME', None)
            else:
                os.environ['DIR_NAME'] = prior_dir

        # Não gerar _SUCCESS.json: data/ terá apenas os CSVs exportados.
        # Os CSVs já foram validados em cada notebook antes de chegar aqui.

        with tempfile.TemporaryDirectory(prefix='.backup-', dir=data_root) as backup_tmp:
            backup = Path(backup_tmp) / 'previous'
            had_old = destination.exists()
            if had_old:
                shutil.move(str(destination), str(backup))
            try:
                shutil.move(str(stage), str(destination))
            except Exception:
                if had_old and backup.exists() and not destination.exists():
                    shutil.move(str(backup), str(destination))
                raise
    print(f'[SUCESSO] Dados publicados em data/{month}/', flush=True)
    return True


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description='Recolha mensal GitHub Insights em 3 grupos de 2.')
    parser.add_argument('--month', help='Mês AAAA_MM; omissão = mês anterior à execução em Maputo.')
    parser.add_argument('--scheduled', action='store_true', help='Executar apenas no dia 1 em Maputo.')
    parser.add_argument('--force', action='store_true', help='Substituir mês já publicado.')
    parser.add_argument('--dry-run', action='store_true', help='Mostrar plano sem executar a API.')
    parser.add_argument('--max-attempts', type=int, default=3)
    parser.add_argument('--retry-delay', type=int, default=DEFAULT_RETRY_DELAY,
                        help='Intervalo entre tentativas de um notebook, em segundos (300).')
    parser.add_argument('--batch-delay', type=int, default=DEFAULT_BATCH_DELAY,
                        help='Pausa entre grupos concluídos, em segundos (5400).')
    parser.add_argument('--cell-timeout', type=int, default=3600,
                        help='Timeout por célula, em segundos (3600).')
    args = parser.parse_args(argv)

    now = datetime.now(DEFAULT_TZ)
    if args.scheduled and args.month:
        parser.error('--scheduled não pode ser usado com --month')
    if args.scheduled and now.day != 1:
        print(f'[SKIP] Hoje é dia {now.day} em Maputo. Agendamento reservado ao dia 1.')
        return 0
    month = validate_month(args.month or previous_month(now))
    if args.dry_run:
        names = read_order(PROJECT_ROOT / 'notebooks')
        print('Mês:', month)
        for i, pair in enumerate(get_groups(names), 1):
            print(f'Grupo {i} ({"paralelo" if i == 2 else "sequencial"}):', ', '.join(pair))
            if i < 3:
                print(f'  Pausa após sucesso: {args.batch_delay // 60} minutos')
        print(f'Tentativas por notebook: {args.max_attempts}; '
              f'intervalo: {args.retry_delay // 60} minutos')
        return 0

    load_dotenv(PROJECT_ROOT / '.env')
    execute_pipeline(PROJECT_ROOT, month, force=args.force,
                     max_attempts=args.max_attempts, retry_delay=args.retry_delay,
                     batch_delay=args.batch_delay, cell_timeout=args.cell_timeout)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:
        print(f'PIPELINE FALHOU: {exc}', file=sys.stderr, flush=True)
        sys.exit(1)
