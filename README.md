*[leia em português](https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/README-pt.md)*

# GitHub Insights - Exploring the Mozambican Developer Ecosystem

<div align='center'>
<img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/assets/img/MozFlag.png?raw=true" width="100%" height="100%">
</div>

----

This project aims to perform data analysis based on publicly available information from the GitHub API, focusing on users in Mozambique. We seek to extract valuable insights from user data, their repositories, and starred repositories to understand patterns, identify development trends, and explore the dynamics of the developer community in Mozambique.


## Methodology

The data analysis in the project follows a methodological approach that involves the following steps:

1. **Data Collection**: The data used in this project is obtained through the GitHub API. Through the API endpoints, we collect information about users, their repositories, their interactions with other repositories, and other GitHub elements. It is important to note that the analyses are based solely on the publicly available data in the GitHub API, and the availability and accessibility of this data are subject to the platform's policies and limitations.

2. **Data Preprocessing**: After collection, we perform a preprocessing step to clean and structure the data. This involves removing irrelevant data, handling null values, converting formats, and other necessary transformations to make the data suitable for analysis.

3. **Analysis**: We explore trends and other insights from the collected data. This includes analyzing the entry of new users over time, identifying trending technologies, analyzing the popularity of specific programming languages, and other relevant trends for the GitHub ecosystem.

4. **Interactive Visualizations**: We create interactive visualizations to facilitate data exploration and understanding. We use visualization libraries such as Matplotlib to create charts, plots, and other visual representations of the analysis results.


## Results and Insights

Some examples of obtained insights include:

- Distribution of users by province: Allows identifying which provinces have a significant presence of users on the platform.

- Popularity of programming languages in Mozambique over time: This analysis helps us understand trends and preferences regarding programming languages in the country.

- Entry of Mozambicans on GitHub over time: Displays the growth and adoption trends of GitHub by the developer community in Mozambique.

- Trending topics in Mozambique: Involves identifying trending topics within the developer community in Mozambique, using topics analysis on repositories. This helps us understand the areas of interest and focus of the country's developer community.

- Percentage of users who liked national repositories: Allows us to evaluate the involvement and support of Mozambican developers in relation to local projects and initiatives.


<div align='center'>
  
| Distribution of users by province  |
|------------|
| <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_02/number_of_registered_users_per_province.png?raw=true" width="800"> |

</div>

<div align='center'>
  
| Users entry per year      | Trending topics       |
|------------|-------------|
| <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/number_of_registered_users_per_year.png?raw=true" width="400"> | <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/trending_topics.png?raw=true" width="400"> |

</div>

<div align='center'>
  
| Users who liked national repositories      | Most used languages       |
|------------|-------------|
| <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/percentage_of_users_who_starred_at_least_1_mozambican_repository.png?raw=true" width="400"> | <img src="https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/results/2024_01/trends_of_most_used_languages_in_repositories.png?raw=true" width="400"> |

</div>


## Limitations

It is important to acknowledge the limitations of the project in order to interpret the results carefully and understand its constraints. The main limitations include:

1. **Data Limitations**: The analyses are based on the data available in the GitHub API. Therefore, any limitations or restrictions imposed by the API, such as request limits or specific data availability, can affect the scope and accuracy of the analyses. Additionally, the quality and consistency of the data depend on the accuracy and updating of the information provided by GitHub users.

2. **Public Access Restrictions**: When using public GitHub data, it is important to remember that not all repositories are publicly available. Therefore, the analysis may be limited only to accessible public data. This results in limitations in analyzing private repositories.

3. **Assumptions and Generalizations**: During the analysis, assumptions and generalizations may be made based on the available data. These assumptions may not be applicable to all contexts or may not fully reflect the complexity and diversity of projects and contributions on GitHub.

4. **Analysis Biases**: Data analysis is subject to inherent biases, such as selection biases or sampling biases. For example, the choice of specific repositories or contributors for analysis may introduce biases in interpreting the results. It is important to be aware of these biases and interpret the results with caution.

5. **Location**: It is necessary to take into account that the analyses performed in this project are restricted to users from Mozambique who have registered their location on GitHub. There may be other Mozambican users with outdated or missing location information, which may impact the representativeness of the obtained results.


## Prerequisites

Before running the project, make sure you meet the following prerequisites:

- Python: Make sure you have Python installed on your machine. You can download the latest version of Python at https://www.python.org/downloads/.

- GitHub API Access Key (optional): You can obtain a personal access key to authenticate requests to the GitHub API. Follow the instructions at https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token to generate your personal access key.

- Python Libraries: It is recommended to have the following Python libraries installed:
    - pandas
    - numpy
    - matplotlib
    - csv
    - requests
    - dotenv
    - wordcloud

## Contribution

If you wish to contribute to this project, feel free to open an issue with your suggestions or submit a pull request with your changes. Your contribution will be greatly appreciated!

<div align='center'>
<img src="https://media3.giphy.com/media/3oriePyO5ePbJWMHPW/giphy.gif?cid=ecf05e47550izrqszztx5yqt8ft70mevtzbjst0d358qhwgu&ep=v1_gifs_search&rid=giphy.gif&ct=g" width="100%" height="100%">
</div>

---

## Made with
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-%23ffffff.svg?style=for-the-badge&logo=Matplotlib&logoColor=black)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)


## Author
- [Hérco ZauZau](https://github.com/HercoZauZau)
- Project Link: https://github.com/HercoZauZau/GitHub_Insights--Mozambique
