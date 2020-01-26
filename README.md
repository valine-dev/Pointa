# Welcome to "Pointa!" Project!

<h2 id="Summary">Summary</h2>
"Pointa!" is a board game which is simple to learn & enjoy. Meanwhile you can also play the game with pen and paper, but this repository is meant to implement the game in python as back-end.

* [Game Side](#Game)
* [Program Side](#Program)

---

<h2 id="Game">Game Side</h2>

### Game Instruction
1. **Preparation**
    - To play Pointa, you need two players, a pen, a piece of paper and a twelve-sided dice or two six-sided dice.

2. **Values**
    - Player Properties
        - HP: Player's health point, starts with 100, and should not exceed 100.
        - PT: Player's points, can be fetched by the player from what player rolled at the 1st phase in a round.
        - DEF: Player's defense value, can be fetched by the player from a "def" action, clear when the round which player fetch the value end.
    - Actions
        - ATK/DEF/HEL: Action value of Attack/Defense/Heal.

3. **Game Process**
    1. **Phase 1**
        - For each player, 1d12 or 2d6. The result should be added into the player's PT value.
    2. **Phase 2**
        - Each Player distribute the PT into three Actions (ATK/DEF/HEL). Then players show their result at the same time, which is settled in the current round.
    3. **Phase 3**
        - Step 1: Sorting
            - Take out every actions except the actions which did't get any PT, sort them by the order of less PT to more PT.
        - Step 2: Executing
            - Execute the action from beginning to end by the rule in the table below ('x' as the PT the action used) :
            >|Action|Process|
            >|:----:|:----:|
            >|atk|Executor must do another 1d12 or 2d6 to determine the coefficient "a" effects the final damage. When the result is **1-5, a=0.5**. **6-11 is 1.0**. **12 is 1.5**.  So the final damage to target's HP should be **a(0.3x^2) - target's DEF**(Rounded up as result) (take negative number result as 0), and target's DEF should minus the a(0.3x^2) (take negative number result as 0 too) |
            >|def|Add **0.25x^2**(Rounded up as the result) to Executor's DEF value.|
            >|hel|Add **0.35x^2**(Rounded up as the result) to Executor's HP value but can't break the limit of 100.|
        - Step 3: Settling
	        - If any player's HP goes to 0 or below 0, the player dies. If a player was killed in the round, the player loses. But if both of the players dead, the one who has the largest absolute value of HP loses. If no one dies, continue to next round.

