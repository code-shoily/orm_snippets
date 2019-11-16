import datetime
from typing import Dict, Any

from hypothesis import strategies

from .models import Message


def example_message() -> Dict[str, Any]:
    users = [
        'batman', 'superman', 'wonder-woman', 'flash', 'green-lantern', 'martian-manhunter',
        'joker', 'darkseid', 'lex-luthor', 'ananta-jalil', 'zoom', 'savitr', 'mr-mxyzpltk',
        'victor-zsasz', 'hawkgirl', 'guardian', 'super-girl',
    ]
    sender = strategies.sampled_from(users).example()
    recipient = strategies.sampled_from([u for u in users if u != sender]).example()
    when = strategies.dates(min_value=datetime.date(2019, 1, 1),
                            max_value=datetime.date.today()).example()

    return {
        'sender': sender,
        'recipient': recipient,
        'when': when
    }


def seed(limit: int = 1000) -> None:
    for _ in range(limit):
        Message.objects.create(**example_message())