# You can use this to restrict access based on recognition result
AUTHORIZED_USERS = {"Alice", "Bob"}

def is_authorized(name):
    return name in AUTHORIZED_USERS
