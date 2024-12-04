import requests

class AniList:
    def __init__(self):  # Connect with AniList API
        self.api_url = "https://graphql.anilist.co"

    def recommend_anime(self, tags, genres, min_score):  # Recommend anime based on genres and score
        # Default genres and tags in case both are empty
        if not genres:
            genres = ["Action", "Adventure", "Comedy", "Romance"]
        if not tags:
            tags = ["Magic", "Isekai"]

        # GraphQL query
        query = """
            query($genres: [String], $tags: [String], $minScore: Int) {
                Page(perPage: 5) {
                    media(tag_in: $tags, genre_in: $genres, type: ANIME, averageScore_greater: $minScore, sort: SCORE_DESC) {
                        title {
                            romaji
                            english
                        }
                        genres
                        averageScore
                        description
                        episodes
                    }
                }
            }
        """
        
        variables = {"genres": list(genres), "tags": list(tags), "minScore": min_score}
        response = requests.post(self.api_url, json={"query": query, "variables": variables})
        
        if response.status_code == 200:
            data = response.json()
            media_list = data.get("data", {}).get("Page", {}).get("media", [])
            return self._process_anime_data(media_list)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return []

    def _process_anime_data(self, media_list):  # Process anime data
        results = []
        for media in media_list:
            if len(results) == 2:  # Limit to 2 recommendations
                break
            results.append({
                "id": media.get("id"),
                "title_romaji": media.get("title", {}).get("romaji"),
                "title_english": media.get("title", {}).get("english"),
                "description": media.get("description"),
                "genres": media.get("genres"),
                "averageScore": media.get("averageScore"),
                "episodes": media.get("episodes")
            })
        return results


#Example of usage
if __name__ == "__main__":
    # Create an instance of AniList
    anilist = AniList()

    # Example of user preferences
    genres = ["Romance"]  # Example genres
    tags = ["Zombie"]  # No tags provided
    min_score = 70  # Example minimum score filter

    # Recommend anime based on the provided preferences
    result = anilist.recommend_anime(tags, genres, min_score)

    # Print the result
    if not result:
        print("No recommendations found.")
    else:
        print("AniList Recommendations:")
        for anime in result:
            print(f"Anime ID: {anime['id']}")
            print(f"Romaji Title: {anime['title_romaji']}")
            print(f"English Title: {anime['title_english']}")
            print(f"Description: {anime['description']}")
            print(f"Genres: {', '.join(anime['genres'])}")
            print(f"Average Score: {anime['averageScore']}")
            print(f"Episodes: {anime['episodes']}")
            print()