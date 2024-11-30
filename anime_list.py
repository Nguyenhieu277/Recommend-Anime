import requests


class AniList:
    def __init__(self):  # Connect with AniList API
        self.api_url = "https://graphql.anilist.co"

    def recommend_anime(self, genres=None, min_score=70):  # Recommend anime based on genres and score
        query = """
            query($genres: [String], $minScore: Int) {
                Page(perPage: 5) {
                    media(genre_in: $genres, type: ANIME, averageScore_greater: $minScore, sort: SCORE_DESC) {
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

        # If no genres are provided, use a default set (e.g., "Action", "Adventure")
        genres = genres or ["Action", "Adventure", "Comedy", "Romance"]

        variables = {"genres": list(genres), "minScore": min_score}
        response = requests.post(self.api_url, json={"query": query, "variables": variables})
        
        if response.status_code == 200:
            data = response.json()
            media_list = data.get("data", {}).get("Page", {}).get("media", [])
            return self._process_anime_data(media_list)
        else:
            return {"error": f"API error: {response.status_code}"}

    def _process_anime_data(self, media_list):  # Process anime data
        if media_list:
            results = []
            for media in media_list:
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
        else:
            return {
                "message": "No recommendations found based on your preferences.",
                "suggestions": "Try adjusting your genre or score preferences."
            }


# if __name__ == "__main__":
#     # Create an instance of AniList
#     anilist = AniList()

#     # Example of user preferences
#     genres = ["Sports", "Action", "Drama"]  # Example genres
#     min_score = 80  # Example minimum score filter

#     # Recommend anime based on the provided preferences
#     result = anilist.recommend_anime(genres, min_score)

#     # Print the result
#     if "error" in result:
#         print(result["error"])
#     elif "message" in result:
#         print(result["message"])
#         print(result["suggestions"])
#     else:
#         print("AniList Recommendations:")
#         for anime in result:
#             print(f"Anime ID: {anime['id']}")
#             print(f"Romaji Title: {anime['title_romaji']}")
#             print(f"English Title: {anime['title_english']}")
#             print(f"Description: {anime['description']}")
#             print(f"Genres: {', '.join(anime['genres'])}")
#             print(f"Average Score: {anime['averageScore']}")
#             print(f"Episodes: {anime['episodes']}")
#             print()
