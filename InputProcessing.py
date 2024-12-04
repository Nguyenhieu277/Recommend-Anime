import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
nltk.download('punkt_tab')
nltk.download('stopwords')

class InputProcessor:
    def __init__(self):
        
        self.stop_words = set(stopwords.words("english"))
        self.genres_list = [
            "action", "adventure", "comedy", "drama", "ecchi", "fantasy", 
            "horror", "mahou shoujo", "mecha", "music", "mystery", 
            "psychological", "romance", "sci-fi", "slice of life", 
            "sports", "supernatural", "thriller"
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
            "astronomy": ["sci-fi", "space", "fantasy"],
            "martial arts": ["martial arts", "action", "sports", "mecha"],
            "magical": ["fantasy", "advanture", "shoujo"]
        }
        self.tags = [
            "4-koma", "achronological order", "afterlife", "age gap", "airsoft", "aliens", 
            "alternate universe", "american football", "amnesia", "anti-hero", "archery", 
            "assassins", "athletics", "augmented reality", "aviation", "badminton", "band", 
            "bar", "baseball", "basketball", "battle royale", "biographical", "bisexual", 
            "body swapping", "boxing", "bullying", "calligraphy", "card battle", "cars", 
            "cgi", "chibi", "chuunibyou", "classic literature", "college", "coming of age", 
            "cosplay", "crossdressing", "crossover", "cultivation", "cute girls doing cute things", 
            "cyberpunk", "cycling", "dancing", "delinquents", "demons", "development", 
            "dragons", "drawing", "dystopian", "economics", "educational", "ensemble cast", 
            "environmental", "episodic", "espionage", "fairy tale", "family life", "fashion", 
            "female protagonist", "fishing", "fitness", "flash", "food", "football", "foreign", 
            "fugitive", "full cgi", "full colour", "gambling", "gangs", "gender bending", 
            "gender neutral", "ghost", "gods", "gore", "guns", "gyaru", "harem", "henshin", 
            "hikikomori", "historical", "ice skating", "idol", "isekai", "iyashikei", "josei", 
            "kaiju", "karuta", "kemonomimi", "kids", "love triangle", "mafia", "magic", 
            "mahjong", "maids", "male protagonist", "martial arts", "memory manipulation", 
            "meta", "military", "monster girl", "mopeds", "motorcycles", "musical", 
            "mythology", "nekomimi", "ninja", "no dialogue", "noir", "nudity", "otaku culture", 
            "outdoor", "parody", "philosophy", "photography", "pirates", "poker", "police", 
            "politics", "post-apocalyptic", "primarily adult cast", "primarily female cast", 
            "primarily male cast", "puppetry", "real robot", "rehabilitation", "reincarnation", 
            "revenge", "reverse harem", "robots", "rugby", "rural", "samurai", "satire", 
            "school", "school club", "seinen", "ships", "shogi", "shoujo", "shoujo ai", 
            "shounen", "shounen ai", "slapstick", "slavery", "space", "space opera", 
            "steampunk", "stop motion", "super power", "super robot", "superhero", 
            "surreal comedy", "survival", "swimming", "swordplay", "table tennis", "tanks", 
            "teacher", "tennis", "terrorism", "time manipulation", "time skip", "tragedy", 
            "trains", "triads", "tsundere", "urban fantasy", "vampire", "video games", 
            "virtual world", "volleyball", "war", "witch", "work", "wrestling", "writing", 
            "wuxia", "yakuza", "yandere", "youkai", "zombie", "misc"
        ]

        self.stemmer = PorterStemmer()

    def process_input(self, user_input):

        words = word_tokenize(user_input.lower())
        filtered_words = [word for word in words if word.isalpha() and word not in self.stop_words]

    
        genres = [word for word in filtered_words if word in self.genres_list]

        hobbies = [word for word in words if word in self.hobby_map]

        tags = [word for word in words if word in self.tags]
        for hobby in hobbies:
            genres.extend(self.hobby_map[hobby])

        genres = list(dict.fromkeys(genres))
        tags = list(dict.fromkeys(tags))
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
            "tags" : tags,
            "min_score" : min_score
        }

# if __name__ == '__main__':
#     processor = InputProcessor()
#     test_cases = [
#         "romance and zombie anime",
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