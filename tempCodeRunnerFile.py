if __name__ == "__main__":
    # Create an instance of AniList
    anilist = AniList()

    # Example of user preferences
    genres = ["Sports", "Action", "Drama"]  # Example genres
    min_score = 80  # Example minimum score filter

    # Recommend anime based on the provided preferences
    result = anilist.recommend_anime(genres, min_score)

    # Print the result
    if "error" in result:
        print(result["error"])
    elif "message" in result:
        print(result["message"])
        print(result["suggestions"])
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
