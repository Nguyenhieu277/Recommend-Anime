import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')
nltk.download('stopwords')

class InputProcessor:
    def __init__(self):
        
        self.stop_words = set(stopwords.words("english"))
        self.genres_list = [
            "action", "adventure", "comedy", "drama", "fantasy", "horror", "romance", 
            "sci-fi", "slice of life", "sports", "supernatural", "game", "gourmet", 
            "music", "mecha", "psychological", "mystery", "thriller", "historical", 
            "military", "martial arts", "ecchi", "harem", "reverse harem", "shoujo", 
            "shounen", "seinen", "josei", "cyberpunk", "post-apocalyptic", "magic", 
            "parody", "school", "survival", "tragedy", "demons", "kids", 
            "romantic comedy", "superpower", "dark fantasy", "isekai", "crime", 
            "idols", "vampire", "zombie", "steampunk", "detective", "medical", 
            "battle royale", "space", "time travel", "dystopian", "anthropomorphic", 
            "mythology", "yaoi", "yuri", "otokonoko", "alchemy", "political", 
            "family", "nature", "healing", "reverse isekai"
        ]
 
        self.hobby_map = {
            "sports": ["sports", "action", "adventure"],
            "music": ["music", "slice of life", "romantic comedy"],
            "cooking": ["gourmet", "slice of life", "comedy"],
            "gaming": ["game", "sci-fi", "action", "adventure", "fantasy"],
            "reading": ["mystery", "fantasy", "historical", "psychological", "thriller"],
            "technology": ["sci-fi", "mecha", "cyberpunk", "post-apocalyptic"],
            "dancing": ["music", "slice of life"],
            "traveling": ["adventure", "historical", "fantasy", "sci-fi"],
            "art": ["romance", "slice of life", "historical", "parody"],
            "fitness": ["sports", "action", "survival"],
            "nature": ["nature", "healing", "fantasy"],
            "photography": ["slice of life", "nature", "historical"],
            "studying": ["school", "psychological", "mystery"],
            "movies": ["drama", "romantic comedy", "thriller", "action"],
            "coding": ["sci-fi", "cyberpunk", "mecha", "magic"],
            "volunteering": ["family", "slice of life", "healing"],
            "meditation": ["healing", "slice of life", "nature"],
            "writing": ["tragedy", "drama", "fantasy", "psychological"],
            "socializing": ["romantic comedy", "slice of life", "comedy"],
            "collecting": ["historical", "fantasy", "mystery"],
            "adventuring": ["adventure", "survival", "action", "post-apocalyptic"],
            "fashion": ["romance", "slice of life", "comedy"],
            "gardening": ["nature", "healing", "slice of life"],
            "anime": ["romantic comedy", "action", "sci-fi", "fantasy"],
            "astronomy": ["sci-fi", "space", "fantasy"],
            "martial arts": ["martial arts", "action", "sports", "mecha"]
        }


    def process_input(self, user_input):

        words = word_tokenize(user_input.lower())
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words]

    
        genres = [word for word in filtered_words if word in self.genres_list]

        hobbies = [word for word in words if word in self.hobby_map]

        for hobby in hobbies:
            genres.extend(self.hobby_map[hobby])

        genres = list(dict.fromkeys(genres))
        min_score = 70
        words_with_numbers = word_tokenize(user_input.lower())
        for i, word in enumerate(words_with_numbers):
            if word.isdigit():
                score = int(word)
                if 0 <= score <= 100:
                    min_score = score
            elif word in ["above", "minimum", "at", "least", "with"] and i + 1 < len(words_with_numbers):
                if words_with_numbers[i + 1].isdigit():
                    score = int(words_with_numbers[i + 1])
                    if 0 <= score <= 100:
                        min_score = score


        return {
            "genres" : genres,
            "min_score" : min_score
        }

# if __name__ == '__main__':
#     processor = InputProcessor()
#     test_cases = [
#         "I love watching anime with at least 80 score",
#         "Can you recommend some romance or drama anime? Minimum score: 90.",
#         "Looking for sci-fi and supernatural anime, maybe something above 75.",
#         "I'm into sports and adventure shows. Surprise me!",
#         "What are some good comedy anime? Anything works, score doesn't matter.",
#         "I enjoy cooking and gaming. Recommend something fun!",
#         "I'm a fan of music and dancing. Any suggestions?"
#     ]

#     for idx, input_text in enumerate(test_cases):
#         print(f"Test Case {idx + 1}:")
#         print(f"Input: {input_text}")
#         result = processor.process_input(input_text)
#         print("Processed Result:", result)
#         print("-" * 40)