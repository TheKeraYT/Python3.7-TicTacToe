#-----------------------------------------
# Автор - TheKeraYT                      |
# Python - 3.7                           |
# Название проекта: "Крестики-Нолики"    |
# Язык: Русский                          |
#----------------------------------------|
# Даты выхода:                           |
# Pre-Alpha - 07.05.19                   |
# Alpha - 08.05.19                       |
# Beta - 09.05.19                        |
# ---------------------------------------|
# Код писался в Sublime Text 3           |
#-----------------------------------------
from tkinter import *
import random
class Square():
    """ задает квадраты(клетки) """
    def __init__(self, master, root, num, row, column):
        self.master = master
        self.square_num = num
        self.msg = StringVar()
        self.lbl = Label(root, textvariable=self.msg, font="FreeSerifBold 75", bg="white")
        self.lbl.grid(row=row, column=column, sticky=NSEW, padx=5, pady=5)
    def unbind(self):
        self.lbl.unbind("<Button-1>")
    def bind(self):
        self.lbl.bind("<Button-1>", self.choice)
    def set_msg(self, txt):
        self.msg.set(txt)
    def choice(self, event):
        self.master.turn_user(self.square_num)
    def cfg(self, color):
        self.lbl.configure(bg=color)
class Application(Frame):
    def __init__(self, master):
        super(Application, self).__init__(master)
        self.master = master
        self.master.config(bg="#D9D9D9")
        # константы
        self.wins = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
                     (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        self.board_start = ['_'] * 9
        self.free_squares_start = [x for x in range(9)]
        self.choice_pc1 = [0, 2, 6, 8]
        self.choice_pc2 = [1, 3, 5, 7]
        # статистика игры
        self.drawn_game = 0
        self.user_win = 0
        self.pc_win = 0
        self.create_widgets()
    def create_widgets(self):
        # блок слева
        frame_left = Frame(self.master)
        frame_left.grid(row=0, column=0, padx=5, pady=5, sticky=N)
        # статистика
        statistics = LabelFrame(frame_left, text=" Статистика ")
        statistics.grid()
        self.stat_msg = StringVar()
        stat_lbl = Label(statistics, textvariable=self.stat_msg, justify=LEFT, width=15)
        stat_lbl.grid(padx=0)
        self.stat_msg.set(
            'Сыграно игр: %s.\nИз них:\n  побед: %s;\n  поражений: %s;\n  ничьих: %s.' %
            (self.user_win + self.pc_win + self.drawn_game,
             self.user_win, self.pc_win, self.drawn_game)
        )
        # блок в центре
        frame_center = Frame(self.master)
        frame_center.grid(row=0, column=1, padx=10, pady=5, sticky=N)
        step_choice = LabelFrame(frame_center, text=" Выбрать ход ")
        step_choice.grid(ipadx=5)
        self.step = IntVar()
        self.step.set(0)
        step0 = Radiobutton(step_choice, text='Случайным', variable=self.step, value=0)
        step1 = Radiobutton(step_choice, text='Первым', variable=self.step, value=1)
        step2 = Radiobutton(step_choice, text='Вторым', variable=self.step, value=2)
        step0.grid(ipady=2, sticky=W)
        step1.grid(ipady=3, sticky=W)
        step2.grid(ipady=2, sticky=W)
        # блок справа
        right_frame = Frame(self.master)
        right_frame.grid(row=0, column=2, padx=5, pady=5)
        # Выбор знака
        sign_choice = LabelFrame(right_frame, text=" Выбор знака ")
        sign_choice.grid(ipadx=5)
        self.user_choice = StringVar()
        self.user_choice.set('0')
        sign0 = Radiobutton(sign_choice, text='Ваш знак "0"', variable=self.user_choice, value='0')
        sign1 = Radiobutton(sign_choice, text='Ваш знак "X"', variable=self.user_choice, value='X')
        sign0.grid()
        sign1.grid()
        # кнопка старт
        self.btn = Button(right_frame, text="Старт")
        self.btn.bind("<Button-1>", self.start)
        self.btn.grid(pady=6, sticky=NSEW)
        # Статус игры
        status = LabelFrame(self.master, text=" Статус игры ")
        status.grid(row=1, column=0, columnspan=3, padx=5, sticky=NSEW)
        self.status_msg = StringVar()
        status_lbl = Label(status, textvariable=self.status_msg)
        status_lbl.grid()
        self.status_msg.set('Добро пожаловать в игру "Крестики - Нолики"!')
        # squares
        self.squares = {}
        num = 0
        for row in range(2, 5):
            for column in range(0, 3):
                self.squares[num] = Square(self, self.master, num, row, column)
                num += 1
        self.widgets = [sign0, sign1, step0, step1, step2, self.btn]
    def start(self, *args):
        self.choice_pc = None
        self.flag_end = False
        self.free_squares = self.free_squares_start[:]
        self.board = self.board_start[:]
        self.status_msg.set('Осторожно! Игра активирована! Удачи!')
        for square_num in range(9):
            square = self.squares[square_num]
            square.bind()
            square.set_msg('')
            square.cfg('white')
        if self.user_choice.get() == '0':
            self.user_sign, self.pc_sign = '0', 'X'
        else:
            self.user_sign, self.pc_sign = 'X', '0'
        uc = self.step.get()
        if uc == 2:
            self.turn_pc()
        elif uc == 0:
            rnd = random.choice([1, 2])
            if rnd == 2:
                self.turn_pc()
        self.widget_state()
        self.btn.unbind("<Button-1>")
    def widget_state(self, wst=DISABLED):
        for widget in self.widgets:
            widget.config(state=wst)
    def unbind_squares(self):
        for square_num in self.free_squares:
            self.squares[square_num].unbind()
    def greet_winner(self, sign):
        """ поздравления """
        if sign == self.user_sign:
            self.status_msg.set('Поздравляю с победой!')
            self.user_win += 1
        else:
            self.status_msg.set('Победа за компьютером! Ну как так?!!!')
            self.pc_win += 1
        self.flag_end = True
    def show_win(self, win, sign):
        if sign == self.user_sign:
            color = 'green'
        else:
            color = 'red'
        for square_num in win:
            square = self.squares[square_num]
            square.cfg(color)
    def game_over(self):
        """ окончание игры """
        self.stat_msg.set(
            'Сыграно игр: %s.\nИз них:\n  побед: %s;\n  поражений: %s;\n  ничьих: %s.' %
            (self.user_win + self.pc_win + self.drawn_game,
             self.user_win, self.pc_win, self.drawn_game)
        )
        self.widget_state(NORMAL)
        self.btn.bind("<Button-1>", self.start)
    def test_win(self, sign):
        """ определение исхода игры """
        for a, b, c in self.wins:
            if self.board[a] == sign and self.board[b] == sign and self.board[c] == sign:
                self.show_win((a, b, c), sign)
                self.unbind_squares()
                self.greet_winner(sign)
                self.game_over()
                return
        if not self.free_squares:
            self.status_msg.set('Ничья. Вы точно можете лучше!')
            self.flag_end = True
            self.drawn_game += 1
            for square_num in range(9):
                square = self.squares[square_num]
                square.cfg('yellow')
            self.game_over()
    def is_win(self, sign, iboard):
        for a, b, c in self.wins:
            if iboard[a] == sign and iboard[b] == sign and iboard[c] == sign:
                return True
        return False
    def find_best_turn(self, sign):
        for iturn in self.free_squares:
            iboard = self.board[:]
            iboard[iturn] = sign
            res = self.is_win(sign, iboard)
            if res:
                return iturn
        return None
    def default_choice(self):
        if not self.choice_pc:
            self.choice_pc = [4]
            random.shuffle(self.choice_pc1)
            random.shuffle(self.choice_pc2)
            self.choice_pc.extend(self.choice_pc1)
            self.choice_pc.extend(self.choice_pc2)
        for iturn in self.choice_pc:
            if iturn in self.free_squares:
                return iturn
    def turn_pc(self):
        """ ход пк """
        square_num = self.find_best_turn(self.pc_sign)
        if square_num == None:
            square_num = self.find_best_turn(self.user_sign)
            if square_num == None:
                square_num = self.default_choice()
        self.turn(square_num, self.pc_sign)
    def change_board(self, square_num, sign):
        """ заполнение клетки знаком """
        self.board[square_num] = sign
        self.free_squares.remove(square_num)
    def turn(self, square_num, sign):
        square = self.squares[square_num]
        square.unbind()
        square.set_msg(sign)
        self.change_board(square_num, sign)
        self.test_win(sign)
    def turn_user(self, square_num):
        """ ход игрока """
        self.turn(square_num, self.user_sign)
        if not self.flag_end:
            self.turn_pc()
def main():
    root = Tk()
    root.title('Игра "Крестики - Нолики"')
    root.resizable(FALSE, FALSE)
    app = Application(root)
    root.mainloop()
if __name__ == '__main__':
    main()
