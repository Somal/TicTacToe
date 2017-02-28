from game import *


class Line(object):
    def __init__(self, coordinates_2d, field_2d, linker):
        self.coords = coordinates_2d
        self.line = []
        for i, x, y in enumerate(self.coords):
            pass

    def show(self):
        print(self.coords[0], self.coords[-1])


class Agent(object):
    def __init__(self, game: Game):
        self.game = game
        self.linker = []  # 2d field
        for i in range(self.game.field.get_size()[0]):
            tmp = []
            for j in range(self.game.field.get_size()[1]):
                tmp.append(None)
            self.linker.append(tmp)

        lines = self.line_generation()
        # TODO: create linkers

    def line_generation(self):
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
