;; scoring and judging

;; Payoff matrix      Player A
;;                  coop  defect
;; Player B coop   (3,3)  (0,5)
;;          defect (5,0)  (1,1)

;; score a game 
(defn score [a b]
  (let [p [a b]]
    (cond 
      (= p [:coop :coop])   [3,3]
      (= p [:coop :defect]) [0,5]
      (= p [:defect :coop]) [5,0]
      (= p [:defect :defect]) [1,1]
      :else [0 0])))

;; play one game, returns updated [scores games] table
(defn play [scores games a-b]
  ;; (println "Playing")
  (let [a (a-b 0)
        b (a-b 1)
        a-name (a :name)
        b-name (b :name)
        name-key [a-name b-name]
        ;; api: 'play' will get a seq of [me other] pairs
        a-previous-games (or (games name-key) [])
        ;; api: 'play' will get a seq of [me other] pairs - so reverse
        b-previous-games (map #(reverse %) a-previous-games)
        a-turn (a :play a-previous-games)
        b-turn (b :play b-previous-games)
        payoff (score a-turn b-turn)
        a-payoff (payoff 0)
        b-payoff (payoff 1)]
        ;; (println a-name a-turn "and" b-name b-turn)
        [(merge-with + scores {a-name a-payoff}, {b-name b-payoff})
         (merge-with concat games {name-key [[a-turn b-turn]]})]))

;; Play one round of all against all 
(defn round [scores games player-pairs]
  (cond
    (empty? player-pairs) [scores games]
    :else 
      (let [[new-scores new-games] (play scores games (first player-pairs))]
        ;(println new-scores)
        ;(println new-games)
        (round new-scores new-games (rest player-pairs)))))

;; helper function
(defn tourney* [remaining scores games player-pairs]
  (cond
    (<= remaining 0) scores
    :else
      (let [[new-scores new-games] (round scores games player-pairs)]
        (tourney* (dec remaining) new-scores new-games player-pairs))))

;; all pairs -- including self-pairs
(defn all-pairs [coll]
  (for [i (range (count coll))
        j (range (inc i) (count coll))]
    [(nth coll i) (nth coll j)]))

(defn tourney [rounds players]
  (let [player-pairs (all-pairs players)]
    (tourney* rounds {} {} player-pairs)))

;; this is the history of the other player
(defn opponent-history [state]
  (map #(last %) state))

;; players

;; Always cooperate
(defn cooperator [state] :coop)

;; Always defect
(defn defector [state] :defect)

;; Randomly choose
(defn gaussian [state] (if (= (rand-int 2) 0) :coop :defect))

;; Tit for tat — cooperate at first, then mirror other
(defn tit-for-tat [state]
  (let [l (first state)]
    (if (nil? l) 
      :coop
      (let [other-play (last (opponent-history state))]
        (if (= other-play :coop) :coop :defect)))))

;; Evil tit for tat — cooperate at first, then do opposite
(defn evil-tit-for-tat [msg & [state]]
  (let [l (first state)]
    (if (nil? l) 
      :coop
      (let [other-play (last (opponent-history state))]
        (if (= other-play :coop) :defect :coop)))))

;; return a function that responds to :name and :play
;; messages
(defn create-player [name function]
  (fn [msg & [state]]
    (cond
      (= msg :name) name
      (= msg :play) (function state))))

;; create all kinds of players
(defn create-players []
  [(create-player (gensym "Coop-") cooperator)
   (create-player (gensym "Def-") defector)
   (create-player (gensym "Rand-") gaussian)
   (create-player (gensym "TfT-") tit-for-tat)
   (create-player (gensym "EvilTfT-") evil-tit-for-tat)
   ])

;; (tourney 100 (concat (create-players) (create-players)))


