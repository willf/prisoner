from itertools import combinations
import random

## Implement a Prisoner's Dilemma tournament


## Scoring and judging:

# Payoff matrix      Player A
#                  coop  defect
# Player B coop   (3,3)  (0,5)
#          defect (5,0)  (1,1)


# Define the payoff matrix


class Player:
    def __init__(self, name="Player"):
        self.name = name
        self.memory = {}

    def cooperate(self):
        return PrisonersDilemmaTourney.COOPERATION

    def defect(self):
        return PrisonersDilemmaTourney.DEFECTION

    def move(self, opponent):
        return self.defect()

    def observe(self, opponent, move):
        if self.memory.get((opponent, move)) is None:
            self.memory[opponent] = []
        self.memory[opponent].append(move)

    def remember(self, opponent):
        return self.memory.get(opponent, [])


class Defector(Player):
    def __init__(self, name="Defector"):
        super().__init__(name)

    def move(self, opponent):
        return self.defect()


class Cooperator(Player):
    def __init__(self, name="Cooperator"):
        super().__init__(name)

    def move(self, opponent):
        return self.cooperate()


class RandomPlayer(Player):
    def __init__(self, name="RandomPlayer"):
        super().__init__(name)

    def move(self, opponent):
        if random.randint(0, 1) == 0:
            return self.defect()
        else:
            return self.cooperate()


class TitForTatPlayer(Player):
    def __init__(self, name="TitForTatPlayer"):
        super().__init__(name)

    def move(self, opponent):
        memory = self.remember(opponent)
        if len(memory) == 0:
            return self.cooperate()
        else:
            return memory[-1]


class TitForTwoTatsPlayer(Player):
    def __init__(self, name="TitForTwoTatsPlayer"):
        super().__init__(name)

    def move(self, opponent):
        memory = self.remember(opponent)
        if len(memory) <= 1:
            return self.cooperate()
        else:
            last_two = memory[-2:]
            if last_two[0] == last_two[1] and last_two[0] == self.defect():
                return self.defect()
            else:
                return self.cooperate()


class EvilTitForTatPlayer(Player):
    def __init__(self, name="EvilTitForTatPlayer"):
        super().__init__(name)

    def move(self, opponent):
        memory = self.remember(opponent)
        if len(memory) == 0:
            return self.cooperate()
        else:
            last = memory[-1]
            if last == self.defect():
                return self.cooperate()
            else:
                return self.defect()


class PrisonersDilemmaTourney:
    COOPERATION = 0
    DEFECTION = 1

    def __init__(self, players=[]):
        self.matrix = [[(3, 3), (0, 5)], [(5, 0), (1, 1)]]
        self.players = players
        self.scoreboard = {}
        for player in players:
            self.scoreboard[player] = 0
        self.previous_moves = {}
        for player in players:
            self.previous_moves[player] = []

    def payout(self, moveA: int, moveB: int):
        """Returns the payoff for the two moves
        >>> p = PrisonersDilemmaTourney()
        >>> p.payout(p.COOPERATION, p.COOPERATION)
        (3, 3)
        >>> p.payout(p.COOPERATION, p.DEFECTION)
        (0, 5)
        >>> p.payout(p.DEFECTION, p.COOPERATION)
        (5, 0)
        >>> p.payout(p.DEFECTION, p.DEFECTION)
        (1, 1)
        """
        if moveA not in [self.COOPERATION, self.DEFECTION]:
            raise ValueError("Move must be either COOPERATION or DEFECTION")
        if moveB not in [self.COOPERATION, self.DEFECTION]:
            raise ValueError("Move must be either COOPERATION or DEFECTION")
        return self.matrix[moveA][moveB]

    def play(self, playerA: Player, playerB: Player):
        """Play a game and update the players' scores
        >>> p = PrisonersDilemmaTourney([Player(), Player()])
        >>> p.play(p.players[0], p.players[1])
        ((1, 1), (1, 1))
        >>> p.scoreboard[p.players[0]]
        1
        >>> p.scoreboard[p.players[1]]
        1
        >>> p.previous_moves[p.players[0]]
        [1]
        >>> p.previous_moves[p.players[1]]
        [1]
        """
        moveA = playerA.move(playerB)
        moveB = playerB.move(playerA)
        scoreA, scoreB = self.payout(moveA, moveB)
        self.scoreboard[playerA] += scoreA
        self.scoreboard[playerB] += scoreB
        self.previous_moves[playerA].append(moveA)
        self.previous_moves[playerB].append(moveB)
        playerA.observe(playerB, moveB)
        playerB.observe(playerA, moveA)
        return ((moveA, scoreA), (moveB, scoreB))

    def play_round(self):
        for playerA, playerB in combinations(self.players, 2):
            self.play(playerA, playerB)

    def play_tournament(self, n_rounds=10):
        for i in range(n_rounds):
            self.play_round()

    def print_scoreboard(self):
        for i, player in enumerate(
            sorted(self.players, key=lambda x: self.scoreboard[x], reverse=True)
        ):
            print(f"{i+1:2}: {player.name}: {self.scoreboard[player]}")


