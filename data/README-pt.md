Esta pasta contém os dados do projeto, organizados em três subpastas: "raw", "processed" e "results". Abaixo está uma descrição detalhada de cada subpasta e dos arquivos dentro delas. 

Nota: É importante atualizar esta pasta sempre que novos resultados ou visualizações forem gerados durante o projeto.

## Subpasta "raw"

A subpasta 'raw' contém os dados brutos coletados da API do GitHub. Esses dados foram coletados inicialmente por meio de solicitações à API e são a fonte primária para a análise subsequente.

## Subpasta "processed"

A subpasta 'processed' contém os dados processados após a limpeza, transformação e agregação dos dados brutos coletados. Esses dados processados são usados para análises posteriores e para gerar resultados finais.

- `repos_data.csv`: Este arquivo contém informações sobre os repositórios criados no GitHub. Cada registro representa um repositório e inclui os seguintes campos:
   - `id`: Identificador único do repositório.
   - `owner_id`: Identificador único do proprietário do repositório.
   - `language`: Linguagem principal do repositório.
   - `created_at`: Data de criação do repositório.
   - `updated_at`: Data de atualização do repositório.
   - `stargazers_count`: Número de estrelas recebidas pelo repositório.
   - `forks_count`: Número de forks do repositório.

- `starred_data.csv`: Este arquivo contém informações sobre os repositórios curtidos pelos usuários. Cada registro representa preferências dentre todos repositórios curtidos e inclui os seguintes campos:
   - `user_id`: Identificador único do usuário.
   - `has_moz_owner`: Indicador se algum dos repositórios curtidos pertence a um proprietário de Moçambique.
   - `fav_lang`: Linguagem de programação favorita do usuário.
   - `fav_topic`: Tópico favorito do usuário.

- `user_data.csv`: Este arquivo contém informações sobre os usuários do GitHub. Cada registro representa um usuário e inclui os seguintes campos:
   - `id`: Identificador único do usuário.
   - `city_id`: Identificador único da cidade em que o usuário está localizado.
   - `followers`: Número de seguidores do usuário.
   - `following`: Número de usuários que o usuário segue.
   - `created_at`: Data de criação da conta do usuário.
   - `updated_at`: Data de atualização da conta do usuário.

Observação: Para manter o foco na análise dentro de Moçambique, foram removidos registros relacionados a algumas províncias. Isso foi feito para evitar confusão com nomes comuns de províncias e cidades como 'Gaza' e 'Beira' que podem se sobrepor a outros países.

Certifique-se de usar os dados corretos com base em suas necessidades de análise.

## Subpasta "results"

A subpasta 'results' contém os resultados finais das análises e visualizações realizadas no projeto. Esses resultados são gerados a partir dos dados processados e são apresentados de forma organizada e pronta para serem compartilhados. 
