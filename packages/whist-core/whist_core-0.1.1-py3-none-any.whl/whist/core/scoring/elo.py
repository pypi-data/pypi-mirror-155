"""
Elo Rating Calculator
"""
from whist.core.scoring.score_card import ScoreCard
from whist.core.scoring.team import Team
from whist.core.user.player import Player


# pylint: disable=too-few-public-methods
class EloRater:
    """
    Static class that calculates the Elo-Rating for players after several hands played.
    """

    @staticmethod
    def rate(teams: list[Team], scores: ScoreCard) -> None:
        """
        Calculates the new rating of player after several hand played.
        :param teams:
        :type teams:
        :param scores:
        :type scores:
        :return:
        :rtype:
        """
        delta = EloRater._score_delta(teams[0], teams[1], scores)
        for team in teams:
            for player in team.players:
                k_factor = EloRater._k_factor(player)
                won = scores.won(team)
                player.rating += round(k_factor * delta * won)

    @staticmethod
    def _k_factor(player: Player) -> int:
        if player.rating > 2400 and player.games > 30:
            return 10
        if player.rating < 2300 and player.games < 30:
            return 40
        return 20

    @staticmethod
    def _score_delta(team: Team, opponent: Team, scores: ScoreCard) -> float:
        num_games = len(scores)
        num_wins = scores.score(team)
        expected_score = EloRater._expected_score(team, opponent)
        return num_wins - num_games * expected_score

    @staticmethod
    def _expected_score(team: Team, opponent: Team) -> float:
        q_a = EloRater._team_quotient(team)
        q_b = EloRater._team_quotient(opponent)

        return q_a / (q_a + q_b)

    @staticmethod
    def _team_quotient(team: Team):
        return 10 ** (team.rating / 400)
