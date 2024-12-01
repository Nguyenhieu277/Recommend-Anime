if __name__ == "__main__":
    client = OpenAIClient()
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant to recommend anime",
        },
        {
            "role": "user",
            "content": "I want to romance anime ",
        }
    ]
    response = client.get_response(messages)
    print(response)