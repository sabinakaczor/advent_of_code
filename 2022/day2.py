'''
Symbols meaning:

A for Rock
B for Paper
C for Scissors

X for Loss
Y for Draw
Z for Win
'''

ROCK = 'A'
PAPER = 'B'
SCISSORS = 'C'

LOSS = 'X'
DRAW = 'Y'
WIN = 'Z'

shape_scoring = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}

outcome_scoring = {
    LOSS: 0,
    DRAW: 3,
    WIN: 6,
}

expected_choices = {
    LOSS: {
        ROCK: SCISSORS,
        PAPER: ROCK,
        SCISSORS: PAPER,
    },
    DRAW: {
        ROCK: ROCK,
        PAPER: PAPER,
        SCISSORS: SCISSORS,
    },
    WIN: {
        ROCK: PAPER,
        PAPER: SCISSORS,
        SCISSORS: ROCK,
    },
}


def calculate_round_score(opponent_choice, expected_outcome):
    player_choice = expected_choices[expected_outcome][opponent_choice]
    return shape_scoring[player_choice] + outcome_scoring[expected_outcome]

result = 0;
with open('2022/input2.txt') as f:
    for line in f.readlines():
        line = line.strip()
        [opponent_choice, expected_outcome] = line.split(' ')
        result += calculate_round_score(opponent_choice, expected_outcome)
        
print(result)