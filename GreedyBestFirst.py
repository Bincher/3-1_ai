from queue import PriorityQueue

# Shortest Path Finding Problem : 20개 도시의 예제에 대한 내용을 포함하는 클래스
class Problem:
    def __init__(self):
        self.initial_state = 'A'    # 초기 도시 : A
        self.goal_state = 'M'       # 목적 도시 : M
        # 도시 사이의 거리 : A(0)~M(19), -1(바로가는 경로 없음), 0(자기 자신)
        self.distance = [[0, 75, -1, 118, -1, -1, -1., 140, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [75, 0, 71, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, 71, 0, -1, -1, -1, -1, 151, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [118, -1, -1, 0, 111, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, 111, 0, 70, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, 70, 0, 75, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, 75, 0, -1, -1, 120, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [140, -1, 151, -1, -1, -1, -1, 0, 80, -1, -1, 99, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, 80, 0, 146, 97, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, 120, -1, 146, 0, 138, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, 97, 138, 0, -1, 101, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, 99, -1, -1, -1, 0, 211, -1, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 101, 211, 0, 90, 85, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 90, 0, -1, -1, -1, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 86, -1, 0, 98, -1, 142, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 98, 0, 86, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 86, 0, -1, -1, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 142, -1, -1, 0, 92, -1],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 92, 0, 87],
                         [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 87, 0]]
        # 각 도시로부터 목적 도시인 M 도시까지의 직선 거리
        self.straight_line_distance = [366, 374, 380, 329, 244, 241, 242, 253, 193, 160, 98, 178, 0, 77, 80, 151, 161, 199, 226, 234]

        self.index_to_state = {}    # index로부터 상태(도시) 반환
        self.state_to_index = {}    # 상태로부터 index 반환
        state = 'A'
        index = 0
        while state <= 'T':
            self.index_to_state[index] = state
            self.state_to_index[state] = index
            state = chr(ord(state) + 1)
            index += 1

# Tree 탐색 시 state 하나와 그에 대하 부가적인 정보를 포함하는 노드 클래스
class Node:
    def __init__(self):
        self.state = None
        self.parent_node = None # 부모 노드
        self.action = None      # route finding 문제의 경우 state와 동일
        self.path_cost = 0      # breadth first 탐색의 경우 사용하지 않음
        self.f = 0              # Informed Search(Greedy Best-first Search, A* Search)
        self.depth = 0          # tree search에서의 depth(root == 0)

# 현재 state가 지나온 경로 상에 이미 나왔던(expand되었던) 경로인지 확인
def IsVisitedState(state, parent_node):
    while parent_node != None:
        if parent_node.state == state:
            return True
        parent_node = parent_node.parent_node
    return False

# 노드 하나를 expand하는 함수
def Expand(parent_node, problem):
    expanded_nodes = []

    parent_index = problem.state_to_index[parent_node.state]
    for index in range(len(problem.distance[parent_index])):
        if problem.distance[parent_index][index] > 0:     # 현재 state로부터 연결되어 있다면
            state = problem.index_to_state[index]
            if not IsVisitedState(state, parent_node):    # 이미 지나온 경로인지 확인
                node = Node()
                node.state = state
                node.parent_node = parent_node
                node.action = node.state
                node.path_cost = parent_node.path_cost + problem.distance[parent_index][index]
                node.f = problem.straight_line_distance[index]     # Greedy Best-first Search
                node.depth = parent_node.depth + 1
                expanded_nodes.append(node)

    return expanded_nodes

# Tree 탐색을 수행하는 함수 : fringe에 노드를 삽입/인출하는 방법에 따라 다양한 Tree 탐색 알고리즘이 만들어질 수 있음
# fringe가 f(=h) 값을 기준으로 한 PriorityQueue와 같이 동작하는 경우 Greedy Best-first Search가 됨
def TreeSearch(problem, fringe):
    node = Node()
    node.state = problem.initial_state
    node.depth = 0
    node.f = problem.straight_line_distance[0]
    fringe.put((node.f, node))
    print("Expanded State : ", end="")

    while True:
        if fringe.empty():
            return False
        node = fringe.get()[1]
        print(f"{node.state}({node.f}) ", end="")
        if node.state == problem.goal_state:
            return node
        expanded_nodes = Expand(node, problem)
        for node in expanded_nodes:
            fringe.put((node.f, node))

# Greedy Best-first Search를 수행하기 위해 PriorityQueue를 사용하여 fringe를 만들고 TreeSearch 함수를 실행함
def main():
    problem = Problem()
    print("<<< Greedy Best-first Search >>>")
    fringe = PriorityQueue()     # 우선순위 Queue
    solution = TreeSearch(problem, fringe)
    expand_order = []
    while solution != None:
        expand_order.insert(0, solution.state)
        solution = solution.parent_node
    print("\nSolution Path :", expand_order)

main()
