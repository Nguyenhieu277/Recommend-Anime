# Overview

The "Recommend Anime" project is a recommendation system designed to help users find anime that match their interests and preferences. By analyzing natural language input, the system filters anime based on genres, minimum scores, and hobbies, delivering personalized suggestions. If no anime fits the query, it provides guidance to refine the search.



## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install packages.

```bash
pip install requirements.txt
```
## Features
- Natural Language Input: Accepts plain English queries (e.g., "I want romance and action anime with a score above 90").
- Genre Matching: Identifies anime genres from user input.
- Score Filtering: Filters recommendations based on minimum average score.
- Hobby-Based Mapping: Matches hobbies to related genres for broader recommendations.
- Fallback Responses: Informs users when no anime matches their criteria.
- Detailed Output: Provides titles, descriptions, genres, scores, and episode counts for each recommendation.

## Requirements

- Using AniList databases
- nltk (Natural Language Toolkit)
- streamlit (for user interface, if applicable)
## Usage
Running the Application
Clone the repository:

```bash
git clone https://github.com/your-username/recommend-anime.git
cd recommend-anime
```
Run the app with streamlit:

```bash
streamlit run app.py
```
Input a query in natural language to get anime recommendations.

## Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch:
```bash
git checkout -b feature/your-feature
```
Commit your changes:
```bash
git commit -m "Add your feature"
```
Push to the branch:
```bash
git push origin feature/your-feature
```
Create a pull request.
## License

[MIT](https://choosealicense.com/licenses/mit/)
