import requests
from bs4 import BeautifulSoup
from collections import defaultdict
from typing import Union
from . import session_cookie as SC


# Get your session cookie to retrieve the correct input!

# Go to any AoC input link > `Inspect` > `Network` tab > Refresh the page > Find `Cookie` header > Copy the text after `session=` :)

class Puzzle:
    def __init__(
        self,
        year: Union[int, str],
        day: Union[int, str],
        session_cookie=SC.get_session_cookie(),
    ):

        msgdy = "int or str only pls"
        msgsc = "str only pls"
        assert isinstance(year, int) or isinstance(year, str), msgdy
        assert isinstance(day, int) or isinstance(day, str), msgdy
        assert isinstance(session_cookie, str), msgsc

        self.year = str(year)
        self.day = str(day).lstrip("0")
        self.session_cookie = session_cookie
        self.submission = defaultdict(list)

    def load_input(self):
        r = requests.get(
            f"https://adventofcode.com/{self.year}/day/{self.day}/input",
            cookies={"session": self.session_cookie},
        )
        inp = r.text.split("\n")
        return inp[:-1] if not inp[-1] else inp

    def submit(self, part: Union[int, str], answer: Union[int, str]):
        msg = "int or str only pls"
        assert isinstance(part, int) or isinstance(part, str), msg
        assert isinstance(answer, int) or isinstance(answer, str), msg
        part = str(part)
        answer = str(answer)
        self.submission[part].append(answer)

        r = requests.post(
            f"https://adventofcode.com/{self.year}/day/{self.day}/answer",
            data={"level": part, "answer": answer},
            cookies={"session": self.session_cookie},
        )
        response = BeautifulSoup(r.text, 'html.parser').article.stripped_strings
        print(" ".join(list(response)).replace("  ", " "))
