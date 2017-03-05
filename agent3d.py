import time

from game3d import *
import queue

TIME_LIMIT = 10
MAX_DEPTH = 0
NODES_QUEUE = queue.Queue()


def utility_hash(array):
    result = sum(array) / len(array)
    if max(array) >= 1.0:
        result = 1
    if max(array) <= -1.0:
        result = -1
    return result


class FieldNode(object):
    def __init__(self, field, gamer_index, parent=None):
        self.field = field
        self.parent = parent
        self.children = []
        self.utility = None
        self.next_move = None
        self.last_move = None

        self.gamer_index = gamer_index  # who will create mode

    def update_depth(self):
        self.depth = 0
        for i in range(self.field.get_size()[0]):
            for j in range(self.field.get_size()[1]):
                for k in range(self.field.get_size()[2]):
                    if self.field.get((i, j, k)) != 0:
                        self.depth += 1

    def add_child(self, field):
        node = FieldNode(field=field, gamer_index=field.enemy(self.gamer_index), parent=self)
        self.children.append(node)
        return node

    def update_utility(self):
        agent = Agent3d(self.field)
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
        lines = []
        # first 16 vertical
        for i in range(self.field.get_size()[0]):
            # line = []
            for j in range(self.field.get_size()[1]):
                line2 = []
                for k in range(self.field.get_size()[2]):
                    line2.append((i, j, k))
                lines.append(line2)
        # print(lines)

        # next 16 horizontal
        for k in range(self.field.get_size()[1]):
            # line = []
            for i in range(self.field.get_size()[0]):
                line2 = []
                for j in range(self.field.get_size()[2]):
                    line2.append((i, j, k))
                lines.append(line2)
        # print(lines)

        # next 16 horizontal another
        for j in range(self.field.get_size()[1]):
            for k in range(self.field.get_size()[0]):
                line2 = []
                for i in range(self.field.get_size()[2]):
                    line2.append((i, j, k))
                lines.append(line2)
        # print(lines)

        # 3d diagonals
        line = [(0, 0, 0), (1, 1, 1), (2, 2, 2), (3, 3, 3)]
        lines.append(line)
        line = [(0, 3, 3), (1, 2, 2), (2, 1, 1), (3, 0, 0)]
        lines.append(line)
        line = [(0, 3, 0), (1, 2, 1), (2, 1, 2), (3, 0, 3)]
        lines.append(line)
        line = [(0, 0, 3), (1, 1, 2), (2, 2, 1), (3, 3, 0)]
        lines.append(line)
        # print(lines)

        # diagonal from 1 side
        for i in range(self.field.get_size()[0]):
            line = []
            for j in range(self.field.get_size()[1]):
                line.append((j, j, i))
            lines.append(line)

        for k in range(self.field.get_size()[0]):
            line = []
            for i in range(3, -1, -1):
                j = 3 - i
                line.append((i, j, k))
            lines.append(line)
        # print(lines)

        # diagonal from 2 side
        for j in range(self.field.get_size()[0]):
            line = []
            for i in range(self.field.get_size()[1]):
                line.append((i, j, i))
            lines.append(line)

        for j in range(self.field.get_size()[0]):
            line = []
            for i in range(3, -1, -1):
                k = 3 - i
                line.append((i, j, k))
            lines.append(line)
        # print(lines)

        # diagonal from 3 side
        for i in range(self.field.get_size()[0]):
            line = []
            for j in range(self.field.get_size()[1]):
                line.append((i, j, j))
            lines.append(line)

        for i in range(self.field.get_size()[0]):
            line = []
            for j in range(3, -1, -1):
                k = 3 - j
                line.append((i, j, k))
            lines.append(line)
        # print(lines)

        return lines

    def create_move_minimax(self, gamer_index, start_time, max_depth=6):
        def go_to_depth():
            global MAX_DEPTH
            root_node = NODES_QUEUE.get()
            MAX_DEPTH = max(MAX_DEPTH, root_node.depth)
            root_node.update_utility()

            if utility_hash(root_node.utility) == 1.0 or utility_hash(root_node.utility) == -1.0:
                return None

            root_node.utility = None
            empty_flag = True
            for i in range(root_node.field.get_size()[0]):
                for j in range(root_node.field.get_size()[1]):
                    for k in range(root_node.field.get_size()[1]):
                        if root_node.field.get((i, j, k)) == 0:
                            empty_flag = False
                            node = root_node.add_child(root_node.field.copy())
                            node.field.put((i, j, k), gamer_index)

                            # node.game.field.show()
                            node.last_move = (i, j, k)
                            node.gamer_index = node.field.enemy(gamer_index)
                            node.update_depth()
                            NODES_QUEUE.put(node)

            if empty_flag:
                root_node.update_utility(root_node.game.enemy(gamer_index))

        def update_tree_utility(node, max_depth):
            def func(x, y):
                nx = utility_hash(x)
                ny = utility_hash(y)
                return nx > ny if node.gamer_index == 1 else nx < ny

            if node.depth == max_depth:
                node.update_utility()
                return None

            for child in node.children:
                update_tree_utility(child, max_depth)
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

        copy_field = self.field.copy()
        root = FieldNode(copy_field, gamer_index)
        root.update_depth()
        NODES_QUEUE.put(root)

        while time.time() - start_time < 0.95*TIME_LIMIT:
            # print(time.time()-start_time)
            # Go to depth
            go_to_depth()

        print(MAX_DEPTH)
        update_tree_utility(root, MAX_DEPTH - 1)
        self.field.show_everytime = prev_showing

        def get_moves(node, prev_moves):
            move = node.next_move
            # print(move, prev_moves)
            if node.children.__len__() == 0 or node.depth == MAX_DEPTH - 1:
                return prev_moves
            for child in node.children:
                if child.field.get(move) != 0:
                    return get_moves(child, prev_moves + [move])

        return utility_hash(root.utility), root, get_moves(root, [])


if __name__ == '__main__':
    f = Field3D((4, 4, 4), show_everytime=False)
    agent = Agent3d(field=f)
    f.show()

    start = time.time()
    score, root, moves = agent.create_move_minimax(1, max_depth=3, start_time=start)
    print(score, moves)
    print(time.time() - start)
