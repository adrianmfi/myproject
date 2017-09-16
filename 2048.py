import tkinter as tk
import random
import math
import itertools

ROWS = 4
COLS = 4
COLORS =["ivory3", "white smoke","old lace", "peach puff", "tan1","tomato","tomato3","gold"]


class Game2048():
    
    def __init__(self, highscore = 0):
        self.is_finished = False
        self.score = 0
        self.highscore = highscore
        self.board = [[0 for i in range(COLS)] for j in range(ROWS)]
        self._place_randomly()
        

    def move_left(self):
        self._move(0)

    def move_down(self):
        self._move(1)
        
    def move_right(self):
        self._move(2)
        
    def move_up(self):
        self._move(3)
        
    def can_move(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    return False
        for row in range(ROWS):
            for col in range(COLS-1):
                if self.board[row][col] == self.board[row][col+1]:
                    return False
        for row in range(ROWS-1):
            for col in range(COLS):
                if self.board[row][col] == self.board[row+1][col]:
                    return False
        return True

    def _move(self, direction):
        self._rotate_board(direction)
        could_move = self._move_left()
        self._rotate_board(4-direction)
        self.highscore = max(self.score, self.highscore)
        if could_move and self._list_empty_tiles():
            self._place_randomly()
        if self.can_move():
            self.is_finished = True
        
        
    def _move_left(self):
        could_move = False
        for row in range(ROWS):
            startCol = 0
            checkCol = 1
            while checkCol < COLS:
                startValue = self.board[row][startCol]
                checkValue = self.board[row][checkCol]
                #If value found
                if checkValue != 0:
                    #If equal value or empty starting point
                    if startValue == checkValue or startValue == 0:
                        could_move = True
                        self.board[row][startCol] += checkValue
                        self.board[row][checkCol] = 0
                        if(startValue == checkValue):
                        
                            self.score += 2*startValue
                            startCol += 1
                    #Else if unequal value
                    else:
                        self.board[row][checkCol] = 0
                        self.board[row][startCol + 1] = checkValue
                        startCol += 1
                    checkCol = startCol +1
                #Empty spot on board
                else:
                    checkCol += 1
        return could_move
        
    def _place_randomly(self):
        empty_tiles = self._list_empty_tiles()
        rand_row, rand_col = empty_tiles[random.randrange(len(empty_tiles))]
        if random.randint(0,100) > 75:
            rand_val = 4
        else:
            rand_val = 2

        self.board[rand_row][rand_col] = rand_val
        

    def _rotate_board(self, num_rotations):
        for i in range(num_rotations):
            self.board = [list(i) for i in zip(*self.board[::-1])]

    def _list_empty_tiles(self):
        empty_tiles = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    empty_tiles.append([row,col])
        return empty_tiles    


class GUI2048():
    def __init__(self,root, handle_restart_clicked):
        self.root = root 
        self.root.wm_title("2048") 
        self.tiles = [[tk.Label(self.root,text = '',font=("Helvetica", 14), width = 8, bg = "ivory3") for i in range(COLS)] for i in range(ROWS)]
        self.scoreLabel1 = tk.Label(self.root, text = "Score:", font = ("Helvetica",14), width = 5)
        self.scoreLabel2 = tk.Label(self.root, text = "0", font = ("Helvetica",12),width = 5, justify =tk.LEFT)
        self.scoreLabel1.grid(row = ROWS, column = 0)
        self.scoreLabel2.grid(row = ROWS, column = 1)
        
        self.highScoreLabel1 = tk.Label(self.root, text = "Highscore:", font = ("Helvetica",8),width = 8)
        self.highScoreLabel2 = tk.Label(self.root, text = "", font = ("Helvetica",8),width = 8)
        self.highScoreLabel1.grid(row = ROWS+1, column = 0)
        self.highScoreLabel2.grid(row = ROWS+1, column = 1)
        
        self.gameOverLabel1 = tk.Label(self.root, text = "", font = ("Helvetica",12),width = 5)
        self.gameOverLabel2 = tk.Label(self.root, text = "", font = ("Helvetica",12),width = 5)
        self.gameOverLabel1.grid(row = ROWS, column = COLS-2)
        self.gameOverLabel2.grid(row = ROWS, column = COLS-1)
        
        self.restartButton = tk.Button(self.root,text ="Restart")     
        self.restartButton.grid(row = ROWS+1,column = COLS-1)
        self.restartButton.bind('<Button-1>', handle_restart_clicked)

        for i in range(ROWS):
            for j in range(COLS):
                self.tiles[i][j].grid(row = i, column = j,padx = 2,pady = 2,ipady = 10)


    def update_tiles(self,board):
        for row in range(ROWS):
            for col in range(COLS):
                tile = board[row][col]
                    
                #Update tile background color
                if math.log(tile+1,2) < len(COLORS):
                    self.tiles[row][col].config(bg = COLORS[int(math.log(tile+1,2))])
                else:
                    self.tiles[row][col].config(bg = COLORS[-1])
                #Update tile text color
                if tile < 8:
                    self.tiles[row][col].config(fg = "dim gray")
                else:
                    self.tiles[row][col].config(fg = "white")
                #Update tile text
                if tile == 0:
                    self.tiles[row][col].config(text = '')
                else:
                    self.tiles[row][col].config(text = tile)
                
    def update_scores(self,score,highscore):        
        self.scoreLabel2.config(text = score)
        self.highScoreLabel2.config(text = highscore)

    def show_game_over(self):
        self.gameOverLabel1.config(text='Game')
        self.gameOverLabel2.config(text='over')

    def clear_game_over(self):
        self.gameOverLabel1.config(text='')
        self.gameOverLabel2.config(text='')
        

class Controller2048():
    def __init__(self):      
        try:
            with open("highscores2048.txt") as highscores:
                highscore = int(highscores.read())
        except FileNotFoundError as e:
            print(e)
            highscore = 0

        self.root = tk.Tk()
        self.game = Game2048(highscore)
        self.gui = GUI2048(self.root,self.handle_restart_clicked)
        self.gui.update_tiles(self.game.board)
        self.gui.update_scores(self.game.score,self.game.highscore)

    def play_with_keyboard(self):
        self.root.bind("<Left>", self.handle_button_pressed)
        self.root.bind("<Up>", self.handle_button_pressed)
        self.root.bind("<Right>", self.handle_button_pressed)
        self.root.bind("<Down>", self.handle_button_pressed)
        self.root.mainloop()
    
    def handle_button_pressed(self,event):
        if self.game.is_finished:
            return

        if event.keysym == 'Left':
            self.game.move_left()
        elif event.keysym == 'Up':
            self.game.move_up()
        elif event.keysym == 'Right':
            self.game.move_right()
        elif event.keysym == 'Down':
            self.game.move_down()
        else:
            return

        if self.game.is_finished:
            self.gui.show_game_over()
        self.gui.update_tiles(self.game.board)
        self.gui.update_scores(self.game.score, self.game.highscore)
        
    def handle_restart_clicked(self,event):
        self.game = Game2048(self.game.highscore)
        self.gui.update_tiles(self.game.board)
        self.gui.update_scores(self.game.score,self.game.highscore)
        self.gui.clear_game_over()
        
def main():
    controller = Controller2048()
    controller.play_with_keyboard()

if __name__ == "__main__":                
    main()