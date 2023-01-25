def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello", "hi", "sup",):
        return "Hey"

    if user_message in ("who are you"):
        return "I am a bot"