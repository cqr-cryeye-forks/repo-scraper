from functools import reduce
from typing import Optional

from pydantic import BaseModel, Field

from repo_scraper.constants.result import *

dic = {
    BIG_FILE: WARNING,
    NOT_PLAIN_TEXT: WARNING,
    MATCH: ALERT,
    NOT_MATCH: NOTHING,
    FILETYPE_NOT_ALLOWED: WARNING,
    MISSED_FILE: ERROR,
}


class Result(BaseModel):
    identifier: str = Field(default_factory=str)
    reason: str = Field(default_factory=str)
    matches: Optional[list[str]] = Field(default_factory=list)
    result_type: str = Field(default_factory=str)
    comments: Optional[list[str]] = Field(default_factory=list)

    def __init__(self, identifier, reason, matches=None, comments=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.identifier = identifier
        self.reason = reason
        self.matches = matches
        self.result_type = dic[reason]
        self.comments = comments

    def __str__(self):
        # Message to print for matches is originally No matches, unless
        # self.matches has some values
        matches_print = 'No matches to show'
        if self.matches:
            # Create list of string with 'index. content' format for each match
            matches_print = [f'{str(idx + 1)}. {content}' for idx, content in enumerate(self.matches)]

            # Join list
            matches_print = reduce(lambda x, y: x + '\n' + y, matches_print)

        return f'{self.result_type} - {self.reason} in {self.identifier}\n{matches_print}\n'


class Results(BaseModel):
    results: list[Result] = Field(default_factory=list)
