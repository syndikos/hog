"""CS 61A Presents The Game of Hog."""

from dice import four_sided, make_test_dice, six_sided
from ucb import interact, log_current_line, main, trace

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS>0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return the
    number of 1's rolled (capped at 11 - NUM_ROLLS).
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert isinstance(num_rolls, int), 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    outcomes = []
    iterator = num_rolls

    while iterator > 0:
        point = dice()
        outcomes.append(point)
        iterator -= 1
    # print('the dice outcomes list is:', outcomes)
    num_of_1s = outcomes.count(1)
    if num_of_1s == 0:
        return sum(outcomes)
    return min(11-num_rolls, num_of_1s)


def free_bacon(opponent_score):
    """Return the points scored from rolling 0 dice (Free Bacon)."""
    # BEGIN PROBLEM 2
    def split_digits(num):
        """Returns a list contains all the digits in a number.
        >>> split_digits(12)
        [1, 2]
        >>> split_digits(10)
        [1, 0]
        >>> split_digits(7)
        [0, 7]
        """
        assert isinstance(num, int), 'your input must be a integer'
        ans = []
        for i in str(num):
            ans.append(i)
        if len(ans) < 2:
            ans.append('0')
        return ans
    digits = split_digits(opponent_score)
    # print('splited number in free_bacon:', digits)
    ans = 1 + int(max(digits))
    return ans


    # END PROBLEM 2


def square(x):
    return x*x

def is_prime(x):
    """assumes x is a integer, 
    if x is a prime number,returns True, else
    returns False

    >>> is_prime(47)
    True

    >>> is_prime(2)
    True

    >>> is_prime(1)
    False

    >>> is_prime(0)
    False
    """

    assert isinstance(x, int), "the number  is not an integer"
    assert x >= 0, "the number is negative"

    if x < 2:
        return False
    if x == 2:
        return True

    for i in range(2, x):
        if square(i) > x:
            return True
        elif x % i == 0:
            return False
def next_prime(num):
    """Returns the first prime after num"""
    ans = num + 1
    if is_prime(ans):
        return ans
    return next_prime(num + 1)

def hogtimus(score):
    """If score is a prime, returns
    the next prime"""
    if is_prime(score):
        return next_prime(score)
    return score

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free Bacon).
    Return the points scored for the turn by the current player. Also
    implements the Hogtimus Prime rule.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    # Leave these assert statements here; they help check for errors.
    assert isinstance(num_rolls, int), 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN PROBLEM 2



    def first_step(num_rolls, opponent_score, dice=six_sided):
        """Returns score without hogtimus"""
        if num_rolls == 0:
            score = free_bacon(opponent_score)
            # return score
        else:
            score = roll_dice(num_rolls, dice)
        return score

    ans = first_step(num_rolls, opponent_score, dice)
    # print('ans before hogtimus is:', ans)
    ans = hogtimus(ans)
    # print('ans after hogtimus:', ans)
    return ans
    # END PROBLEM 2

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog Wild).
    """
    # BEGIN PROBLEM 3
    dice = six_sided
    if (score + opponent_score) % 7 == 0:
        dice = four_sided
    return dice
    # END PROBLEM 3

def is_swap(score0, score1):
    """Returns whether one of the scores is double the other.
    """
    # BEGIN PROBLEM 4
    if (score0 == 0) or (score1 == 0):
        return False
    elif (score0 / score1 == 2.0) or (score1 / score0 == 2.0):
        return True
    return False
    # END PROBLEM 4

def other(player):
    """Return the other player, for a player PLAYER numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - player


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    player = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    def the_strategy(player):
        """Returns strategy of current player"""
        if player == 0:
            return strategy0
        return strategy1

    def the_num_rolls(strategy, score0, score1):
        """Returns num_rolls of current player"""
        if strategy == strategy0:
            return strategy0(score0, score1)
        return strategy1(score1, score0)

    def the_opponent_score(player, score0, score1):
        """Returns opponent_score"""
        if player == 0:
            return score1
        return score0

    def the_play(score0, score1, player):
        """Returns score0 , score1 after one turn"""
        strategy = the_strategy(player)
        # print(strategy)
        num_rolls = the_num_rolls(strategy, score0, score1)
        # print('num_rolls is:',num_rolls)
        opponent_score = the_opponent_score(player, score0, score1)
        # print('opponent_score is:', opponent_score)
        dice = select_dice(score0, score1)
        # if player == 0:
        delta = take_turn(num_rolls, opponent_score, dice)
        # print('delta is:', delta)
        if player == 0:
            score0 += delta
        else:
            score1 += delta
        if is_swap(score0, score1):
            score0, score1 = score1, score0
        # print('score0 is:',score0)
        # print('score1 is:',score1)
        # print('**********')
        if (score0 >= goal) or (score1 >= goal):
            return score0, score1
        player = other(player)
        # print('player is:',player)
        return the_play(score0, score1, player)
    score0, score1 = the_play(score0, score1, player)
    return score0, score1

    # END PROBLEM 5


