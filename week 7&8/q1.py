import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging
import time


logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}
utilities = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        if self.history is None:
            total_num_moves = 0
        else:
            total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def is_win(self):
        # check if the board position is a win for either players
        # Feel free to implement this in anyway if needed
        board = self.get_board()
        if board[0] == board[1] == board[2] == 'x':
            return 'x'
        if board[3] == board[4] == board[5] == 'x':
            return 'x'
        if board[6] == board[7] == board[8] == 'x':
            return 'x'
        if board[0] == board[3] == board[6] == 'x':
            return 'x'
        if board[1] == board[4] == board[7] == 'x':
            return 'x'
        if board[2] == board[5] == board[8] == 'x':
            return 'x'
        if board[0] == board[4] == board[8] == 'x':
            return 'x'
        if board[2] == board[4] == board[6] == 'x':
            return 'x'
        if board[0] == board[1] == board[2] == 'o':
            return 'o'
        if board[3] == board[4] == board[5] == 'o':
            return 'o'
        if board[6] == board[7] == board[8] == 'o':
            return 'o'
        if board[0] == board[3] == board[6] == 'o':
            return 'o'
        if board[1] == board[4] == board[7] == 'o':
            return 'o'
        if board[2] == board[5] == board[8] == 'o':
            return 'o'
        if board[0] == board[4] == board[8] == 'o':
            return 'o'
        if board[2] == board[4] == board[6] == 'o':
            return 'o'
        return None

    def is_draw(self):
        # check if the board position is a draw
        # Feel free to implement this in anyway if needed
        # print(self.get_board())
        if ('0' not in self.get_board()) and (self.is_win() is None):
            return True
        return False

    def get_valid_actions(self):
        # get the empty squares from the board
        # Feel free to implement this in anyway if needed
        valid_actions = []
        for i in range(9):
            if i not in self.history:
                valid_actions.append(i)
        return valid_actions

    def is_terminal_history(self):
        # check if the history is a terminal history
        # Feel free to implement this in anyway if needed
        # print(f'{self.history} Is_win: {self.is_win()} Is_draw: {self.is_draw()}')
        if self.is_win() is not None or self.is_draw():
            self.get_utility_given_terminal_history()
            return True
        return False

    def get_utility_given_terminal_history(self):
        # Feel free to implement this in anyway if needed
        global utilities
        if self.is_win() == 'x':
            utilities[self.get_board_string()] = (1, None)
            return 1
        elif self.is_win() == 'o':
            utilities[self.get_board_string()] = (-1, None)
            return -1
        elif self.is_draw():
            utilities[self.get_board_string()] = (0, None)
            return 0
        return  
        
    def update_history(self, action):
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        # Feel free to implement this in anyway if needed
        new_history = History()
        new_history.history = copy.deepcopy(self.history)
        new_history.history.append(action)
        return new_history
    
    def get_board_string(self):
        return ''.join(self.get_board())
    
    def __str__(self):
        hiSTRy = ''
        for element in self.history:
            hiSTRy += str(element)
        return hiSTRy
    
def get_dict(action):
    prob_dist = dict()
    for i in range(9):
        prob_dist[str(i)] = int(action == i)
    return prob_dist

