class Field2D(object):
    def __init__(self, size, points=('_', 'X', 'O')):
        self.size = size
        self.field = []
        self.points = points
        for i in range(self.size[0]):
            tmp = []
            for j in range(self.size[1]):
                tmp.append(0)
            self.field.append(tmp)

    def put(self, point, gamer_index):
        if gamer_index <= 0 or gamer_index >= len(self.points):
            raise ValueError('Gamer_index is wrong')
        i, j = point
        self.field[i][j] = gamer_index

    def get(self, point):
        i, j = point
        return self.field[i][j]

    def show(self):
        for i in range(self.size[0]):
            tmp = []
            for j in range(self.size[1]):
                tmp.append(self.points[self.field[i][j]])
            print(" | ".join(tmp))
        print()

    def get_size(self):
        return self.size

    def get_points(self):
        return self.points

    def compare_points(self, point1, point2):
        return self.field[point1[0]][point1[1]] == self.field[point2[0]][point2[1]]

    def checking_edges(self, point):
        x, y = point
        return x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]

    def check_field(self):
        """
        Not WORKS!!
        :return:
        """
        # TODO: Change criterion of win (not sum)!!
        for i in range(self.get_size()[0]):
            points_sum = sum(self.field[i])
            if points_sum == (points_sum // self.get_size()[0]) * self.get_size()[0] and points_sum > 0:
                return True

        for j in range(self.get_size()[1]):
            points_sum = sum([self.field[i][j] for i in range(self.get_size()[0])])
            if points_sum == (points_sum // self.get_size()[1]) * self.get_size()[1] and points_sum > 0:
                return True

        # Diagonal checking 1
        d = (1, 1)
        point = (0, 0)
        points_sum = 0
        while self.checking_edges(point):
            points_sum += self.get(point)
            point = (point[0] + d[0], point[1] + d[1])

        if points_sum == (points_sum // self.get_size()[1]) * self.get_size()[1] and points_sum > 0:
            return True

        # Diagonal checking 2
        d = (-1, 1)
        point = (self.get_size()[0] - 1, 0)
        points_sum = 0
        while self.checking_edges(point):
            points_sum += self.get(point)
            point = (point[0] + d[0], point[1] + d[1])

        if points_sum == (points_sum // self.get_size()[1]) * self.get_size()[1] and points_sum > 0:
            return True

        return False


class Game(object):
    def __init__(self, field: Field2D, show_everytime=True):
        self.field = field
        self.finished = False
        self.show_everytime = show_everytime

    def put(self, x, y, gamer_index):
        if self.finished:
            print('The game is finished')
            return 0

        if self.field.get((x, y)) != 0:
            raise ValueError('This point is not empty')

        self.field.put((x, y), gamer_index=gamer_index)
        # if self.field.check_field():
        #     print("{} wins".format(self.field.get_points()[gamer_index]))
        if self.show_everytime:
            self.field.show()


if __name__ == "__main__":
    f = Field2D((3, 3))
    g = Game(field=f, show_everytime=True)
    g.put(1, 0, 1)
    g.put(1, 1, 1)
    g.put(1, 2, 1)
    # g.put(3, 1, 1)
