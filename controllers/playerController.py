# controllers/playerController.py
import requests
from typing import Dict

class PlayerController:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url.rstrip('/')
        self.headers = headers

    def get_info(self, player_id: int) -> Dict:
        url = f"{self.base_url}/player/{player_id}"
        resp = requests.get(url, headers=self.headers)
        return resp.json() if resp.status_code == 200 else {}

    def get_stats_overall(self, player_id: int) -> Dict:
        # Estatísticas gerais (all season)
        url = f"{self.base_url}/player/{player_id}/statistics/overall"
        resp = requests.get(url, headers=self.headers)
        return resp.json() if resp.status_code == 200 else {}

    def get_stats_by_season(self, player_id: int, tournament_id: int, season_id: int) -> Dict:
        url = f"{self.base_url}/player/{player_id}/unique-tournament/{tournament_id}/season/{season_id}/statistics/overall"
        resp = requests.get(url, headers=self.headers)
        return resp.json() if resp.status_code == 200 else {}
