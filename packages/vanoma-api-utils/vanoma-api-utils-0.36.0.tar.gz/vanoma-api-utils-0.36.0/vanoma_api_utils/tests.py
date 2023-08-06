from random import randint
from faker import Faker


faker = Faker()


def random_phone_number() -> str:
    return f"2507{randint(10000000, 100000000)}"
