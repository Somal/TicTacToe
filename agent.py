from game import *


def utility_hash(array):
    result = sum(array) / len(array)
    if max(array) >= 1.0:
        result = 1
    if max(array) <= -1.0:
        result = -1
    return result


class GameNode(object):
    def __init__(self, game, parent=None):
        self.game = game
        self.parent = parent
        self.children = []
        self.utility = None
        self.move = None
        self.depth = 0 if parent is None else parent.depth + 1

    def add_child(self, game):
        node = GameNode(game=game, parent=self)
        self.children.append(node)
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

    # Not use
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

    def create_move_minimax(self, gamer_index, max_depth=6):
        def go_to_depth(max_depth, root_node, gamer_index):
            if max_depth == 0:
                game = root_node.game
                agent = Agent(game)
                U = []
                for line in agent.lines:
                    u_i = line.utility(game.enemy(gamer_index))
                    U.append(u_i)
                root_node.utility = U

                update_parents(root_node)
                return None

            node = root_node.add_child(root_node.game.copy())
            for i in range(root_node.game.field.get_size()[0]):
                for j in range(root_node.game.field.get_size()[1]):
                    try:
                        node.game.put(i, j, gamer_index)

                        node.game.field.show()
                        node.move = (i, j)
                        go_to_depth(max_depth - 1, node, node.game.enemy(gamer_index))  # Change index to enemy
                        print(sum(node.utility) / len(node.utility))
                        node = root_node.add_child(root_node.game.copy())
                    except Exception as e:
                        # print(e)
                        pass

        def update_parents(node):
            if node is not None:
                def func(x, y):
                    nx = utility_hash(x)
                    ny = utility_hash(y)
                    return nx > ny if node.depth % 2 == 0 else nx < ny

                for child in node.children:
                    if child.utility is not None:
                        if node.utility is None:
                            node.utility = child.utility
                            node.move = child.move

                        if func(child.utility, node.utility):
                            node.utility = child.utility
                            node.move = child.move

                if node.parent is not None:
                    update_parents(node.parent)

        prev_showing = self.game.show_everytime
        self.game.show_everytime = False

        root = GameNode(self.game.copy())

        # Go to depth
        go_to_depth(max_depth, root, gamer_index)

        self.game.show_everytime = prev_showing
        return utility_hash(root.utility), root.move


if __name__ == '__main__':
    f = Field2D((3, 3))
    g = Game(field=f, show_everytime=False)
    agent = Agent(game=g)
    # g.put(2, 2, 1)
    # g.put(2, 0, 2)
    # g.put(0, 0, 1)
    # g.put(0, 2, 2)
    g.field.show()
    print(agent.create_move_minimax(1, max_depth=1))
