import random

consonants = "bcdfghjklmnpqrstvwxyz"
vowels = "aeiou"
def generate_fake_word():
    """
    generate a random fake word for the user agent
    """
    word = ""
    length = random.choice([3,4,5,6])
    for i in range(length):
        word += random.choice(consonants)
        word += random.choice(vowels)
    return word

def generate_random_version():
    """
    generate a random version for the user agent
    """
    first_digit = random.choice(['0','1','2','3'])
    second_digit = random.choice(['0','1','2','3','4','5','6','7','8','9'])
    return first_digit + "." + second_digit

def random_tld():
    tlds = ['com', 'net', 'co', 'mil', 'biz', 'info', 'name', 'mobi', 'pro', 'travel', 'museum', 'coop', 'aero', 'xxx', 'idv', 'int', 'jobs', 'post', 'rec']
    return random.choice(tlds)

def get_fake_user_agent():
    fake_site = generate_fake_word()
    version = generate_random_version()
    domain = random_tld()
    return f'{fake_site}/{version} (http://{fake_site}.{domain})'