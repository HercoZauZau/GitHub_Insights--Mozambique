"""Testes offline do orquestrador. Não contactam a API do GitHub."""
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import sys
import threading
from pathlib import Path

import nbformat
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import run_pipeline as p


@pytest.fixture
def example_repo(tmp_path, monkeypatch):
    nbdir = tmp_path / 'notebooks'
    nbdir.mkdir()
    (tmp_path / 'data').mkdir()
    (nbdir / 'ORDER.txt').write_text('\n'.join(p.NOTEBOOK_NAMES) + '\n', encoding='utf-8')
    for name in p.NOTEBOOK_NAMES:
        nb = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('print("exemplo")')])
        nbformat.write(nb, nbdir / name)
    monkeypatch.setenv('API_TOKEN', 'token_falso_so_para_testes')
    return tmp_path


@pytest.fixture
def fake_execution(monkeypatch):
    calls = []
    delays = []
    guard = threading.Lock()

    output_data = {
        'users_ids.csv': 'user_id\n1\n',
        'users_data.csv': 'id,login\n1,user1\n',
        'repos_data.csv': 'id,owner_id\n2,1\n',
        'starred_repos_data.csv': 'id\n2\n',
        'starred_repos_users_ids.csv': 'user_id,repo_id\n1,2\n',
        'issues_data.csv': 'id,repo_id\n',
    }

    def execute(name, work_notebooks, completed_dir, cell_timeout):
        stage = work_notebooks.parent / 'data' / '2026_11'
        with guard:
            calls.append(name)
        for csv_name, _, _ in p.EXPECTED_CSV.get(name, []):
            (stage / csv_name).write_text(output_data[csv_name], encoding='utf-8')
        (completed_dir / name).write_text('{"nbformat": 4}', encoding='utf-8')

    monkeypatch.setattr(p, 'execute_notebook_once', execute)
    monkeypatch.setattr(p.time, 'sleep', delays.append)
    return calls, delays, output_data


def test_month():
    assert p.validate_month('2026_11') == '2026_11'
    for invalid in ('2026-11', '2026_13', '../2026_11', '2026_0', 'abc'):
        with pytest.raises(ValueError):
            p.validate_month(invalid)


@pytest.mark.parametrize(('date', 'expected'), [
    ('2026-11-01', '2026_10'),
    ('2026-12-01', '2026_11'),
    ('2027-01-01', '2026_12'),
    ('2027-02-01', '2027_01'),
    ('2024-03-01', '2024_02'),
    ('2026-11-30', '2026_10'),
])
def test_previous_month_uses_maputo_calendar(date, expected):
    now = datetime.fromisoformat(date + 'T08:17:00').replace(tzinfo=ZoneInfo('Africa/Maputo'))
    assert p.previous_month(now) == expected


def test_previous_month_converts_utc_to_maputo():
    # Ainda é 31/10 em UTC, mas já é 01/11 em Maputo.
    now = datetime.fromisoformat('2026-10-31T22:30:00+00:00')
    assert p.previous_month(now) == '2026_10'


def test_manual_month_override_remains_available(monkeypatch, capsys):
    assert p.main(['--month', '2025_09', '--dry-run']) == 0
    assert 'Mês: 2025_09' in capsys.readouterr().out


def test_six_notebooks_in_three_groups(example_repo):
    names = p.read_order(example_repo / 'notebooks')
    assert len(names) == 6
    assert p.get_groups(names) == [tuple(names[0:2]), tuple(names[2:4]), tuple(names[4:6])]


def test_incorrect_order_is_rejected(example_repo):
    f = example_repo / 'notebooks' / 'ORDER.txt'
    f.write_text('\n'.join(reversed(p.NOTEBOOK_NAMES)) + '\n')
    with pytest.raises(ValueError, match='ORDER.txt'):
        p.read_order(example_repo / 'notebooks')


def test_success_with_two_pauses_and_skip(example_repo, fake_execution):
    calls, delays, _ = fake_execution
    assert p.execute_pipeline(example_repo, '2026_11', max_attempts=3,
                              retry_delay=300, batch_delay=5400)
    dest = example_repo / 'data' / '2026_11'
    metadata = json.loads((dest / '_SUCCESS.json').read_text(encoding='utf-8'))
    assert len(calls) == 6
    assert calls[:2] == list(p.NOTEBOOK_NAMES[:2])
    assert set(calls[2:4]) == set(p.NOTEBOOK_NAMES[2:4])
    assert calls[-2:] == list(p.NOTEBOOK_NAMES[4:])
    assert delays == [300] * 36  # duas pausas de 90 minutos em blocos de 5
    assert metadata['attempts_per_notebook'] == dict.fromkeys(p.NOTEBOOK_NAMES, 1)
    assert metadata['batch_delay_seconds'] == 5400
    assert metadata['groups'][1]['mode'] == 'parallel'
    assert (dest / 'notebooks_executados' / p.NOTEBOOK_NAMES[-1]).exists()
    assert not p.execute_pipeline(example_repo, '2026_11', batch_delay=5400)
    assert len(calls) == 6


