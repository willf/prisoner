prisoner
========

Iterative Prisoners' Dilemma tournament (Clojure)

For now:

    $ lein repl
    > (load "prisoner")
    > (tourney 1000 (concat (create-players) (create-players)))

To create a new player:
(1) write the code — use tit-for-tat as an example
(2) add to (create-players) function for ease of access

TODO:

- probably best to fix how deep the history goes back
- add the new Penrose random players