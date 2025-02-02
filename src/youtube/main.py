import requests


def github():
    response = requests.get('https://www.github.com')
    return response.status_code


if __name__ == "__main__":
    print(github())
