"""
Handles users joining and leaving a table.
"""
from itertools import groupby
from typing import Optional, Dict

from pydantic import BaseModel

from whist.core.error.table_error import PlayerNotJoinedError
from whist.core.scoring.team import Team
from whist.core.user.player import Player
from whist.core.user.status import Status


class UserListEntry(BaseModel):
    """
    Entry class containing the player object and its current status at the table.
    """
    player: Player
    status: Status


class UserList(BaseModel):
    """
    User handler for tables.
    """
    users: Dict[str, UserListEntry] = {}

    def __len__(self):
        return len(self.users)

    @property
    def players(self) -> list[Player]:
        """
        Returns all players at the table.
        :return: players of the table
        :rtype: list[Player]
        """
        users = [user.player for user in self.users.values()]
        return users

    @property
    def ready(self) -> bool:
        """
        Returns if all players are ready.
        :return: Ready or not
        :rtype: boolean
        """
        for player in self.users.values():
            if not player.status.ready:
                return False
        return True

    @property
    def teams(self) -> list[Team]:
        """
        Returns the teams.
        :return: list of teams
        """
        player_by_team: list[list[Player]] = [[entry.player for entry in list(grp)]
                                              for k, grp in groupby(
                list(sorted(self.users.values(), key=lambda x: x.status.team)),
                lambda x: x.status.team)]
        teams: list[Team] = [Team(players=players) for players in player_by_team]
        return teams

    def team(self, player: Player) -> Optional[int]:
        """
        Gets the id of the team for a player.
        :param player: for which the id should be retrieved
        :type player: Player
        :return: Integer if player joined a team or None if not.
        :rtype: int
        """
        status: Status = self._get_status(player)
        return status.team

    def team_size(self, team: int) -> int:
        """
        Gets the size of the team.
        :param team: ID of the team
        :type team: int
        :return: Amount of members
        :rtype: int
        """
        return len([entry for entry in self.users.values() if entry.status.team == team])

    def is_joined(self, player: Player) -> bool:
        """
        Checks if the player is already at the table.
        :param player: to check
        :type player: Player
        :return: True if is member else false
        :rtype: bool
        """
        return player.username in self.users

    def append(self, player: Player):
        """
        Adds a player to the list.
        :param player: player to join
        :type player: Player
        :return: None
        :rtype: None
        """
        if not self.is_joined(player):
            self.users.update({player.username: UserListEntry(player=player, status=Status())})

    def remove(self, player: Player):
        """
        Removes the player from the list.
        :param player: player to leave
        :type player: Player
        :return: None
        :rtype: None
        """
        if self.is_joined(player):
            self.users.pop(player.username)

    def change_team(self, player: Player, team: int) -> None:
        """
        Player changes teams.
        :param player: to change teams
        :type player: Player
        :param team: id of the new team
        :type team: int
        :return: None
        :rtype: None
        """
        status: Status = self._get_status(player)
        status.team = team

    def player_ready(self, player: Player):
        """
        Player says they is ready.
        :param player: player who is ready, must be joined
        :type player: Player
        :return: Raised PlayerNotJoinedError if the player has not yet joined.
        :rtype: None
        """
        if not self.is_joined(player):
            raise PlayerNotJoinedError()
        status: Status = self._get_status(player)
        status.ready = True

    def player_unready(self, player: Player):
        """
        Player says they is not ready.
        :param player: player who is not ready
        :type player: Player
        :return: Raised PlayerNotJoinedError if the player has not yet joined.
        :rtype: None
        """
        if not self.is_joined(player):
            raise PlayerNotJoinedError()
        status: Status = self._get_status(player)
        status.ready = False

    def _get_status(self, player) -> Status:
        return self._get_entry(player).status

    def _get_entry(self, player) -> UserListEntry:
        return self.users[player.username]
