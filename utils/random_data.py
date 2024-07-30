from faker import Faker


def generate_random_data():
    fake = Faker()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = fake.email()
    avatar = fake.image_url()

    return first_name, last_name, email, avatar