def test_retry_only_failed_notebook(example_repo, fake_execution, monkeypatch):
    calls, delays, outputs = fake_execution
    target = p.NOTEBOOK_NAMES[2]
    attempts = {target: 0}
    orig = p.execute_notebook_once

    def once(name, *args):
        if name == target:
            attempts[target] += 1
            if attempts[target] == 1:
                raise ConnectionError('API indisponível por instantes')
        return orig(name, *args)

    monkeypatch.setattr(p, 'execute_notebook_once', once)
    p.execute_pipeline(example_repo, '2026_11', batch_delay=0, retry_delay=300)
    assert calls.count(target) == 1  # Falhou antes de criar dados, depois executou bem
    assert attempts[target] == 2
    assert delays == [300]
    data = json.loads((example_repo / 'data' / '2026_11' / '_SUCCESS.json').read_text())
    assert data['attempts_per_notebook'][target] == 2
    assert data['attempts_per_notebook'][p.NOTEBOOK_NAMES[3]] == 1


def test_failure_does_not_publish_or_wait_after_failure(example_repo, fake_execution, monkeypatch):
    calls, delays, _ = fake_execution
    original = p.execute_notebook_once

    def fail(name, *args):
        if name == p.NOTEBOOK_NAMES[0]:
            raise ValueError('erro persistente')
        return original(name, *args)

    monkeypatch.setattr(p, 'execute_notebook_once', fail)
    with pytest.raises(RuntimeError, match='após 3 tentativas'):
        p.execute_pipeline(example_repo, '2026_11', retry_delay=300, batch_delay=5400)
    assert delays == [300, 300]
    assert calls == []
    assert not (example_repo / 'data' / '2026_11').exists()


def test_parallel_group_waits_for_both_and_errors(example_repo, fake_execution, monkeypatch):
    calls, delays, _ = fake_execution
    original = p.execute_notebook_once
    gate = threading.Barrier(2, timeout=4)
    entered = set()
    lock = threading.Lock()

    def parallel(name, *args):
        if name in p.NOTEBOOK_NAMES[2:4]:
            with lock:
                entered.add(name)
            gate.wait()
        return original(name, *args)

    monkeypatch.setattr(p, 'execute_notebook_once', parallel)
    assert p.execute_pipeline(example_repo, '2026_11', batch_delay=0)
    assert entered == set(p.NOTEBOOK_NAMES[2:4])
    assert delays == []


def test_failed_parallel_notebook_cannot_publish(example_repo, fake_execution, monkeypatch):
    calls, delays, _ = fake_execution
    original = p.execute_notebook_once
    failed = p.NOTEBOOK_NAMES[3]

    def fail_one(name, *args):
        if name == failed:
            raise ValueError('falha permanente')
        return original(name, *args)

    monkeypatch.setattr(p, 'execute_notebook_once', fail_one)
    with pytest.raises(RuntimeError, match='Grupo 2 falhou'):
        p.execute_pipeline(example_repo, '2026_11', max_attempts=2,
                           retry_delay=300, batch_delay=5400)
    assert delays == [300] * 19  # 90 minutos da pausa inicial + uma repetição após erro
    assert not (example_repo / 'data' / '2026_11').exists()


def test_force_failed_reprocessing_preserves_previous(example_repo, fake_execution, monkeypatch):
    calls, delays, _ = fake_execution
    p.execute_pipeline(example_repo, '2026_11', batch_delay=0)
    old = (example_repo / 'data' / '2026_11' / '_SUCCESS.json').read_text()
    orig = p.execute_notebook_once

    def fail_last(name, *args):
        if name == p.NOTEBOOK_NAMES[-1]:
            raise ValueError('falha no último notebook')
        return orig(name, *args)

    monkeypatch.setattr(p, 'execute_notebook_once', fail_last)
    with pytest.raises(RuntimeError):
        p.execute_pipeline(example_repo, '2026_11', force=True, batch_delay=0,
                           max_attempts=1)
    assert (example_repo / 'data' / '2026_11' / '_SUCCESS.json').read_text() == old


def test_token_required(example_repo, monkeypatch):
    monkeypatch.delenv('API_TOKEN')
    with pytest.raises(ValueError, match='API_TOKEN'):
        p.execute_pipeline(example_repo, '2026_11')


def test_csv_validation_rejects_partial(example_repo, fake_execution, monkeypatch):
    calls, delays, data = fake_execution
    orig = p.execute_notebook_once
    target = p.NOTEBOOK_NAMES[1]

    def partial(name, work_notebooks, completed_dir, cell_timeout):
        orig(name, work_notebooks, completed_dir, cell_timeout)
        if name == target:
            path = work_notebooks.parent / 'data' / '2026_11' / 'users_data.csv'
            path.write_text('id\n1\n')  # falta a coluna login

    monkeypatch.setattr(p, 'execute_notebook_once', partial)
    with pytest.raises(RuntimeError):
        p.execute_pipeline(example_repo, '2026_11', max_attempts=2, batch_delay=5400,
                           retry_delay=300)
    assert delays == [300]
    assert not (example_repo / 'data' / '2026_11').exists()
