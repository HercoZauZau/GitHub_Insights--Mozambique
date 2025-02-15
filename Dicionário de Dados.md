# 📄 Dicionário de Dados

**Nota:** Os dados colhidos antes de 2025 apresentam uma estrutura diferente das tabelas abaixo. 

---

## 1. Tabela: Users Data

Esta tabela armazena informações de perfis de usuários (perfis do GitHub).

- **login**: Nome de usuário único (string).
- **id**: Identificador único do usuário (integer).
- **name**: Nome completo do usuário (string).
- **company**: Empresa ou organização associada ao usuário (string).
- **blog**: URL do blog ou site pessoal (string).
- **location**: Localização geográfica (string).
- **email**: Endereço de e-mail (string).
- **bio**: Biografia ou descrição do usuário (string).
- **twitter_username**: Nome de usuário no Twitter (string).
- **public_repos**: Número de repositórios públicos (integer).
- **public_gists**: Número de gists públicos (integer).
- **followers**: Quantidade de seguidores (integer).
- **following**: Quantidade de usuários que o perfil segue (integer).
- **created_at**: Data de criação do perfil (timestamp/datetime).
- **updated_at**: Data da última atualização do perfil (timestamp/datetime).

---

## 2. Tabela: Repos Data

Tabela contendo informações sobre repositórios.

- **id**: Identificador único do repositório (integer).
- **name**: Nome do repositório (string).
- **full_name**: Nome completo do repositório, geralmente no formato `owner/name` (string).
- **owner_id**: Identificador do dono do repositório (integer).
- **html_url**: URL para acesso ao repositório via navegador (string).
- **description**: Descrição do repositório (string).
- **fork**: Indica se o repositório é um fork (boolean).
- **created_at**: Data de criação do repositório (timestamp/datetime).
- **updated_at**: Data da última atualização (timestamp/datetime).
- **pushed_at**: Data do último push para o repositório (timestamp/datetime).
- **homepage**: URL da homepage do projeto, se disponível (string).
- **size**: Tamanho do repositório (integer).
- **stargazers_count**: Número de estrelas (integer).
- **watchers_count**: Número de observadores (integer).
- **language**: Linguagem principal utilizada (string).
- **forks_count**: Número de forks (integer).
- **open_issues_count**: Quantidade de issues abertas (integer).
- **topics**: Lista de tópicos ou tags associadas ao repositório (string com separador).
- **default_branch**: Nome do branch padrão, geralmente `main` ou `master` (string).
- **license_key**: Código ou chave identificadora da licença (string).
- **license_name**: Nome da licença do repositório (string).

---

## 3. Tabela: Starred Data

Tabela contendo informações sobre repositórios curtidos.

- **id**: Identificador único do repositório (integer).
- **name**: Nome do repositório (string).
- **full_name**: Nome completo do repositório (string).
- **owner_id**: Identificador do dono do repositório (integer).
- **html_url**: URL para acesso ao repositório (string).
- **description**: Descrição do repositório (string).
- **fork**: Indica se o repositório é um fork (boolean).
- **created_at**: Data de criação (timestamp/datetime).
- **updated_at**: Data da última atualização (timestamp/datetime).
- **pushed_at**: Data do último push (timestamp/datetime).
- **homepage**: URL da homepage, se houver (string).
- **size**: Tamanho do repositório (integer).
- **stargazers_count**: Número de estrelas (integer).
- **watchers_count**: Número de observadores (integer).
- **language**: Linguagem principal (string).
- **forks_count**: Número de forks (integer).
- **open_issues_count**: Quantidade de issues abertas (integer).
- **license_key**: Código da licença (string).
- **license_name**: Nome da licença (string).
- **topics**: Lista de tópicos ou tags associadas.
- **default_branch**: Nome do branch padrão (string).

---

## 4. Tabela: Starred Repos - Users Ids

Tabela de mapeamento que relaciona usuários a repositórios e identifica os donos dos repositórios.

- **user_id**: Identificador do usuário (integer).
- **repo_id**: Identificador do repositório (integer).
- **owner_id**: Identificador do dono do repositório (integer).

---

## 5. Tabela: Issues Data

Tabela contendo informações sobre as issues (problemas ou solicitações) dos repositórios.

- **id**: Identificador único da issue (integer).
- **number**: Número sequencial da issue no repositório (integer).
- **title**: Título ou assunto da issue (string).
- **user_id**: Identificador do usuário que criou a issue (integer).
- **state**: Estado da issue, por exemplo, `open` ou `closed` (string).
- **comments**: Número de comentários na issue (integer).
- **created_at**: Data de criação da issue (timestamp/datetime).
- **updated_at**: Data da última atualização (timestamp/datetime).
- **closed_at**: Data em que a issue foi fechada (timestamp/datetime, pode ser nula se estiver aberta).
- **body**: Conteúdo ou descrição detalhada da issue (string).
- **reactions_total_count**: Contagem total de reações (integer).
- **repo_id**: Identificador do repositório ao qual a issue pertence (integer).

---

Este dicionário de dados serve como referência para compreensão da estrutura e do significado dos dados presentes em cada uma das tabelas. Ajustes e detalhes adicionais podem ser incluídos conforme a evolução do projeto ou a inclusão de novos campos.