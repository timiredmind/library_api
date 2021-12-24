from passlib.hash import bcrypt

def hash_password(plain_text):
    hashed_password = bcrypt.using(rounds=13).hash(plain_text)
    return hashed_password