import random, string

def generate(length=6):
	code = ''.join(random.choices(string.ascii_uppercase, k=length))
	return code