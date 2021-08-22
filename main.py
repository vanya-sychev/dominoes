import random


class Dominoes:
    def __init__(self):
        self.domino_set = [[left, right] for left in range(7)
                           for right in range(left, 7)]
        self.domino_list = None
        self.domino_snake = []
        self.status = None

    def distribution(self):
        while True:
            random.shuffle(self.domino_set)

            self.domino_list = [self.domino_set[:14], self.domino_set[14:21],
                                self.domino_set[21:]]

            self.domino_set = [i for i in self.domino_set
                               if i not in self.domino_list[0]
                               and i not in self.domino_list[1]
                               and i not in self.domino_list[2]]

            double_domino = [[i, i] for i in range(7)]

            for i in double_domino[::-1]:
                if i in self.domino_list[1]:
                    self.domino_snake.append(i)
                    self.domino_list[1].remove(i)
                    break
                elif i in self.domino_list[2]:
                    self.domino_snake.append(i)
                    self.domino_list[2].remove(i)
                    break

            self.status = "computer" \
                if len(self.domino_list[1]) > len(self.domino_list[2]) \
                else "player"

            if len(self.domino_snake) == 0:
                continue
            else:
                break

    def interface(self):
        print("=" * 70)
        print(f"Stock size: {len(self.domino_list[0])}")
        print(f"Computer pieces: {len(self.domino_list[1])}\n")

        if len(self.domino_snake) > 6:
            print(*self.domino_snake[:3], "...", *self.domino_snake[-3:],
                  sep='')
        else:
            print(*self.domino_snake, sep='')

        print("\nYour pieces:")

        number_of_figures = [str(i) for i in range(1, 21)]
        for i in range(len(self.domino_list[2])):
            print(number_of_figures[i] + ":" + str(self.domino_list[2][i]))

    def player_turn(self):
        print("\nStatus: It's your turn to make a move. Enter your command.")

        while True:
            move = input()

            if move in [str(i) for i in range(len(self.domino_list[2]) + 1)] \
                    or move in \
                    [str(-i) for i in range(1, len(self.domino_list[2]) + 1)]:
                if self.regulations(self.domino_list[2], move) == "Error":
                    print("Illegal move. Please try again.")
                    continue
                else:
                    break
            else:
                print("Invalid input. Please try again.")

        self.interface()

    def computer_turn(self):
        print("\nStatus: Computer is about to make a move. "
              "Press Enter to continue...")
        input()

        self.artificial_intelligence()

        self.interface()

    def regulations(self, queue, move):
        if int(move) < 0:
            if self.domino_snake[0][0] == queue[abs(int(move)) - 1][1]:
                self.domino_snake.insert(0, queue[abs(int(move)) - 1])
                queue.pop(abs(int(move)) - 1)
            elif self.domino_snake[0][0] == queue[abs(int(
                    move)) - 1][::-1][1]:
                self.domino_snake.insert(0, queue[abs(int(move)) - 1][::-1])
                queue.pop(abs(int(move)) - 1)
            else:
                return "Error"
        elif int(move) > 0:
            if self.domino_snake[-1][-1] == queue[int(move) - 1][0]:
                self.domino_snake.append(queue[int(move) - 1])
                queue.pop(int(move) - 1)
            elif self.domino_snake[-1][-1] == queue[int(move) - 1][::-1][0]:
                self.domino_snake.append(queue[int(move) - 1][::-1])
                queue.pop(int(move) - 1)
            else:
                return "Error"
        elif int(move) == 0 and len(self.domino_list[0]) != 0:
            n = random.choice(self.domino_list[0])
            queue.append(n)
            self.domino_list[0].remove(n)
        else:
            return "Error"

    def end_game(self):
        counter = 0
        if len(self.domino_snake) > 3 \
                and self.domino_snake[0][0] == self.domino_snake[-1][-1]:
            for i in range(len(self.domino_snake)):
                if self.domino_snake[i].count(self.domino_snake[0][0]) == 1:
                    counter += 1
                elif self.domino_snake[i].count(self.domino_snake[0][0]) == 2:
                    counter += 2

        numbers_1 = []
        for i in range(len(self.domino_list[1])):
            for j in range(2):
                numbers_1.append(self.domino_list[1][i][j])

        numbers_2 = []
        for i in range(len(self.domino_list[2])):
            for j in range(2):
                numbers_2.append(self.domino_list[2][i][j])

        if len(self.domino_list[1]) == 0:
            print("\nStatus: The game is over. The computer won!")
            return "Stop"
        elif len(self.domino_list[2]) == 0:
            print("\nStatus: The game is over. You won!")
            return "Stop"
        elif self.domino_snake[0][0] == self.domino_snake[-1][-1] \
                and counter == 8:
            print("\nStatus: The game is over. It's a draw!")
            return "Stop"
        elif (self.domino_snake[0][0] not in numbers_1
              or self.domino_snake[-1][-1] not in numbers_1) \
                and len(self.domino_list[0]) == 0:
            print("\nStatus: The game is over. It's a draw!")
            return "Stop"
        elif (self.domino_snake[0][0] not in numbers_2
              or self.domino_snake[-1][-1] not in numbers_2) \
                and len(self.domino_list[0]) == 0:
            print("\nStatus: The game is over. It's a draw!")
            return "Stop"

    def artificial_intelligence(self):
        number_of_digits = {'0': 0, '1': 0, '2': 0, '3': 0,
                            '4': 0, '5': 0, '6': 0}

        for i in range(len(self.domino_list[1])):
            for j in range(len(self.domino_list[1][i])):
                if self.domino_list[1][i][j] == 0:
                    number_of_digits['0'] += 1
                elif self.domino_list[1][i][j] == 1:
                    number_of_digits['1'] += 1
                elif self.domino_list[1][i][j] == 2:
                    number_of_digits['2'] += 1
                elif self.domino_list[1][i][j] == 3:
                    number_of_digits['3'] += 1
                elif self.domino_list[1][i][j] == 4:
                    number_of_digits['4'] += 1
                elif self.domino_list[1][i][j] == 5:
                    number_of_digits['5'] += 1
                elif self.domino_list[1][i][j] == 6:
                    number_of_digits['6'] += 1

        score_score = {}
        for i in range(len(self.domino_list[1])):
            score_score[
                str(self.domino_list[1][i])] \
                = number_of_digits[
                      str(self.domino_list[1][i][0])] + number_of_digits[
                str(self.domino_list[1][i][1])]

        list_of_points = []
        for i in range(len(self.domino_list[1])):
            list_of_points.append(score_score[str(self.domino_list[1][i])])

        list_of_points.sort()

        move = 0
        for i in range(len(self.domino_list[1]) - 1, -1, -1):
            if self.regulations(self.domino_list[1], i) != "Error":
                move = i
                break
            elif self.regulations(self.domino_list[1], -i) != "Error":
                move = -i
                break

        return move

    def start(self):
        self.distribution()
        self.interface()

        while True:
            if self.status == "computer":
                self.computer_turn()
                if self.end_game() == "Stop":
                    break
                self.status = "player"
            elif self.status == "player":
                self.player_turn()
                if self.end_game() == "Stop":
                    break
                self.status = "computer"


dominoes = Dominoes()
dominoes.start()
