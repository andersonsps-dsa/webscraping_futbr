# controllers/LineupController.py
import requests
from typing import List, Dict

class LineupController:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url.rstrip('/')
        self.headers = headers

    def buscar_jogadores_por_partida(self, match_id: int) -> List[Dict]:
        url = f"{self.base_url}/event/{match_id}/lineups"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return []

        data = resp.json()
        lineups = []
        for side in ['home', 'away']:
            team_data = data.get(side, {})
            for p in team_data.get('lineups', []):
                lineup = {
                    'id': p.get('lineup', {}).get('id'),
                    'name': p.get('lineup', {}).get('name'),
                    'team_id': team_data.get('team', {}).get('id'),
                    'position': p.get('lineup', {}).get('position')
                }
                lineups.append(lineup)
        return lineups
