import time

from .game3d import *


def utility_hash(array):
    if array is None:
        result = None
    else:
        result = sum(array) / len(array)
        if max(array) >= 1.0:
            result = 1
        if max(array) <= -1.0:
            result = -1
    return result


class GameNode(object):
    def __init__(self, game, gamer_index, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.utility = None
        self.next_move = None
        self.last_move = None

        self.gamer_index = gamer_index  # who will create mode

    def add_child(self, game):
        node = GameNode(game=game, gamer_index=game.enemy(self.gamer_index), parent=self)
        self.children.append(node)
        return node

    def update_utility(self):
        agent = Agent3d(self.game)
        U = []
        for line in agent.lines:
            u_i = line.utility(1)
            U.append(u_i)
        self.utility = U


class Line(object):
    def __init__(self, coords_3d, field_3d, weight=1):
        self.coords = coords_3d
        self.field = field_3d
        self.weight = weight

    def get_statistics(self):
        """
        :return: dict with count of distinct gamer's moves, i.e. {0: 2, 1: 1, 2: 0}
        :rtype: dict
        """
        stats = {}
        for points_type_index in range(len(self.field.get_points())):
            stats[points_type_index] = 0

        for point in self.coords:
            value = self.field.get(point)
            stats[value] += 1

        return stats

    def utility(self, gamer_index):
        stats = self.get_statistics()
        enemy_index = 1
        for i in range(len(self.field.get_points())):
            if i > 0 and i != gamer_index:
                enemy_index = i

        result = 0
        gamer_move_count = stats[gamer_index]
        enemy_move_count = stats[enemy_index]
        if gamer_move_count == 0 and enemy_move_count > 0:
            result = -(enemy_move_count / len(self.coords)) ** 1
        if gamer_move_count > 0 and enemy_move_count == 0:
            result = (gamer_move_count / len(self.coords)) ** 1
        return result * self.weight

    def show(self):
        print(self.coords[0], self.coords[-1])

    def __str__(self):
        return "| {}, {} |".format(self.coords[0], self.coords[-1])


class Agent3d(object):
    def __init__(self, field: Field3D):
        self.field = field
        self.linker = {}  # 2d field  {point: list(Line)}
        self.lines = set([])  # Store all distinct lines
        for i in range(self.field.get_size()[0]):
            for j in range(self.field.get_size()[1]):
                for k in range(self.field.get_size()[1]):
                    self.linker[(i, j, k)] = []

        self.__init_linker()

    def __init_linker(self):
        lines_coord = self.line_coord_generation()
        for line_coord in lines_coord:
            line = Line(line_coord, field_3d=self.field)
            self.lines.add(line)
            for point in line_coord:
                self.linker[point].append(line)

        for i in range(self.field.get_size()[0]):
            for j in range(self.field.get_size()[1]):
                for k in range(self.field.get_size()[2]):
                    lines = []
                    for line in self.linker[(i, j, k)]:
                        lines.append(line)
                        # print(i, j, lines)

    def line_coord_generation(self):
        pass

    def create_move_minimax(self, gamer_index, max_depth=6):
        def go_to_depth(max_depth, root_node, gamer_index, full_root):
            root_node.update_utility(root_node.game.enemy(gamer_index))
            if max_depth == 0:
                return None

            if utility_hash(root_node.utility) == 1.0 or utility_hash(root_node.utility) == -1.0:
                return None

            root_node.utility = None
            empty_flag = True
            for i in range(root_node.game.field.get_size()[0]):
                for j in range(root_node.game.field.get_size()[1]):
                    if root_node.game.field.get((i, j)) == 0:
                        empty_flag = False
                        node = root_node.add_child(root_node.game.copy())
                        node.game.put(i, j, gamer_index)

                        # node.game.field.show()
                        node.last_move = (i, j)
                        go_to_depth(max_depth - 1, node, node.game.enemy(gamer_index),
                                    full_root)  # Change index to enemy
            if empty_flag:
                root_node.update_utility(root_node.game.enemy(gamer_index))

        def update_tree_utility(node, root):
            def func(x, y):
                nx = utility_hash(x)
                ny = utility_hash(y)
                return nx > ny if node.gamer_index == 1 else nx < ny

            for child in node.children:
                update_tree_utility(child, root)
                if node.utility is None:
                    node.utility = child.utility
                    node.next_move = child.last_move

                if func(child.utility, node.utility):
                    node.utility = child.utility
                    node.next_move = child.last_move
                    #     if node.move == (0, 0) and node is root:
                    #         child.game.field.show()
                    #         print(child.move)
                    #
                    # if node is root:
                    #     print(node.move)

        prev_showing = self.field.show_everytime
        self.field.show_everytime = False

        root = GameNode(self.field.copy(), gamer_index)

        # Go to depth
        go_to_depth(max_depth, root, gamer_index, root)
        update_tree_utility(root, root)
        self.field.show_everytime = prev_showing

        def get_moves(node, prev_moves):
            move = node.next_move
            # print(move, prev_moves)
            if node.children.__len__() == 0:
                return prev_moves
            for child in node.children:
                if child.game.field.get(move) != 0:
                    return get_moves(child, prev_moves + [move])

        return utility_hash(root.utility), root, get_moves(root, [])


if __name__ == '__main__':
    f = Field3D((3, 3, 3), show_everytime=False)
    agent = Agent3d(field=f)
    f.show()
    # t = time.time()
    # score, root, moves = agent.create_move_minimax(1, max_depth=5)
#     print(score, moves)
#     print(time.time() - t)
