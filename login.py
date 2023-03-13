import requests
import logging
import typer

# first endpoint where you login with wifirst credentials
LOGIN_PAGE = "https://portal-front.wifirst.net/api/sessions"
# second endpoint where you authenticate with the wifirst provided credentials
HTML_LOGIN_PAGE = "https://wireless.wifirst.net/goform/HtmlLoginRequest"
# get the fragments id
SETTINGS_PAGE = "https://portal-front.wifirst.net/api/settings?force_production=false"
# get the token for login
TOKEN_PAGE = "https://wireless.wifirst.net/index.txt"


def get_token():
    token = requests.get(TOKEN_PAGE).text
    logging.info(f'Fetched token: {token}')
    return token


def get_fragment():
    r = requests.get(SETTINGS_PAGE)
    logging.info("Fetched settings page")
    fragment = next(x for x in r.json().get('fragments')
                    if x['template'] == 'end_user_freezone_signin')
    logging.info(
        f'Extracted fragment with id "{fragment["id"]}" from settings page')

    return fragment['id']


def get_payload1(email: str, password: str):
    return {"email": email,
            "password": password,
            "box_token": get_token(),
            "fragment_id": get_fragment()}


def get_payload2(response: requests.Response):
    return {
        "username": response['radius'].get('login'),
        "password": response['radius'].get('password'),
        "success_url": "https://portal-selfcare.wifirst.net/",
        "error_url": "https://portal-front.wifirst.net/connect-error",
        "update_session": 0
    }


def login(email: str, password: str = typer.Option(..., "--password", "-p", prompt=True, hide_input=True)):
    logging.info(f'Logging in as {email}')
    resp = requests.post(LOGIN_PAGE, get_payload1(email, password)).json()
    logging.info(
        f'Successfully logged in and got wifirst credentials: {resp["radius"].get("login")} with password {resp["radius"].get("password")}')
    requests.post(HTML_LOGIN_PAGE, get_payload2(resp))


if __name__ == "__main__":
    try:
        typer.run(login)
    except requests.exceptions.ConnectionError:
        logging.error("You are not connected to the wifirst network")
