from random import shuffle


class Dominoes:
    stock, computer, player, snake, status = [], [], [], [], str
    turn = ("Status: It's your turn to make a move. Enter your command.",
            'Status: Computer is about to make a move. Press Enter to continue...')

    def main(self):
        self.stock = [[i, j] for i in range(7) for j in range(i, 7)]
        shuffle(self.stock)
        self.computer, self.player = (lambda s: (sorted(s[:7]), sorted(s[7:])))([self.stock.pop() for _ in range(14)])
        self.snake = [self.computer.pop()] if self.computer[-1] > self.player[-1] else [self.player.pop()]
        self.status = (self.turn[0], self.turn[1])[len(self.computer) > len(self.player)]
        self.end()

    def shift(self):
        current_hand, illegal = (self.computer, self.player)[self.status == self.turn[0]], False
        if self.status == self.turn[0]:
            try:
                if abs(action := int(input())) > len(self.player) or (illegal := not self.move(action, self.player)):
                    raise ValueError
            except ValueError:
                print(('Invalid input.', 'Illegal move.')[illegal], 'Please try again.'), self.shift()
        else:
            input(), self.move(self.bot(), self.computer)
        self.status = (self.turn[0], self.turn[1])[self.status == self.turn[0]]
        self.end()

    def bot(self):
        if not sum(i.count(self.snake[-1][1]) + i.count(self.snake[0][0]) for i in self.computer):
            return 0
        nums = [i for j in self.snake + self.computer for i in j]
        pairs = [i for i in self.computer if self.snake[0][0] in i or self.snake[-1][1] in i]
        best = (lambda n: pairs[n.index(max(n))])([nums.count(i[0]) + nums.count(i[1]) for i in pairs])
        return (-(self.computer.index(best) + 1), self.computer.index(best) + 1)[self.snake[-1][1] in best]

    def move(self, action, current_hand):
        if action > 0:
            if self.snake[-1][1] in current_hand[action - 1]:
                self.snake.insert(len(self.snake), current_hand.pop(action - 1)
                                  if self.snake[-1][1] == current_hand[action - 1][0]
                                  else list(reversed(current_hand.pop(action - 1))))
                return True
        elif action < 0:
            if self.snake[0][0] in current_hand[abs(action) - 1]:
                self.snake.insert(0, current_hand.pop(abs(action) - 1)
                                  if self.snake[0][0] == current_hand[abs(action) - 1][1]
                                  else list(reversed(current_hand.pop(abs(action) - 1))))
                return True
        else:
            current_hand.append(self.stock.pop()) if len(self.stock) else None
            return True
        return False

    def end(self):
        if not len(self.player) or not len(self.computer):
            self.status = 'Status: The game is over. ' + ('The computer won!', 'You won!')[not len(self.player)]
        elif sum(n.count(self.snake[0][0]) for n in self.snake if self.snake[0][0] == self.snake[-1][1]) == 8:
            self.status = "Status: The game is over. It's a draw!"
        self.state(), self.shift() if self.status in (self.turn[0], self.turn[1]) else self.state(), exit()

    def state(self):
        print('=' * 70, f'\nStock size: {len(self.stock)}\nComputer pieces: {len(self.computer)}\n\n',
              *self.snake if len(self.snake) < 7 else f'{self.snake[0]}{self.snake[1]}{self.snake[2]}'
              f'...{self.snake[-3]}{self.snake[-2]}{self.snake[-1]}', sep='')
        print('\nYour pieces:', *(f'\n{i + 1}:{self.player[i]}' for i in range(len(self.player))), f'\n\n{self.status}')


Dominoes().main()
