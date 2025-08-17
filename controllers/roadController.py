import requests

class RoadController:
    def __init__(self, base_url, headers):
        self.base_url = base_url
        self.headers = headers

    def _get_json(self, endpoint):
        """Faz a requisição GET e retorna JSON, ou None se der erro."""
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Erro ao acessar {url}: {e}")
            return None

    def listar_partidas_por_rodada(self, tournament_id, season_id):
        """Retorna todas as partidas de um torneio/temporada com estatísticas básicas."""
        endpoint = f"/unique-tournament/{tournament_id}/season/{season_id}/events"
        dados = self._get_json(endpoint)
        if not dados or "events" not in dados:
            return []

        jogos = []
        for evento in dados["events"]:
            try:
                home = evento.get("homeTeam", {})
                away = evento.get("awayTeam", {})
                score_home = evento.get("homeScore", {}).get("current", 0)
                score_away = evento.get("awayScore", {}).get("current", 0)
                stats = evento.get("statistics", {})

                jogo = {
                    "id_jogo": evento.get("id"),
                    "tempo_seg": evento.get("time", {}).get("currentPeriodStartTimestamp"),
                    "Rodada": evento.get("round", {}).get("round"),
                    "Status_Jogo": evento.get("status", {}).get("description"),
                    "Team_H": home.get("name"),
                    "Team_H_ID": home.get("id"),
                    "Gols_H_ALL": score_home,
                    "Team_A": away.get("name"),
                    "Team_A_ID": away.get("id"),
                    "Gols_A_ALL": score_away,
                    # Estatísticas detalhadas
                    "Finalizacoes_H_ALL": stats.get("shotsOnTarget", {}).get("home", 0),
                    "Finalizacoes_A_ALL": stats.get("shotsOnTarget", {}).get("away", 0),
                    "Cantos_H_ALL": stats.get("corners", {}).get("home", 0),
                    "Cantos_A_ALL": stats.get("corners", {}).get("away", 0),
                    "Faltas_H_ALL": stats.get("fouls", {}).get("home", 0),
                    "Faltas_A_ALL": stats.get("fouls", {}).get("away", 0),
                    "YELLOWCard_H_ALL": stats.get("yellowCards", {}).get("home", 0),
                    "YELLOWCard_A_ALL": stats.get("yellowCards", {}).get("away", 0),
                    "REDCard_H_ALL": stats.get("redCards", {}).get("home", 0),
                    "REDCard_A_ALL": stats.get("redCards", {}).get("away", 0),
                }
                jogos.append(jogo)
            except Exception as e:
                print(f"Erro ao processar jogo {evento.get('id')}: {e}")
                continue

        return jogos


# ===================== TESTE =====================
"""
if __name__ == "__main__":
    BASE_URL = "https://www.sofascore.com/api/v1"
    HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

    rc = RoadController(BASE_URL, HEADERS)
    partidas = rc.listar_partidas_por_rodada(325, 72034)  # Exemplo
    print(f"Total de partidas: {len(partidas)}")
    print(partidas[0] if partidas else "Nenhuma partida encontrada")
"""
