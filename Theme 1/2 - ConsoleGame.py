import random


class Cell:
    def __init__(self, around_mines=0, mine=False):
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False


class GamePole:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.pole = [[Cell() for _ in range(n)] for _ in range(n)]
        self.game_over = False
        self.init()

    def init(self):
        all_coords = [(i, j) for i in range(self.n) for j in range(self.n)]
        mine_coords = random.sample(all_coords, self.m)

        for i, j in all_coords:
            self.pole[i][j].mine = False
            self.pole[i][j].fl_open = False
            self.pole[i][j].around_mines = 0

        for i, j in mine_coords:
            self.pole[i][j].mine = True

        for i in range(self.n):
            for j in range(self.n):
                if not self.pole[i][j].mine:
                    self.pole[i][j].around_mines = self._count_mines_around(i, j)

    def _count_mines_around(self, x, y):
        count = 0
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if dx == 0 and dy == 0:
                    continue
                if 0 <= nx < self.n and 0 <= ny < self.n:
                    if self.pole[nx][ny].mine:
                        count += 1
        return count

    def show(self):
        for row in self.pole:
            line = []
            for cell in row:
                if not cell.fl_open:
                    line.append('#')
                elif cell.mine:
                    line.append('*')
                else:
                    line.append(str(cell.around_mines))
            print(' '.join(line))
        print()

    def open_cell(self, x, y):
        if not (0 <= x < self.n and 0 <= y < self.n):
            print("Координаты вне поля!")
            return

        cell = self.pole[x][y]
        cell.fl_open = True
        if cell.mine:
            self.game_over = True
            self._reveal_all()
            print("\nМина взорвалась! Игра окончена.\n")
            self.show()

    def _reveal_all(self):
        for row in self.pole:
            for cell in row:
                cell.fl_open = True

    def run(self):
        print("Игра Сапёр. Введите координаты через пробел (например, 2 3, где 2 - число по горизонтали, а 3 - по вертикали). Введите 'q' для выхода.")
        while not self.game_over:
            self.show()
            user_input = input("Введите координаты (или 'q' для выхода): ").strip()
            if user_input.lower() == 'q':
                print("Игра завершена по команде пользователя.")
                break

            try:
                x, y = map(int, user_input.split())
                self.open_cell(x-1, y-1)
            except ValueError:
                print("Неверный формат. Введите два числа через пробел.")



game = GamePole(10, 12)
game.run()
