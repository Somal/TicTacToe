import copy


class Field3D(object):
    def __init__(self, size, points=('_', 'X', 'O'), show_everytime=True):
        self.size = size
        self.field = []
        self.points = points
        self.show_everytime = show_everytime
        for i in range(self.size[0]):
            tmp = []
            for j in range(self.size[1]):
                tmp1 = []
                for k in range(self.size[2]):
                    tmp1.append(0)
                tmp.append(tmp1)
            self.field.append(tmp)

    def put(self, point, gamer_index):
        if gamer_index <= 0 or gamer_index >= len(self.points):
            raise ValueError('Gamer_index is wrong')
        i, j, k = point

        if self.field[i][j][k] != 0:
            raise ValueError('This point is not empty')
        self.field[i][j][k] = gamer_index

        if self.show_everytime:
            self.show()

    def get(self, point):
        i, j, k = point
        return self.field[i][j][k]

    def show(self):
        for k in range(self.size[0]):
            for i in range(self.size[1]):
                tmp1 = []
                for j in range(self.size[2]):
                    tmp1.append(self.points[self.get((i, j, k))])
                # tmp.append(self.points[self.field[i][j]])
                print(" | ".join(tmp1))
            print()

    def get_size(self):
        return self.size

    def get_points(self):
        return self.points

    def compare_points(self, point1, point2):
        return self.field[point1[0]][point1[1]][point1[2]] == self.field[point2[0]][point2[1]][point2[2]]

    def checking_edges(self, point):
        i, j, k = point
        return i >= 0 and j >= 0 and k >= 0 and i < self.size[0] and j < self.size[1] and k < self.size[2]

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

    def move_back(self, point):
        i, j, k = point
        self.field[i][j][k] = 0

    def enemy(self, gamer_index):
        enemy_index = 1
        for i in range(len(self.get_points())):
            if i > 0 and i != gamer_index:
                enemy_index = i

        return enemy_index

    def copy(self):
        return copy.deepcopy(self)


if __name__ == "__main__":
    f = Field3D((3, 3, 3), show_everytime=False)
    # g = Game(field=f, show_everytime=True)
    f.put((1, 1, 0), 1)
    f.put((2, 2, 2), 2)
    # a = f.compare_points((1,1,1), (2,2,2))
    # print(a)
    # print(f.get((1,1,1)))
    f.show()

    # f.move_back((1,1,1))
    # f.show()
    # g.put(1, 1, 1)
    # g.put(1, 2, 1)
    # g.put(3, 1, 1)