#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def check_strategy_roll(score, opponent_score, num_rolls):
    """Raises an error with a helpful message if NUM_ROLLS is an invalid
    strategy output. All strategy outputs must be integers from -1 to 10.

    >>> check_strategy_roll(10, 20, num_rolls=100)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(10, 20) returned 100 (invalid number of rolls)

    >>> check_strategy_roll(20, 10, num_rolls=0.1)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(20, 10) returned 0.1 (not an integer)

    >>> check_strategy_roll(0, 0, num_rolls=None)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(0, 0) returned None (not an integer)
    """
    msg = 'strategy({}, {}) returned {}'.format(
        score, opponent_score, num_rolls)
    assert isinstance(num_rolls, int), msg + ' (not an integer)'
    assert 0 <= num_rolls <= 10, msg + ' (invalid number of rolls)'


def check_strategy(strategy, goal=GOAL_SCORE):
    """Checks the strategy with all valid inputs and verifies that the
    strategy returns a valid input. Use `check_strategy_roll` to raise
    an error with a helpful message if the strategy returns an invalid
    output.

    >>> def fail_15_20(score, opponent_score):
    ...     if score != 15 or opponent_score != 20:
    ...         return 5
    ...
    >>> check_strategy(fail_15_20)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(15, 20) returned None (not an integer)
    >>> def fail_102_115(score, opponent_score):
    ...     if score == 102 and opponent_score == 115:
    ...         return 100
    ...     return 5
    ...
    >>> check_strategy(fail_102_115)
    >>> fail_102_115 == check_strategy(fail_102_115, 120)
    Traceback (most recent call last):
     ...
    AssertionError: strategy(102, 115) returned 100 (invalid number of rolls)
    """
    # BEGIN PROBLEM 6
    for score in range(0, goal):
        for opponent_score in range(0, goal):
            num_rolls = strategy(score, opponent_score)
            check_strategy_roll(score, opponent_score, num_rolls)
    # END PROBLEM 6


# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    """
    # BEGIN PROBLEM 7
    # def the_fn(*args):
    #     result = fn(*args)
    #     return result
    
    def averaged(*args):
        total = 0
        num = num_samples
        while num > 0:
            point = fn(*args)
            total += point
            num -= 1
        average = total / num_samples
        return average
    return averaged
    # END PROBLEM 7


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN PROBLEM 8
    scores = []
    numbers_of_dice = []
    average_dice = make_averaged(roll_dice, num_samples)
    for number_of_dice in range(1, 11):
        # sum_of_score = 0
        # num = number_of_dice
        # while num > 0:
        score = average_dice(number_of_dice, dice)
            # sum_of_score += score
            # num -= 1
        scores.append(score)
        numbers_of_dice.append(number_of_dice)
    biggest_score = max(scores)
    the_index = scores.index(biggest_score)
    ans = numbers_of_dice[the_index]
    return ans

    # END PROBLEM 8


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(4)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def free_bacon_timus(opponent_score):
     ans = free_bacon(opponent_score)
     ans = hogtimus(ans)
     return ans



def bacon_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 9
    ans = free_bacon_timus(opponent_score)
   
    # ans = hogtimus
    if ans >= margin:
        return 0
    return num_rolls
    # return 4  # Replace this statement
    # END PROBLEM 9
check_strategy(bacon_strategy)


def swap_strategy(score, opponent_score, margin=8, num_rolls=4):
    """This strategy rolls 0 dice when it triggers a beneficial swap. It also
    rolls 0 dice if it gives at least MARGIN points. Otherwise, it rolls
    NUM_ROLLS.
    """
    # BEGIN PROBLEM 10
    delta = free_bacon_timus(opponent_score)
    new_score = score + delta
    if is_swap(new_score, opponent_score) and (new_score < opponent_score):
        return 0
    elif delta >= margin:
        return 0
    return num_rolls

    # END PROBLEM 10
check_strategy(swap_strategy)


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 11
    "*** REPLACE THIS LINE ***"
    return 4  # Replace this statement
    # END PROBLEM 11
check_strategy(final_strategy)


##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.

@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