def backward_induction(history_obj):
    """
    :param history_obj: Histroy class object
    :return: best achievable utility (float) for th current history_obj
    """
    global strategy_dict_x, strategy_dict_o
    # TODO implement
    # (1) Implement backward induction for tictactoe
    # (2) Update the global variables strategy_dict_x or strategy_dict_o which are a mapping from histories to
    # probability distribution over actions.
    # (2a)These are dictionary with keys as string representation of the history list e.g. if the history list of the
    # history_obj is [0, 4, 2, 5], then the key is "0425". Each value is in turn a dictionary with keys as actions 0-8
    # (str "0", "1", ..., "8") and each value of this dictionary is a float (representing the probability of
    # choosing that action). Example: {”0452”: {”0”: 0, ”1”: 0, ”2”: 0, ”3”: 0, ”4”: 0, ”5”: 0, ”6”: 1, ”7”: 0, ”8”:
    # 0}}
    # (2b) Note, the strategy for each history in strategy_dict_x and strategy_dict_o is probability distribution over
    # actions. But since tictactoe is a PIEFG, there always exists an optimal deterministic strategy (SPNE). So your
    # policy will be something like this {"0": 1, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0} where
    # "0" was the one of the best actions for the current player/history.
    if not history_obj.is_terminal_history():
        # if str(history_obj) == '0412':
        #     print(history_obj.get_valid_actions())
        if history_obj.current_player() == 'x':
            best_utility = -2
            best_move = -1
            # print(history_obj.get_valid_actions())
            # time.sleep(1)
            for move in history_obj.get_valid_actions():
                child = history_obj.update_history(move)
                # print(str(child))
                board_string = child.get_board_string()
                # if str(child)[:-1] == '0412':
                #     print(str(child), board_string in utilities, utilities[board_string])
                if board_string in utilities:
                    child_utility, cmove = utilities[board_string]
                #     if cmove is not None:
                #         strategy_dict_o[str(child)] = get_dict(move)
                else:
                    child_utility = backward_induction(child)
                if child_utility > best_utility:
                    best_move = move    
                    best_utility = child_utility
            strategy_dict_x[str(history_obj)] = get_dict(best_move)
        else:
            best_utility = 2
            best_move = -1
            for move in history_obj.get_valid_actions():
                child = history_obj.update_history(move)
                board_string = child.get_board_string()
                if str(child) in utilities:
                    child_utility, cmove = utilities[board_string]
                #     if cmove is not None:
                #         strategy_dict_x[str(child)] = get_dict(move)
                else:
                    child_utility = backward_induction(child)
                # print(child_utility)
                if child_utility < best_utility:
                    best_move = move
                    best_utility = child_utility
            # print('best', best_move)
            strategy_dict_o[str(history_obj)] = get_dict(best_move)
        utilities[history_obj.get_board_string()] = (best_utility, best_move)
    else:
        best_utility = utilities[history_obj.get_board_string()][0]
        # print(best_utility)
    return best_utility
    # TODO implement

# import itertools


def are_permutations(history, other):
    odd_elements_history = set()
    even_elements_history = set()
    odd_elements_other = set()
    even_elements_other = set()

    for i in range(len(history)):
        if i % 2 == 0:
            even_elements_history.add(history[i])
            even_elements_other.add(other[i])
        else:
            odd_elements_history.add(history[i])
            odd_elements_other.add(other[i])

    if odd_elements_history == odd_elements_other and even_elements_history == even_elements_other:
        return True
    return False

permutations = dict()

function_count = 0

def get_permutations(history):
    global permutations, function_count

    function_count += 1
    length = len(history)
    odd_elements = []
    even_elements = []
    # print(history, length)
    if length == 1 or length == 2:
        # print('Returning')
        permutations[history] = set([history,])
        return set([history,])
        # yield history
    
    if history in permutations:
        return permutations[history]

    for i in range(length):
        if i % 2 == 0:
            even_elements.append(history[i])
        else:
            odd_elements.append(history[i])

    permutations[history] = set()

    for i in range(0, length, 2):
        for j in range(1, length, 2):
            dupe = history
            if i < j:
                dupe = dupe[:i] + dupe[0] + dupe[i+1:j] + dupe[1] + dupe[j+1:]
            else:
                dupe = dupe[:j] + dupe[1] + dupe[j+1:i] + dupe[0] + dupe[i+1:]
            dupe = dupe[2:]
            # perms = get_permutations(dupe)
            # print(history, dupe, list(perms))
            # time.sleep(1)
            # print(dupe, get_permutations(dupe))
            for perm in get_permutations(dupe):
                # print('Yielding', history[i], history[j], perm)
                # yield history[i]+history[j]+perm
                permutations[history].add(history[i]+history[j]+perm)
    return permutations[history]



def solve_tictactoe():
    global strategy_dict_x, strategy_dict_o, utilities, permutations, function_count
    start_time = time.time()
    backward_induction(History())
    logging.info('Break')
    print(time.time() - start_time)
    x_keys = list(strategy_dict_x.keys())
    for element in x_keys:
        element_prob = strategy_dict_x[element]
        for emelent in get_permutations(element):
            strategy_dict_x[emelent] = element_prob

    o_keys = list(strategy_dict_o.keys())
    for element in o_keys:
        element_prob = strategy_dict_o[element]
        for emelent in get_permutations(element):
            strategy_dict_o[emelent] = element_prob
    
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    # print(len(strategy_dict_o), len(strategy_dict_x))
    # print(permutations)
    # print(function_count)
    print(time.time() - start_time)
    return strategy_dict_x, strategy_dict_o


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")