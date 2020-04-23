import click
import requests
from . import config, database


@click.group()
def auth():
    pass


@auth.command()
def register():
    print("Input Username:")
    username = input("- ")
    print("Input Email:")
    email = input("- ")
    print("Input Password:")
    password = input("- ")
    requestBody = {
        "username": username,
        "email": email,
        "password": password
    }
    try:
        registerRequest = requests.post(f"{config.pulseURL}/register", json=requestBody)
    except requests.exceptions.ConnectionError:
        print("Failed to connect to server")
        quit()

    if registerRequest.status_code == 200:
        print("Registered Successfully! Please Login with 'auth login'")
    else:
        print("An Error Occurred, dumping:")
        print(registerRequest.raw)


@auth.command()
def login():
    print("Input Email:")
    email = input("- ")
    print("Input Password:")
    password = input("- ")
    requestBody = {
        "email": email,
        "password": password,
        "scope": "write"
    }
    try:
        tokenRequest = requests.post(f"{config.pulseURL}/get_token", json=requestBody)
    except requests.exceptions.ConnectionError:
        print("Failed to connect to server")
        quit()

    if tokenRequest.status_code == 200:
        for message in tokenRequest.json().get("messages"):
            print(message)
        token = tokenRequest.json().get("response")
        if token is None:
            print("No Token! Something went wrong, and the server hasnt given us a token!")
            quit()
        print(f"Your Auth Token is: {token}")
        print("Storing in local DB for later usage...")
        database["authToken"] = token
        database.commit()
        print("Token Stored!")
        quit()
    else:
        print("An Error Occurred, dumping:")
        print(registerRequest.raw)
        quit()
