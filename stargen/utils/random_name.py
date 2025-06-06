import random
import string

def generate_random_name():
    # Set the length of the random name between 8 and 16
    length = random.randint(8, 16)
    
    # Generate a random name with the chosen length
    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    return random_name