if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description="Play a tournament of Prisoners Dilemma"
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=100,
        help="Number of rounds in the tournament",
    )
    parser.add_argument(
        "--random",
        "-r",
        type=int,
        default=0,
        help="Number of random players to add to the tournament",
    )

    parser.add_argument(
        "--titfortat",
        "-t",
        type=int,
        default=0,
        help="Number of titfortat players to add to the tournament",
    )

    parser.add_argument(
        "--eviltitfortat",
        "-e",
        type=int,
        default=0,
        help="Number of evil titfortat players to add to the tournament",
    )

    parser.add_argument(
        "--cooperator",
        "-c",
        type=int,
        default=0,
        help="Number of cooperator players to add to the tournament",
    )

    parser.add_argument(
        "--defector",
        "-d",
        type=int,
        default=0,
        help="Number of defector players to add to the tournament",
    )

    parser.add_argument(
        "--titfortwotats",
        "-2",
        type=int,
        default=0,
        help="Number of titfortwotats players to add to the tournament",
    )

    parser.add_argument(
        "--oneplayer",
        "-1",
        action="store_true",
        default=False,
        help="Add one player of each type to the tournament",
    )

    args = parser.parse_args()

    players = []

    tournament = PrisonersDilemmaTourney(players)
    tournament.play_tournament(args.rounds)
    tournament.print_scoreboard()

    args = parser.parse_args()

    players = []
    if args.random:
        for i in range(args.random):
            players.append(RandomPlayer(name=f"RandomPlayer {i+1}"))

    if args.titfortat:
        for i in range(args.titfortat):
            players.append(TitForTatPlayer(name=f"TitForTatPlayer {i+1}"))

    if args.eviltitfortat:
        for i in range(args.eviltitfortat):
            players.append(EvilTitForTatPlayer(name=f"EvilTitForTatPlayer {i+1}"))

    if args.cooperator:
        for i in range(args.cooperator):
            players.append(Cooperator(name=f"Cooperator {i+1}"))

    if args.defector:
        for i in range(args.defector):
            players.append(Defector(name=f"Defector {i+1}"))

    if args.titfortwotats:
        for i in range(args.titfortwotats):
            players.append(TitForTwoTatsPlayer(name=f"TitForTwoTatsPlayer {i+1}"))

    if args.oneplayer:
        players.append(RandomPlayer())
        players.append(TitForTatPlayer())
        players.append(EvilTitForTatPlayer())
        players.append(Cooperator())
        players.append(Defector())
        players.append(TitForTwoTatsPlayer())

    p = PrisonersDilemmaTourney(players=players)
    rounds = args.rounds
    p.play_tournament(n_rounds=rounds)
    print(f"After {rounds} rounds, the scores are:")
    p.print_scoreboard()
