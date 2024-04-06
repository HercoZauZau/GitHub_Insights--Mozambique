*[read in english](https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/README.md)*

# GitHub Insights - Explorando o Ecossistema dos Desenvolvedores Moçambicanos

<div align='center'>
<img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/assets/img/MozFlag.png?raw=true" width="100%" height="100%">

----

Este projeto tem como objetivo realizar análises de dados com base nas informações públicas disponibilizadas pela API do GitHub, focando nos usuários em Moçambique. Buscamos extrair insights valiosos dos dados dos usuários, seus repositórios e repositórios curtidos, a fim de compreender padrões, identificar tendências de desenvolvimento e explorar a dinâmica da comunidade de desenvolvedores em Moçambique.


## Metodologia

A análise de dados no projeto segue uma abordagem metodológica que envolve as seguintes etapas:

1. **Coleta de Dados**: Os dados utilizados neste projeto são obtidos por meio da API do GitHub. Através dos endpoints disponibilizados pela API, coletamos informações sobre os usuários, seus repositórios, suas interações com outros repositórios e outros elementos do GitHub. É importante ressaltar que as análises são baseadas apenas nos dados públicos disponíveis na API do GitHub, e a disponibilidade e acessibilidade desses dados estão sujeitas às políticas e limitações da plataforma.

2. **Pré-processamento dos Dados**: Após a coleta, realizamos uma etapa de pré-processamento para limpar e estruturar os dados. Isso envolve a remoção de dados irrelevantes, tratamento de valores nulos, conversão de formatos e outras transformações necessárias para tornar os dados adequados para análise.

3. **Análises**: Exploramos tendências e outros pontos a partir dos dados coletados. Isso inclui a análise entradas de novos usuários ao longo do tempo, a identificação de tecnologias em tendência, a análise de popularidade de determinadas linguagens de programação e outras tendências relevantes para o ecossistema do GitHub.

4. **Visualizações Interativas**: Criamos visualizações interativas para facilitar a exploração e compreensão dos dados. Utilizamos bibliotecas de visualização, como matplotlib para criar gráficos, plots e outras representações visuais dos resultados da análise.


## Resultados e Insights

Alguns exemplos de insights obtidos incluem:

- Distribuição de usuários por provincia: Permite identificar quais províncias têm uma presença mais significativa de usuários na plataforma.
  
- Popularidades das linguagens de programação em Moçambique ao longo do tempo: Esta análise nos ajuda a entender as tendências e preferências em relação às linguagens de programação no país.
  
- Entrada de moçambicanos no GitHub ao longo do tempo: Exibe as tendências de crescimento e adoção do GitHub pela comunidade de desenvolvedores em Moçambique.
  
- Tópicos em tendência em Moçambique: Envolve a identificação dos tópicos em tendência dentro da comunidade de desenvolvedores em Moçambique, usando análise de palavras-chave nos repositórios. Isso nos ajuda a entender as áreas de interesse e foco da comunidade de desenvolvedores do país.
  
- Percentagem de usuários que curtiram repositórios nacionais: Nos permite avaliar o envolvimento e o apoio da comunidade de desenvolvedores moçambicanos em relação aos projetos e iniciativas locais.


<div align='center'>
  
| Distribuição de usuários por provincia  |
|------------|
| <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2023_06/number_of_registered_users_per_province.png?raw=true" width="800"> |

</div>

<div align='center'>
  
| Entrada de usuários por ano      | Tópicos em tendência       |
|------------|-------------|
| <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/number_of_registered_users_per_year.png?raw=true" width="400"> | <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/trending_topics.png?raw=true" width="400"> |

</div>

<div align='center'>
  
| Usuários que curtem repositórios nacionais      | Linguagens mais usadas       |
|------------|-------------|
| <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/percentage_of_users_who_starred_at_least_1_mozambican_repository.png?raw=true" width="400"> | <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/trends_of_most_used_languages_in_repositories.png?raw=true" width="400"> |

</div>


## Limitações

É importante reconhecer as limitações do projeto, a fim de interpretar os resultados com cuidado e compreender suas restrições. As principais limitações incluem:

1. **Limitações dos Dados**: As análises são baseadas nos dados disponíveis na API do GitHub. Portanto, quaisquer limitações ou restrições impostas pela API, como limites de solicitação ou disponibilidade de dados específicos, podem afetar a abrangência e a precisão das análises. Além disso, a qualidade e a consistência dos dados dependem da precisão e atualização das informações fornecidas pelos usuários do GitHub.

2. **Restrições dos Acessos Públicos**: Ao utilizar dados públicos do GitHub, é importante lembrar que nem todos os repositórios estão disponíveis publicamente. Portanto, a análise pode ser limitada apenas aos dados públicos acessíveis. Isso resulta em limitações na análise de repositórios privados.

3. **Suposições e Generalizações**: Durante a análise, podem ser feitas suposições e generalizações com base nos dados disponíveis. Essas suposições podem não ser aplicáveis a todos os contextos ou podem não refletir completamente a complexidade e a diversidade dos projetos e contribuições no GitHub.

4. **Vieses na Análise**: A análise de dados está sujeita a vieses inerentes, como vieses de seleção ou vieses de amostragem. Por exemplo, a escolha de determinados repositórios ou contribuidores para análise pode introduzir vieses na interpretação dos resultados. É importante estar ciente desses vieses e interpretar os resultados com cautela.

5. **Localização**: É preciso levar em consideração que as análises realizadas neste projeto estão restritas aos usuários de Moçambique que registraram sua localização no GitHub. É possível que existam outros usuários moçambicanos com informações de localização desatualizadas ou ausentes, o que pode impactar a representatividade dos resultados obtidos.


## Pré-requisitos

Antes de executar o projeto, verifique se você atende aos seguintes pré-requisitos:

- Python: Certifique-se de ter o Python instalado em sua máquina. Você pode baixar a versão mais recente do Python em https://www.python.org/downloads/.

- Chave de acesso à API do GitHub (opcional): Pode se obter uma chave de acesso pessoal para autenticar as solicitações à API do GitHub. Siga as instruções em https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token para gerar sua chave de acesso pessoal.

- Bibliotecas Python: É recomendado ter as seguintes bibliotecas Python instaladas:
    - pandas
    - numpy
    - matplotlib
    - csv
    - requests
    - dotenv
    - wordcloud

## Sequência de Execução:

1. data_collect/get_users_ids.ipynb
2. cleaning_and_structuring/structure_ids.ipynb
3. data_collect/get_users_data.ipynb
4. data_collect/get_repos_data.ipynb
5. data_collect/get_starred_data.ipynb
6. visualization/users_insights.ipynb
7. visualization/repos_insights.ipynb
8. visualization/starred_insights.ipynb

## Contribuição

Se você deseja contribuir para este projeto, fique à vontade para abrir uma issue com suas sugestões ou envie um pull request com suas alterações. Sua contribuição será muito apreciada!

<div align='center'>
<img src="https://media3.giphy.com/media/3oriePyO5ePbJWMHPW/giphy.gif?cid=ecf05e47550izrqszztx5yqt8ft70mevtzbjst0d358qhwgu&ep=v1_gifs_search&rid=giphy.gif&ct=g" width="100%" height="100%">
</div>

---

## Feito com
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)

## Autor
- [Hérco ZauZau](https://github.com/HercoZauZau)
- Link do projecto: https://github.com/HercoZauZau/GitHub_Insights--Mozambique
  
