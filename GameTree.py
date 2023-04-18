import copy
import random

# Game Tree Search 대상 문제 : Tic-Tac-Toe
class Problem:
    def __init__(self):
        self.board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]
        # -1(공백), 1(X, computer, MAX), 0(O, human, MIN)
        self.turn = 0
        self.max_depth = 2

    def PrintBoard(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 1:
                    print("X ", end="")
                elif self.board[i][j] == 0:
                    print("O ", end="")
                if self.board[i][j] == -1:   # 공백이라면
                    print("_ ", end="")
            print()

    def Utility(self, state):   # 0을 중심으로
        count1 = self.GetScore(state, 1, 0)
        count0 = self.GetScore(state, 0, 1)

        if count1 == 100:
            return count1
        elif count0 == 100:
            return -count0

        return count1 - count0

    def GetScore(self, state, player, opponent):
        # made이면 100점
        if self.Made(state, player):
            return 100

        # made가 가능한 라인 개수 계산 및 반환
        score = 0

        for i in range(3):
            if self.PossibleMade(state[i][0], state[i][1], state[i][2], opponent):
                score += 1
            if self.PossibleMade(state[0][i], state[1][i], state[2][i], opponent):
                score += 1
        if self.PossibleMade(state[0][0], state[1][1], state[2][2], opponent):
            score += 1
        if self.PossibleMade(state[0][2], state[1][1], state[2][0], opponent):
            score += 1

        return score

    def Made(self, state, player):
        for i in range(3):
            if state[i][0] == player and (state[i][0] == state[i][1] == state[i][2]):   # 가로
                return True
            if state[0][i] == player and (state[0][i] == state[1][i] == state[2][i]):   # 세로
                return True
        if state[0][0] == player and (state[0][0] == state[1][1] == state[2][2]):       # 대각선 \
            return True
        if state[0][2] == player and (state[0][2] == state[1][1] == state[2][0]):       # 대각선 /
            return True

    def PossibleMade(self, pos1, pos2, pos3, opponent):
        if pos1 != opponent and pos2 != opponent and pos3 != opponent:
            return True
        return False

    def TerminalTest(self, state, depth):
        # depth가 max_depth 이상이면 끝
        if depth >= self.max_depth:
            return True

        # made이면 끝
        if self.Made(state, 1) or self.Made(state, 0):
            return True

        # 공백이 하나라도 있으면 끝이 아님
        if not self.NoBlank(state):
            return False

        # 이외(공백이 없음)에는 끝
        return True

    def NoBlank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == -1:
                    return False
        return True

    def Successors(self, state, player):
        successors = []

        for i in range(3):
            for j in range(3):
                if state[i][j] == -1:   # 공백이라면
                    new_state = copy.deepcopy(state)
                    new_state[i][j] = player
                    successors.append([(i, j), new_state])

        return successors

best_state_list = []
best_max_value = -10000

def MiniMax(state):
    v = MaxValue(state, -10000, 10000, 0)
    return best_state_list[0][0]
    #return random.choice(best_state_list)[0]

def MaxValue(state, alpha, beta, depth):
    global best_state_list, best_max_value
    if depth == 0:
        best_state_list = []
        best_max_value = -10000

    if problem.TerminalTest(state, depth):
        return problem.Utility(state)

    v = -10000
    for successor in problem.Successors(state, 1):
        min_value = MinValue(successor[1], alpha, beta, depth + 1)
        if depth == 0:
            if min_value > best_max_value:
                best_state_list = []
                best_state_list.append((successor[0], successor[1], min_value))
                best_max_value = min_value
            #elif min_value == best_max_value:
            #    best_state_list.append((successor[0], successor[1], min_value))
        v = max(v, min_value)
        alpha = max(alpha, v)
        if beta <= alpha:       # if beta < alpha
            break

    return v

def MinValue(state, alpha, beta, depth):
    if problem.TerminalTest(state, depth):
        return problem.Utility(state)

    v = 10000
    for successor in problem.Successors(state, 0):
        v = min(v, MaxValue(successor[1], alpha, beta, depth + 1))
        beta = min(beta, v)
        if beta <= alpha:       # if beta < alpha:
            break

    return v

problem = Problem()

def main():
    problem.PrintBoard()

    while True:
        i, j = MiniMax(problem.board)
        print(f"컴퓨터 : ({i}, {j}) 선택")
        problem.board[i][j] = 1
        problem.PrintBoard()

        if problem.GetScore(problem.board, 1, 0) == 100:
            print("컴퓨터 승리!!!")
            break

        if problem.NoBlank(problem.board):
            print("비겼습니다.")
            break

        i, j = eval(input("위치 선택(x, y) : "))
        problem.board[i][j] = 0
        problem.PrintBoard()

        if problem.GetScore(problem.board, 0, 1) == 100:
            print("너 승리!!!")
            break

        if problem.NoBlank(problem.board):
            print("비겼습니다.")
            break

main()