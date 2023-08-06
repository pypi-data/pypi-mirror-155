import os
from dataclasses import dataclass
from typing import Any

from requests import Response

from betsapi3.base_client import BaseAPIClient
from betsapi3.utils import Endpoint, UrlParameter, api_endpoint


@dataclass(slots=True)
class Bet365API(BaseAPIClient):
    _endpoints = {
        'in_play': Endpoint(
            'inplay', 1, 'bet365',
            {
                'raw': UrlParameter(int)
            }
        ),
        'in_play_filter': Endpoint(
            'inplay_filter', 1, 'bet365',
            {
                'sport_id': UrlParameter(int),
                'league_id': UrlParameter(str),
                'skip_esports': UrlParameter(int)
            }
        ),
        'in_play_event': Endpoint(
            'event', 1, 'bet365',
            {
                'FI': UrlParameter(str, True),
                'stats': UrlParameter(Any),
                'lineup': UrlParameter(Any),
                'raw': UrlParameter(int)
            }
        ),
        'pre_match_odds': Endpoint(
            'prematch', 3, 'bet365',
            {
                'FI': UrlParameter(str, True),
                'raw': UrlParameter(int)
            }
        ),
        'upcoming': Endpoint(
            'upcoming', 1, 'bet365',
            {
                'sport_id': UrlParameter(int, True),
                'league_id': UrlParameter(str),
                'skip_esports': UrlParameter(int),
                'day': UrlParameter(str),
                'page': UrlParameter(int)
            }
        )
    }

    @api_endpoint
    def in_play(self, raw: int | None = None) -> Response:
        pass

    @api_endpoint
    def in_play_filter(self, sport_id: int | None = None, league_id: str | None = None,
                       skip_esports: int | None = None) -> Response:
        pass

    @api_endpoint
    def in_play_event(self, FI: int, stats: Any = None, lineup: Any = None,
                      raw: int | None = None) -> Response:
        pass

    @api_endpoint
    def upcoming(self, sport_id: int, league_id: str | None = None,
                 skip_esports: int | None = None, day: str | None = None, page: int | None = None) -> Response:
        pass

    @api_endpoint
    def pre_match_odds(self, FI: str, raw: int | None = None) -> Response:
        pass

    @api_endpoint
    def result(self, event_id: str, raw: int | None = None) -> Response:
        pass


if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()

    client = Bet365API(os.environ.get('BETS_API_KEY'))

    client.in_play()
    print(client.upcoming(1, skip_esports=1).json())
