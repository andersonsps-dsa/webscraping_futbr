import pandas as pd
from controllers.roadController import RoadController
from controllers.matchController import MatchController
from controllers.tournamentController import TournamentController

# Configurações gerais
BASE_URL = "https://www.sofascore.com/api/v1"
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}

# Inicializa os controllers
road_controller = RoadController(BASE_URL, HEADERS)
tournament_controller = TournamentController(BASE_URL, HEADERS)

# Exemplo de campeonatos (para TournamentController)
campeonatos = [
    {"nome": "Brasileirão", "tournament_id": 325, "temporadas": {2025: 72034, 2024: 58766, 2023: 48982}},
    {"nome": "La Liga", "tournament_id": 8, "temporadas": {2025: 77559, 2024: 61643}},
    {"nome": "Premier League", "tournament_id": 17, "temporadas": {2025: 76986, 2024: 61627}},
    {"nome": "Champions League", "tournament_id": 7, "temporadas": {2025: 76953, 2024: 61644}}
]

# RoadController e MatchController: percorrer campeonatos e temporadas
all_road_matches = []
all_match_details = []

for campeonato in campeonatos:
    tournament_id = campeonato["tournament_id"]
    for season, season_id in campeonato["temporadas"].items():
        # RoadController
        partidas_road = road_controller.listar_partidas_por_rodada(tournament_id, season_id)
        for partida in partidas_road:
            partida["tournament"] = campeonato["nome"]
            partida["season"] = season
        all_road_matches.extend(partidas_road)

        # MatchController
        match_controller = MatchController(BASE_URL, HEADERS, tournament_id, season_id)
        detalhes_rodada = match_controller.listar_detalhes_rodada(rodada=1)  # exemplo: rodada 1
        for partida in detalhes_rodada:
            row = {
                "tournament": campeonato["nome"],
                "season": season,
                "match_id": partida["match_id"],
                "home_team": partida["home_team"],
                "away_team": partida["away_team"],
                "placar": partida["placar"],
                "status": partida["status"]
            }
            row.update(partida["estatisticas"])
            row["num_incidentes"] = len(partida["incidentes"])
            all_match_details.append(row)

df_road = pd.DataFrame(all_road_matches)
df_match = pd.DataFrame(all_match_details)

# TournamentController: todas as rodadas
partidas_tournament = tournament_controller.listar_todas_rodadas(campeonatos)
df_tournament = pd.DataFrame(partidas_tournament)

# Salvar tudo em um Excel com múltiplas abas
with pd.ExcelWriter("dados_partidas.xlsx", engine="xlsxwriter") as writer:
    df_road.to_excel(writer, sheet_name="RoadController", index=False)
    df_match.to_excel(writer, sheet_name="MatchController", index=False)
    df_tournament.to_excel(writer, sheet_name="TournamentController", index=False)

print("Dados salvos em 'dados_partidas.xlsx'")
