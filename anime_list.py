import requests
from InputProcessing import InputProcessor
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
# if __name__ == "__main__":
#     processor = InputProcessor()
#     prompt = "Romance and zombie anime"
#     processed = processor.process_input(prompt)
#     genres = set(processed["genres"])
#     tags = set(processed["tags"])
#     min_score = processed["min_score"]

#     ani = AniList()
#     recommend = ani.recommend_anime(tags, genres, min_score)

#     bot_response = "".join(
#             f"<div>"
#             f"<h2>Title: {anime.get('title_english', anime.get('title_romaji', 'N/A'))}</h2>"
#             f"<p><strong>Description:</strong> {anime.get('description', 'No description available')}</p>"
#             f"<p><strong>Genres:</strong> {', '.join(anime.get('genres', []))}</p>"
#             f"<p><strong>Average Score:</strong> {anime.get('averageScore', 'N/A')}</p>"
#             f"<p><strong>Episodes:</strong> {anime.get('episodes', 'N/A')}</p>"
#             f"</div><br>"
#             if isinstance(anime, dict)
#             else "<p>Don't have anime based on your description</p>"
#             for anime in recommend
#         )
#     print(bot_response)
    