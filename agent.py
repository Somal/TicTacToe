from game import *


class FieldNode(object):
    def __init__(self, field, parent=None):
        self.field = field
        self.parent = parent
        self.children = []
        self.max_utility = 0
        self.next_move = None

    def add_child(self, child):
        self.children.append(child)


class Tree(object):
    def __init__(self, root_field):
        self.root = FieldNode(field=root_field)

    def get_root(self):
        return self.root

    def add_node(self, parent, node_field):
        node = FieldNode(field=node_field, parent=parent)
        parent.add_child(node)
        return node


class Line(object):
    def __init__(self, coords_2d, field_2d, weight=1):
        self.coords = coords_2d
        self.field = field_2d
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
            result = -enemy_move_count / len(self.coords)
        if gamer_move_count > 0 and enemy_move_count == 0:
            result = gamer_move_count / len(self.coords)
        return result * self.weight

    def show(self):
        print(self.coords[0], self.coords[-1])

    def __str__(self):
        return "| {}, {} |".format(self.coords[0], self.coords[-1])


class Agent(object):
    def __init__(self, game: Game):
        self.game = game
        self.linker = {}  # 2d field  {point: list(Line)}
        self.lines = set([])  # Store all distinct lines
        for i in range(self.game.field.get_size()[0]):
            for j in range(self.game.field.get_size()[1]):
                self.linker[(i, j)] = []

        self.__init_linker()

    def __init_linker(self):
        lines_coord = self.line_coord_generation()
        for line_coord in lines_coord:
            line = Line(line_coord, field_2d=self.game.field)
            self.lines.add(line)
            for point in line_coord:
                self.linker[point].append(line)

        for i in range(self.game.field.get_size()[0]):
            for j in range(self.game.field.get_size()[1]):
                lines = []
                for line in self.linker[(i, j)]:
                    lines.append(str(line))
                    # print(i, j, lines)

    def line_coord_generation(self):
        lines = []
        for i in range(self.game.field.get_size()[0]):
            line = []
            for j in range(self.game.field.get_size()[1]):
                line.append((i, j))
            lines.append(line)

        for j in range(self.game.field.get_size()[1]):
            line = []
            for i in range(self.game.field.get_size()[0]):
                line.append((i, j))
            lines.append(line)

        # Diagonal checking 1
        d = (1, 1)
        point = (0, 0)
        line = []
        while self.game.field.checking_edges(point):
            line.append(point)
            point = (point[0] + d[0], point[1] + d[1])
        lines.append(line)

        # Diagonal checking 2
        d = (-1, 1)
        point = (self.game.field.get_size()[0] - 1, 0)
        line = []
        while self.game.field.checking_edges(point):
            line.append(point)
            point = (point[0] + d[0], point[1] + d[1])
        lines.append(line)
        return lines

    def create_move_locally(self, gamer_index, comparison_func):
        prev_showing = self.game.show_everytime
        self.game.show_everytime = False

        utilities = {}
        for i in range(self.game.field.get_size()[0]):
            for j in range(self.game.field.get_size()[1]):
                # Try to put point to somewhere
                try:
                    g.put(i, j, gamer_index)
                    U = []
                    for line in agent.lines:
                        u_i = line.utility(gamer_index)
                        U.append(u_i)
                    utilities[(i, j)] = U
                    g.field.move_back((i, j))
                except:
                    pass

        self.game.show_everytime = prev_showing
        result, point = comparison_func(utilities)
        return result, point

    def default_comparison_vectors_func(self, utilities):
        max_result = 0
        result_point = None
        for point, utility_vector in utilities.items():
            avg = sum(utility_vector) / len(utility_vector)
            if avg > max_result:
                max_result = avg
                result_point = point
        return max_result, result_point

    def create_move_minimax(self, gamer_index, comparison_func, depth=6):
        tree = Tree(self.game.copy())


if __name__ == '__main__':
    f = Field2D((3, 3))
    g = Game(field=f)
    agent = Agent(game=g)
    g.put(0, 0, 1)
    g.put(1, 2, 2)
    g.put(2, 1, 1)
    # g.put(0, 2, 2)
    # for line in agent.linker[(0, 1)]:
    #     print(str(line), line.get_statistics(), line.utility(1))
    print(agent.create_move_locally(2, agent.default_comparison_vectors_func))
