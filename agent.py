from game import *


class Line(object):
    def __init__(self, coords_2d, field_2d):
        self.coords = coords_2d
        self.field = field_2d

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
        return result

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

    def create_move(self):
        pass


if __name__ == '__main__':
    f = Field2D((3, 3))
    g = Game(field=f)
    agent = Agent(game=g)
    g.put(1, 1, 1)
    g.put(0, 0, 2)
    g.put(2, 0, 1)
    g.put(0, 2, 2)
    for line in agent.linker[(0, 1)]:
        print(str(line), line.get_statistics(), line.utility(1))

    for i in range(g.field.get_size()[0]):
        for j in range(g.field.get_size()[1]):
            pass