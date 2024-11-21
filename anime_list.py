import requests
from openAI_client import OpenAIClient
from dotenv import load_dotenv

load_dotenv()
class AniList:
    def __init__(self):
        self.api_url = "https://graphql.anilist.co"

    def search_anime(self, query_text):
        query = """
            query ($search: String) {
            Media(search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                }
                description
                genres
                averageScore
                episodes
            }
        }
        """

        variables = {"search" : query_text}
        response = requests.post(self.api_url, json = {"query" : query, "variables" : variables})
        
        if response.status_code == 200:
            data = response.json()
            media = data.get("data", {}).get("Media", None)
            return self._process_anime_data(media, query_text)
        else: 
            return {"error": f"API error: {response.status_code}"}

    def _process_anime_data(self, media, query_text):
        if media:
            return {
                "id" : media.get("id"),
                "title_romaji" : media.get("title", {}).get("romaji"),
                "title_english" : media.get("title", {}).get("english"),
                "description" : media.get("desciption"),
                "genres" : media.get("genres"),
                "averageScore" : media.get("averageScore"),
                "episodes" : media.get("episodes")
            }
    def _recommend_anime_openAI(self, query_text):
        client = OpenAIClient()
        prompt = (
            f"I searched for an anime titled '{query_text}', but it was not found. "
            "Can you recommend some similar anime based on its name?"
        )

        messages = [
            {"role" : "system", "content" : "You are a helpful assistant for recommend anime"},
            {"role" : "user", "content" : prompt}
        ]

        response = client.generate_text(messages)
        return {"recommendations" : response}

# if __name__ == "__main__":
#     # Create an instance of AniList
#     anilist = AniList()

#     # Search for an anime
#     anime_name = "Naruto Shippuden"  # Example anime name
#     result = anilist.search_anime(anime_name)

#     # Print the result
#     if "error" in result:
#         print(result["error"])
#     elif "recommendations" in result:
#         print("OpenAI Recommendations:")
#         print(result["recommendations"])
#     else:
#         print("AniList Data:")
#         print(f"Anime ID: {result['id']}")
#         print(f"Romaji Title: {result['title_romaji']}")
#         print(f"English Title: {result['title_english']}")
#         print(f"Description: {result['description']}")
#         print(f"Genres: {', '.join(result['genres'])}")
#         print(f"Average Score: {result['averageScore']}")
#         print(f"Episodes: {result['episodes']}")