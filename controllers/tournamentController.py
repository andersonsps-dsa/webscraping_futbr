# controllers/tournamentController.py
import requests
from typing import List, Dict, Optional

class TournamentController:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url.rstrip('/')
        self.headers = headers

    def _get(self, endpoint: str) -> Optional[Dict]:
        """Faz requisição GET e retorna o JSON, tratando erros"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            resp = requests.get(url, headers=self.headers)
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"Erro {resp.status_code} ao acessar {url}")
        except requests.RequestException as e:
            print(f"Erro de requisição: {e}")
        return None

    def listar_partidas_rodada(self, tournament_id: int, season_id: int, rodada: int,
                               nome_campeonato: str, ano: int) -> List[Dict]:
        """Retorna partidas de uma rodada específica com match_id"""
        url_round = f"unique-tournament/{tournament_id}/season/{season_id}/events/round/{rodada}"
        data = self._get(url_round)
        partidas = []

        if not data or 'events' not in data:
            return []  # Se não houver rodada, retorna lista vazia

        for event in data.get('events', []):
            home_score = event.get('homeScore', {}).get('display') or "0"
            away_score = event.get('awayScore', {}).get('display') or "0"

            # Pegando match_id correto
            match_id = event.get('id')

            partidas.append({
                "campeonato": nome_campeonato,
                "ano": ano,
                "match_id": match_id,
                "mandante": event['homeTeam']['name'],
                "visitante": event['awayTeam']['name'],
                "placar": f"{home_score} x {away_score}"
            })

        return partidas

    def listar_todas_rodadas(self, campeonatos: List[Dict]) -> List[Dict]:
        """Retorna todas as partidas de todos os campeonatos e temporadas informadas"""
        todas_partidas = []

        for campeonato in campeonatos:
            nome_campeonato = campeonato['nome']
            for ano, season_id in campeonato['temporadas'].items():
                rodada = 1
                while True:
                    partidas = self.listar_partidas_rodada(
                        campeonato['tournament_id'], season_id, rodada, nome_campeonato, ano
                    )
                    if not partidas:  # Encerra o loop se não houver mais partidas
                        break
                    todas_partidas.extend(partidas)
                    rodada += 1

        return todas_partidas


# -------------------------------
# Código de teste / main comentado
# -------------------------------
# if __name__ == "__main__":
#     headers = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
#     base_url = "https://www.sofascore.com/api/v1"
# 
#     campeonatos = [
#         {"nome": "Brasileirão", "tournament_id": 325, "temporadas": {2025: 72034, 2024: 58766, 2023: 48982}},
#         {"nome": "La Liga", "tournament_id": 8, "temporadas": {2025: 77559, 2024: 61643}},
#         {"nome": "Premier League", "tournament_id": 17, "temporadas": {2025: 76986, 2024: 61627}},
#         {"nome": "Champions League", "tournament_id": 7, "temporadas": {2025: 76953, 2024: 61644}}
#     ]
# 
#     controller = TournamentController(base_url, headers)
#     resultado = controller.listar_todas_rodadas(campeonatos)
#     print(f"Total de partidas encontradas: {len(resultado)}")
