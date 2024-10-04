import requests
from pathlib import Path
from typing import Union

assert_message = """
Get your session cookie to retrieve the correct input!

Go to any AoC input link > `Inspect` > `Network` tab > Refresh the page > Find `Cookie` header > Copy the text after `session=` :)
""".strip()

def download_input(year: Union[int, str], day: Union[int, str], session_cookie: str = None):
    if isinstance(year, int):
        year = str(year)
    
    if isinstance(day, int):
        day = str(day)
    day = day.lstrip('0')
    
    if session_cookie is None:
        session_cookie = get_session_cookie()
    assert session_cookie, assert_message
    
    s = requests.Session()
    r = s.get(f'https://adventofcode.com/{year}/day/{day}/input', cookies = {'session': session_cookie})
    inp = r.text
    
    return inp.split('\n')[:-1]


def get_session_cookie(path: Union[Path, str] = '../utils/aoc_input/session_cookie.txt'):
    try:
        with Path(path).open(mode ='r') as file:
            return file.read()
    except FileNotFoundError:
        return None
