# Iterative Prisoners' Dilemma tournament

## Python

For now:

    $ python prisoner.py -1

```
usage: prisoner.py [-h] [--rounds ROUNDS] [--random RANDOM] [--titfortat TITFORTAT] [--eviltitfortat EVILTITFORTAT]
                   [--cooperator COOPERATOR] [--defector DEFECTOR] [--titfortwotats TITFORTWOTATS] [--oneplayer]

Play a tournament of Prisoners Dilemma

optional arguments:
  -h, --help            show this help message and exit
  --rounds ROUNDS       Number of rounds in the tournament
  --random RANDOM, -r RANDOM
                        Number of random players to add to the tournament
  --titfortat TITFORTAT, -t TITFORTAT
                        Number of titfortat players to add to the tournament
  --eviltitfortat EVILTITFORTAT, -e EVILTITFORTAT
                        Number of evil titfortat players to add to the tournament
  --cooperator COOPERATOR, -c COOPERATOR
                        Number of cooperator players to add to the tournament
  --defector DEFECTOR, -d DEFECTOR
                        Number of defector players to add to the tournament
  --titfortwotats TITFORTWOTATS, -2 TITFORTWOTATS
                        Number of titfortwotats players to add to the tournament
  --oneplayer, -1       Add one player of each type to the tournament
```

Modify the code to create new players, etc.

## Clojure

For now:

    $ lein repl
    > (load "prisoner")
    > (tourney 1000 (concat (create-players) (create-players)))

To create a new player:
(1) write the code — use tit-for-tat as an example
(2) add to (create-players) function for ease of access

TODO:

- probably best to fix how deep the history goes back
- add Press/Dyson players
