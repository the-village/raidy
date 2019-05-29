import random


def generate_random_id():
    return random.randint(0, 1000000)


def mask_message(text):
    return text + ' ' + str(random.randint(1, 10000000))

def trimming_message(text, symbols):
    symbols = [x+random.randint(1, 3) for x in range(symbols)]
    symbol = random.choice(symbols)
    return text[symbol:]
