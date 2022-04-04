from secrets import token_urlsafe


def token_gen():
    token = token_urlsafe(16)
    with open("token.key", "w") as file:
        file.write(token)
        file.close()
    return token
