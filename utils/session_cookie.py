# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:nomarker
#     text_representation:
#       extension: .py
#       format_name: nomarker
#       format_version: '1.0'
#       jupytext_version: 1.16.3
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

import json
from pathlib import Path
from selenium import webdriver
from typing import Union

from getpass import getpass


# to-do: hash creds

def get_session_cookie(
        path: Union[Path, str] = Path(__file__).parent/"session_cookie.txt"
    ):
    with Path(path).open(mode="r") as file:
        return file.read()


def update_session_cookie(site: str):
    accepted = ("github", "google", "twitter", "reddit")
    site = site.lower().strip().replace(" ", "")
    assert site in accepted, f"You can only login from one of the following: {accepted}"

    data = _get_data(site=site)
    _overwrite(logs=data)


def _get_data(site: str, log_type: str = "performance"):
    login = "/2024/auth/login"
    auth_url = f"/auth/{site}"
    username = input('Account: ')
    password = getpass('Enter password: ')

    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_experimental_option("detach", True)
    options.add_argument("--enable-logging")
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    driver = webdriver.Chrome(options=options)
    driver.get("https://adventofcode.com/")

    driver.find_element(by="xpath", value=f'//a[@href="{login}"]').click()
    driver.find_element(by="xpath", value=f'//a[@href="{auth_url}"]').click()

    if site == "github":
        driver.find_element("id", "login_field").send_keys(username)
        driver.find_element("id", "password").send_keys(password)
        driver.find_element("name", "commit").click()

        totp = input("Please enter your TOTP from authentication app: ")
        driver.find_element("id", "app_totp").send_keys(totp)
    driver.refresh()

    logs = driver.get_log(log_type)
    driver.close()
    return logs


def _overwrite(logs: list, file_path: Union[str, Path] = None):
    updated = False
    for log in logs:
        try:
            message_obj = json.loads(log.get("message"))
            message = message_obj.get("message")
            method = message.get("method")
            if method == "Network.requestWillBeSentExtraInfo":
                cookies = message.get("params").get("associatedCookies")
                for cookie in cookies:
                    cookie_name = cookie["cookie"]["name"]
                    if cookie_name == "session":
                        session_cookie = cookie["cookie"]["value"]
                        if not file_path:
                            file_path = (
                                Path("./wip.ipynb").parent / "session_cookie.txt"
                            )
                        Path(file_path).write_text(session_cookie)
                        updated = True
                        break
        except Exception as e:
            print(e)
        if updated:
            break

    if not updated:
        print("Cannot find session cookie :(")
    else:
        print("Done!")
