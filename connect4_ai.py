import math
import random


def is_terminal_node(board):
    return board.check_victory() or len(board.get_possible_moves()) == 0


def alpha_beta_decision(board, turn, ai_level, queue, max_player):
    # random move (to modify)
    # queue.put(board.get_possible_moves()[rnd.randint(0, len(board.get_possible_moves()) - 1)])
    queue.put(minimax(board, ai_level, -math.inf, math.inf, True, max_player)[0])


def minimax(board, depth, alpha, beta, max_player, player):
    opponent = 1
    if player == 1:
        opponent = 2
    possible_moves = board.get_possible_moves()
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if board.is_winning(player):
                return None, 100000000000  # AI wins
            elif board.is_winning(opponent):
                return None, -10000000000  # opponent wins
            else:
                return None, 0  # draw occurs
        else:  # depth is zero
            return None, score_position(board, player)

    if max_player:
        value = -math.inf
        column = random.choice(possible_moves)
        for col in possible_moves:
            tmp_board = board.copy()  # making a copy of board
            tmp_board.add_disk(col, player, False)  # adding disk of current player to the copy board
            new_value = minimax(tmp_board, depth - 1, alpha, beta, False, player)[1]  # evoking recursive function

            if new_value > value:  # updating values
                value = new_value
                column = col
            alpha = max(alpha, value)  # alpha beta pruning
            if alpha >= beta:
                break
        return column, value
    else:
        value = math.inf
        column = random.choice(possible_moves)
        for col in possible_moves:
            tmp_board = board.copy()  # making copy of board
            tmp_board.add_disk(col, opponent, False)  # adding disk of the opponent to the copy board
            new_value = minimax(tmp_board, depth - 1, alpha, beta, True, player)[1]  # evoking recursive function

            if new_value < value:  # updating values
                value = new_value
                column = col
            beta = min(beta, value)  # alpha beta pruning
            if alpha >= beta:
                break
        return column, value


def score_position(board, disk):
    score = 0

    # Score of placing in center column
    center_column = [int(i) for i in list(board.grid[:, 3])]
    score += center_column.count(disk) * 3

    # Horizontal assessment
    for r in range(6):
        row = [int(i) for i in list(board.grid[:, r])]
        for c in range(4):
            window = row[c : c + 4]
            score += evaluate_window(window, disk)

    # Vertical assessment
    for c in range(7):
        col = [int(i) for i in list(board.grid[c, :])]
        for r in range(3):
            window = col[r : r + 4]
            score += evaluate_window(window, disk)

    # Positive sloped diagonal assessment
    for r in range(3):
        for c in range(4):
            window = [board.grid[c + i][r + i] for i in range(4)]
            score += evaluate_window(window, disk)

    # Negative sloped diagonal assessment
    for r in range(3):
        for c in range(4):
            window = [board.grid[c + i][r + 3 - i] for i in range(4)]
            score += evaluate_window(window, disk)

    return score


def evaluate_window(window, player):
    score = 0
    opponent = 1
    if player == 1:
        opponent = 2

    if window.count(player) == 4:  # 4 disks in a row
        score += 100
    elif window.count(player) == 3 and window.count(0) == 1:  # 3 disks in a row and one empty slot
        score += 5
    elif window.count(player) == 2 and window.count(0) == 2:  # 2 disks in a row and 2 emtpy slots
        score += 2

    if window.count(opponent) == 3 and window.count(0) == 1:  # 3 opponent disks in a row and one empty slot
        score -= 4

    return score

    # To paste into original file into the Board class, helper method

    # def is_winning(self, player):
    #     # Horizontal alignment check
    #     for line in range(6):
    #         for horizontal_shift in range(4):
    #             if self.grid[horizontal_shift][line] == self.grid[horizontal_shift + 1][line] == self.grid[horizontal_shift + 2][line] == self.grid[horizontal_shift + 3][line] == player:
    #                 return True
    #     # Vertical alignment check
    #     for column in range(7):
    #         for vertical_shift in range(3):
    #             if self.grid[column][vertical_shift] == self.grid[column][vertical_shift + 1] == \
    #                     self.grid[column][vertical_shift + 2] == self.grid[column][vertical_shift + 3] == player:
    #                 return True
    #     # Diagonal alignment check
    #     for horizontal_shift in range(4):
    #         for vertical_shift in range(3):
    #             if self.grid[horizontal_shift][vertical_shift] == self.grid[horizontal_shift + 1][vertical_shift + 1] ==\
    #                     self.grid[horizontal_shift + 2][vertical_shift + 2] == self.grid[horizontal_shift + 3][vertical_shift + 3] == player:
    #                 return True
    #             elif self.grid[horizontal_shift][5 - vertical_shift] == self.grid[horizontal_shift + 1][4 - vertical_shift] ==\
    #                     self.grid[horizontal_shift + 2][3 - vertical_shift] == self.grid[horizontal_shift + 3][2 - vertical_shift] == player:
    #                 return True
    #     return False
