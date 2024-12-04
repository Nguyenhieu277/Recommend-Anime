if __name__ == '__main__':
    processor = InputProcessor()
    test_cases = [
        "I love watching zombie anime",
        "Can you recommend some romance or drama anime? Minimum score: 90.",
        "Looking for sci-fi and supernatural anime, maybe something above 75.",
        "I'm into sports and adventure shows. Surprise me!",
        "What are some good comedy anime? Anything works, score doesn't matter.",
        "I enjoy cooking and gaming. Recommend something fun!",
        "I'm a fan of music and dancing. Any suggestions?"
    ]

    for idx, input_text in enumerate(test_cases):
        print(f"Test Case {idx + 1}:")
        print(f"Input: {input_text}")
        result = processor.process_input(input_text)
        print("Processed Result:", result)
        print("-" * 40)