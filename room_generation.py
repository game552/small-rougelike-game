import random
import queue

level = 1
count_of_rooms = random.randint(1, 2) + 5 + round(level * 2.6)


class Map:
    def __init__(self):
        self.map = {x + y: False for y in range(10, 80, 10) for x in range(1, 10)}
        self.row = []
        self.que = queue.Queue()
        self.conclusion = []

    def set_cell(self, position, value):
        """Установить значение в ячейку карты."""
        if position in self.map:
            self.map[position] = value
        else:
            raise ValueError(f"Ячейка {position} вне допустимых границ.")

    def get_cell(self, position):
        """Получить значение из ячейки карты."""
        return self.map.get(position, False)

    def display_map(self):
        """Вывод карты в удобном виде."""
        for y in range(70, 10, -10):
            row = [str(self.map.get(x + y, '   ')).center(5) for x in range(1, 10)]
            print('  '.join(row))

    def return_map(self):
        for y in range(70, 10, -10):
            self.row.append([self.map.get(x + y) for x in range(1, 10)])
        return self.row

    def room_generation(self, position):
        neighbors = count_neighbors(position)
        for i in neighbors:
            choose = random.randint(0, 1)
            if not all(self.map_neighbors(neighbors)):
                if all(count_neighbors(i)):
                    if len(self.conclusion) < count_of_rooms:
                        if not self.get_cell(i):
                            if choose:
                                self.set_cell(i, "Room")
                                self.conclusion.append(i)
                                self.que.put(i)

    def map_neighbors(self, neighbors):
        return [self.get_cell(i) for i in neighbors]


def count_neighbors(pos):
    neighbors = []
    if 0 <= pos - 10 <= 80:
        neighbors.append(pos - 10)
    else:
        neighbors.append(False)
    if 0 <= pos + 10 <= 80:
        neighbors.append(pos + 10)
    else:
        neighbors.append(False)
    if 0 <= pos - 1 <= 80:
        neighbors.append(pos - 1)
    else:
        neighbors.append(False)
    if 0 <= pos + 1 <= 80:
        neighbors.append(pos + 1)
    else:
        neighbors.append(False)
    return neighbors
