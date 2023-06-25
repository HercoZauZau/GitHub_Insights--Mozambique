*[leia em português](https://github.com/HercoZauZau/GitHub_Insights--Mozambique/blob/main/data/README-pt.md)*

This folder contains the project data, organized into three subfolders: "raw", "processed", and "results". Below is a detailed description of each subfolder and the files within them.

Note: It is important to update this folder whenever new results or visualizations are generated during the project.

## Subfolder "raw"

The 'raw' subfolder contains the raw data collected from the GitHub API. This data was initially collected through API requests and serves as the primary source for subsequent analysis.

## Subfolder "processed"

The 'processed' subfolder contains the processed data after cleaning, transforming, and aggregating the raw collected data. This processed data is used for further analysis and generating final results.

- `repos_data.csv`: This file contains information about the repositories created on GitHub. Each record represents a repository and includes the following fields:
   - `id`: Unique identifier of the repository.
   - `owner_id`: Unique identifier of the repository owner.
   - `language`: Main programming language of the repository.
   - `created_at`: Creation date of the repository.
   - `updated_at`: Update date of the repository.
   - `stargazers_count`: Number of stars received by the repository.
   - `forks_count`: Number of forks of the repository.

- `starred_data.csv`: This file contains information about the repositories liked by users. Each record represents preferences among all liked repositories and includes the following fields:
   - `user_id`: Unique identifier of the user.
   - `has_moz_owner`: Indicator if any of the starred repositories belongs to a Mozambican owner.
   - `fav_lang`: User's favorite programming language.
   - `fav_topic`: User's favorite topic.

- `user_data.csv`: This file contains information about the GitHub users. Each record represents a user and includes the following fields:
   - `id`: Unique identifier of the user.
   - `city_id`: Unique identifier of the city where the user is located.
   - `followers`: Number of followers of the user.
   - `following`: Number of users the user is following.
   - `created_at`: Account creation date of the user.
   - `updated_at`: Account update date of the user.

Note: In order to focus the analysis within Mozambique, records related to some provinces have been removed. This was done to avoid confusion with common provincial and city names like 'Gaza' and 'Beira' which may overlap with other countries.
Make sure to use the correct data based on your analysis needs.

## Subfolder "results"

The 'results' subfolder contains the final results of the analyses and visualizations conducted in the project. These results are generated from the processed data and are presented in an organized format ready to be shared.
