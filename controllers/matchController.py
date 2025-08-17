import requests

class MatchController:
    def __init__(self, base_url, headers, tournament_id, season_id):
        self.base_url = base_url
        self.headers = headers
        self.tournament_id = tournament_id
        self.season_id = season_id

    def _get_json(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            print(f"Erro {response.status_code} ao acessar {url}")
            return None
        return response.json()

    # Pega partidas por rodada do torneio
    def listar_partidas_por_rodada(self, rodada):
        endpoint = f"/unique-tournament/{self.tournament_id}/season/{self.season_id}/events/round/{rodada}"
        data = self._get_json(endpoint)
        return data.get("events", []) if data else []

    # Pega incidentes de uma partida
    def listar_incidentes_partida(self, match_id):
        endpoint = f"/event/{match_id}/incidents"
        return self._get_json(endpoint) or []

    # Pega estatísticas de uma partida
    def listar_estatisticas_partida(self, match_id):
        data = self._get_json(f"/event/{match_id}/statistics")
        if not data or "statistics" not in data:
            return {}

        estatisticas = {}
        for stats in data["statistics"]:
            period = stats.get("period")
            for grupo in stats.get("groups", []):
                for item in grupo.get("statisticsItems", []):
                    key = item.get("key")
                    estatisticas[f"{key}_H_{period}"] = item.get("home", 0)
                    estatisticas[f"{key}_A_{period}"] = item.get("away", 0)
        return estatisticas

    # Consolida tudo por rodada
    def listar_detalhes_rodada(self, rodada):
        partidas = self.listar_partidas_por_rodada(rodada)
        resultados = []

        for partida in partidas:
            match_id = partida["id"]
            estatisticas = self.listar_estatisticas_partida(match_id)
            incidentes = self.listar_incidentes_partida(match_id)

            resultados.append({
                "match_id": match_id,
                "home_team": partida["homeTeam"]["name"],
                "away_team": partida["awayTeam"]["name"],
                "placar": f"{partida['homeScore'].get('current', 0)} x {partida['awayScore'].get('current', 0)}",
                "status": partida.get("status", {}).get("type"),
                "estatisticas": estatisticas,
                "incidentes": incidentes
            })

        return resultados


# ===================== MAIN =====================
"""
if __name__ == "__main__":
    BASE_URL = "https://www.sofascore.com/api/v1"
    HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    TOURNAMENT_ID = 325
    SEASON_ID = 72034
    RODADA = 1  # exemplo

    mc = MatchController(BASE_URL, HEADERS, TOURNAMENT_ID, SEASON_ID)
    detalhes = mc.listar_detalhes_rodada(RODADA)

    for partida in detalhes:
        print(f"{partida['home_team']} x {partida['away_team']} | {partida['placar']}")
        print(f"Estatísticas: {list(partida['estatisticas'].keys())[:5]}...")  # primeiras 5 estatísticas
        print(f"Incidentes: {len(partida['incidentes'])} registrados\n")
"""