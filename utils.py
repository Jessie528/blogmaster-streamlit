import random

def get_joke():
    jokes = [
        "Why don't programmers like nature? It has too many bugs.",
        "Why do Java developers wear glasses? Because they don't C#.",
        "Why did the developer go broke? Because he used up all his cache.",
        "Why do Python programmers prefer snake_case? Because it’s readable!",
        "Why did the computer get glasses? To improve its web sight!",
        "I told my laptop it was getting too hot. Now it won’t stop fanning itself.",
        "Why did the robot write a blog? It couldn’t resist a byte of fame!",
    ]
    return random.choice(jokes)
