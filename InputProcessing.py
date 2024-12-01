import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt_tab')
nltk.download('stopwords')

class InputProcessor:
    def __init__(self):
        
        self.stop_words = set(stopwords.words("english"))
        self.genres_list = [
            "action", "adventure", "comedy", "drama", "fantasy",
            "horror", "romance", "sci-fi", "slice of life", "sports", "supernatural", "game", "gourmet", "music",
            "mecha"
        ]  
        self.hobby_map = {
            "sports": ["sports"], 
            "music": ["music"],
            "cooking": ["gourmet", "slice of life"],
            "gaming": ["game", "sci-fi", "action", "adventure"],
            "reading": ["mystery", "fantasy"],
            "technology": ["sci-fi", "mecha"],
            "dancing": ["music"],
        }

    def process_input(self, user_input):

        words = word_tokenize(user_input.lower())
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words]

    
        genres = [word for word in filtered_words if word in self.genres_list]

        hobbies = [word for word in filtered_words if word in self.hobby_map]

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
#         "I want to romance anime with at least 80 score",
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