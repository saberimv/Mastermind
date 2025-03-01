#Marzieh Saberi
#Date: Nov, Dec 2023
#Mastermind: 10 colors, 5 holes
#-------------------------------------------------------------

from datetime import date
import time
import turtle
import random
import csv
import os.path
import threading

screen = turtle.Screen()
pen = turtle.Turtle()
header = turtle.Turtle()
code_breakers_turtle = turtle.Turtle()
name_turtle = turtle.Turtle()
time1_turtle = turtle.Turtle()
time2_turtle = turtle.Turtle()

canvas = screen.getcanvas()
root = canvas.winfo_toplevel()

pen.hideturtle()
header.hideturtle()
code_breakers_turtle.hideturtle()
name_turtle.hideturtle()
time1_turtle.hideturtle()
time2_turtle.hideturtle()
    
pen.speed(0)
header.speed(0)    
code_breakers_turtle.speed(0)
name_turtle.speed(0)
time1_turtle.speed(0)
time2_turtle.speed(0)

color_count = 10
hole_count = 5
code_breaker_count = 5

about_position = [155, 390]
about_size = [80, 20]

how_position = [170, 365]
how_size = [65, 20]

history_position = [170, 340]
history_size = [65, 20]

new_game_position = [170, 315]
new_game_size = [65, 20]

code_breakers_box_position = [-240, 390]
code_breakers_box_size = [130,90]

colors = ["red", "orange", "green", "yellow", "cyan", "darkviolet", "deeppink", "lime", "blue", "saddlebrown"]
colored_peg_box_position = [-200, 290]
colored_peg_box_size = [400, 27]
colored_peg_center = [-180,276]
colored_peg_space = 40

name_position = [-240, 250]
name_size = [120,20]

time_position = [-240, 225]
time_size = [120,20]

code_peg_radius = 10
code_maker_peg_center = [-20,240]
cod_maker_peg_space = 40

show_position = [180,250]
show_size = [38,20]
hint_position = [188,225]
hint_size = [25,20]
hint_count = 3

step_center = [-230,163]
step_height = 45
step_count = 12
point_counter = 0

key_peg_radius = 5
key_peg_center = [-150,170]
key_peg_space = 20

code_breaker_peg_center = [-20,170]
code_breaker_peg_space = 40

clear_position = [170,180]
clear_size = [33,20]
ok_position = [208,180]
ok_size = [22,20]

code_breakers = []

time_limit = 10*60
font_normal = ('', 8, 'normal')
font_bold = ('', 8, 'bold')
font_underline = ('', 8, 'underline')

#Code_Breaker Class-------------------------------------------------------------
class Code_Breaker:
    def __init__(self, starting_time, turn, name, score, time, hint, game_result, code_maker_peg, code_breaker_peg, key_peg, step_counter, colors_omitted):
        self.starting_time = starting_time
        self.turn = turn
        self.name = name
        self.score = score
        self.time = time
        self.hint = hint
        self.game_result = game_result
        
        self.code_maker_peg = code_maker_peg
        if code_maker_peg == []:
            self.AppendCodeMakerPeg()
        
        self.code_breaker_peg = code_breaker_peg
        self.key_peg = key_peg
        self.step_counter = step_counter

        self.colors_omitted = []
        self.colors_omitted = colors_omitted

    def __str__(self):
        return f"Name: {self.name}\nScore: {self.score}\nTime: {self.time//60}:{self.time%60}"

    def AppendCodeMakerPeg(self):
        self.code_maker_peg = []
        for _ in range(hole_count):
            self.code_maker_peg.append(random.choice([i for i in range(color_count)]))
        
    def AppendCodeBreakerPeg(self, color):
        if point_counter == 0:
            self.code_breaker_peg.append([])
        self.code_breaker_peg[-1].append(color)
        
    def AppendKeyBreakerPeg(self):
        #Color: 0:bagel, 1:pico(gold), 2:fermi(black)
        resultList = [-1,-1,-1,-1,-1]
        maker_counter = [0,0,0,0,0]
        breaker_counter = [0,0,0,0,0]
        position = []
        
        for i in range (hole_count):
            position.append([])
            counter = 0
            for j in range(hole_count):
                if self.code_breaker_peg[-1][i] == self.code_breaker_peg[-1][j]:
                    counter += 1
                    position[-1].append(j)
            breaker_counter[i] = counter
            
        for i in range (hole_count):
            counter = 0
            for j in range(hole_count):
                if self.code_breaker_peg[-1][i] == self.code_maker_peg[j]:
                    counter += 1
            maker_counter[i] = counter
        
        for i in range (hole_count):
            if resultList[i] != -1:
                continue
            
            for j in position[i]:
                result = ''
                for k in range (hole_count):
                    if(self.code_breaker_peg[-1][j] == self.code_maker_peg[k]):
                        if j == k:
                            result += '2'
                        else:
                            result += '1'                    
                if '2' in result:
                    resultList[j] = 2
                else:
                    resultList[j] = 1

            if breaker_counter[i] > maker_counter[i]:
                a = breaker_counter[i] - maker_counter[i]
                for j in position[i]:
                    if a == 0:
                        break
                    if resultList[j] == 1:
                        resultList[j] = 0
                        a -= 1
                    
        resultList.sort(reverse=True)
        self.key_peg.append([])
        self.key_peg[-1] = resultList.copy()
        return self.key_peg[-1]
    
    def CalculateScore(self):
        #Rules: black peg: 10 score//gold pig: 5 score//minute remained: 40 score//step remained: 40 score//win: 200 score//hint: -150 score
        score = 0
        for i in self.key_peg:
            for j in i:
                if j == 2:
                    score += 10
                if j == 1:
                    score += 5

        score -= self.hint * 150

        if self.game_result == "win":
            score += 200
            score += int(((time_limit - self.time)/60)*40)
            score += (step_count - self.step_counter - 1)*40

        if score < 0:
            score = 0
        elif score >= 1000:
            score = 1000
    
        self.score = score
        return score
    
    def CalculateTime(self):
        if int(time.time() - self.starting_time) >= time_limit:
            self.time = int(time_limit)        
        else:
            self.time = int(time.time() - self.starting_time)

#Check Click-------------------------------------------------------------
def CheckClick(x, y):
    global point_counter
    
    #About program
    if x >= about_position[0] and x <= about_position[0]+about_size[0] and y <= about_position[1] and y >= about_position[1]-about_size[1]:
        turtle.TK.messagebox.showinfo(title="About Program", message="Mastermind.\nProgrammed by Marzieh Saberi, on Nov, Dec 2023.")

    #How to play
    elif x >= how_position[0] and x <= how_position[0]+how_size[0] and y <= how_position[1] and y >= how_position[1]-how_size[1]:
        if os.path.isfile("Readme.txt"):
            os.startfile("Readme.txt")
        else:
            turtle.TK.messagebox.showinfo(title="How to play", message="Mastermind is a code-breaking game for two players.\nOne player becomes the codemaker, the other the codebreaker.\nThe codemaker chooses a pattern of five code pegs. The codebreaker tries to guess the pattern, in both order and color.")
        
    #History
    elif x >= history_position[0] and x <= history_position[0]+history_size[0] and y <= history_position[1] and y >= history_position[1]-history_size[1]:
        ShowHistory()
    
    #New Game
    elif x >= new_game_position[0] and x <= new_game_position[0]+new_game_size[0] and y <= new_game_position[1] and y >= new_game_position[1]-new_game_size[1]:
        if len(code_breakers) >= code_breaker_count:
            turtle.TK.messagebox.showinfo(title="No more player!", message="No more player!\nJust "+str(code_breaker_count)+" players can play this game!")
        elif code_breakers != [] and code_breakers[-1].turn:
            msg_box = turtle.TK.messagebox.askquestion('New Game', 'Are you sure you want to start a new game?',icon='warning')
            if msg_box == 'yes':
                ColoredPeg(1)
                EndProgram(1, 1)
                DecodingBoard()
                NewCodeBreaker(1)
                return
        else:
            ColoredPeg(1)
            DecodingBoard()
            NewCodeBreaker(1)
            return

    if code_breakers == [] or not code_breakers[-1].turn:
        return

    #Show
    if x >= show_position[0] and x <= show_position[0]+show_size[0] and y <= show_position[1] and y >= show_position[1]-show_size[1]:
        EndProgram(1)
           
    #Hint
    elif x >= hint_position[0] and x <= hint_position[0]+hint_size[0] and y <= hint_position[1] and y >= hint_position[1]-hint_size[1]:
        if(code_breakers[-1].hint >= hint_count):
            turtle.TK.messagebox.showinfo(title="No More Hint", message="No more hint!")
        else:
            code_breakers[-1].hint += 1
            CodeMakerPeg(4)

    #Colored Pegs
    for i in range(color_count):
        if (((x-(colored_peg_center[0]+(i*colored_peg_space)))**2)+((y - colored_peg_center[1])**2))**0.5 < code_peg_radius:
            if code_breakers[-1].colors_omitted[i] == 0:
                CodeBreakerPeg(2, code_breakers[-1].step_counter, i)
            break

    #Clear Buttons
    for i in range(step_count):
        if x >= clear_position[0] and x <= clear_position[0]+clear_size[0] and y <= clear_position[1]-(i*step_height) and y >= clear_position[1]-(i*step_height)-clear_size[1]:
            if i == code_breakers[-1].step_counter and point_counter != 0:
                CodeBreakerPeg(1, code_breakers[-1].step_counter, "")
                point_counter = 0
                del code_breakers[-1].code_breaker_peg[-1]
            break

    #Ok Buttons
    for i in range(step_count):
        if x >= ok_position[0] and x <= ok_position[0]+ok_size[0] and y <= ok_position[1]-(i*step_height) and y >= ok_position[1]-(i*step_height)-ok_size[1]:
            if i == code_breakers[-1].step_counter and point_counter == hole_count:
                KeyBreakerPeg(2, code_breakers[-1].step_counter)
                code_breakers[-1].step_counter += 1
                point_counter = 0
                
                if code_breakers[-1].step_counter == step_count and code_breakers[-1].game_result != "win":
                    code_breakers[-1].step_counter -= 1
                    EndProgram(1)
            break
    return

#Dot-------------------------------------------------------------
def Dot(turtle, x, y, radius, color):
    turtle.up()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.dot(radius, color)
    return

#Rectangle-------------------------------------------------------------
def Rectangle(turtle, x, y, width, height, font_color, bg_color, text):
    turtle.color(font_color, bg_color)
    turtle.up()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.begin_fill()    
    turtle.setheading(0)
    turtle.forward(width)
    turtle.setheading(270)
    turtle.forward(height)
    turtle.setheading(180)
    turtle.forward(width)
    turtle.setheading(90)
    turtle.forward(height)
    turtle.end_fill()
    turtle.up()
    if text != "":
        turtle.goto(x+5, y-17)
        turtle.pendown()
        turtle.write(text)
    return

#Write Text-------------------------------------------------------------
def WriteText(turtle, x, y, font_color, text, font=()):
    turtle.color(font_color)
    turtle.up()
    turtle.goto(x, y)
    turtle.pendown()
    turtle.write(text, font=font)
    return

#Make Header-------------------------------------------------------------
def MakeHeader():
    #Title
    WriteText(header, -80, 340, "black", "Mastermind", ("Times New Roman", 25, "bold"))

    #About Program & How to Play & Show History & New Game
    Rectangle(header, about_position[0], about_position[1], about_size[0], about_size[1], "black", "papayawhip", "About Program")
    Rectangle(header, how_position[0], how_position[1], how_size[0], how_size[1], "black", "papayawhip", "How to Play")
    Rectangle(header, history_position[0], history_position[1], history_size[0], history_size[1], "black", "papayawhip", "")
    WriteText(header, history_position[0]+15, history_position[1]-17, "black", "History", font_normal)
    Rectangle(header, new_game_position[0], new_game_position[1], new_game_size[0], new_game_size[1], "black", "papayawhip", "New Game")

    #Code Breakers Box
    UpdateCodeBreakersBox()
    
    #Colored Pegs
    WriteText(header, colored_peg_box_position[0]+100, colored_peg_box_position[1]+2, "black", "Left Click: select a color / Right Click: omit a color", font_normal)
    Rectangle(header, colored_peg_box_position[0], colored_peg_box_position[1], colored_peg_box_size[0], colored_peg_box_size[1], "darkgray", "whitesmoke", "")
    for i in range(color_count):
        Dot(header, colored_peg_center[0]+i*colored_peg_space, colored_peg_center[1], code_peg_radius*2, colors[i])
    
    return

#Decoding Board-------------------------------------------------------------
def DecodingBoard():
    #Name & Time
    Rectangle(name_turtle, name_position[0], name_position[1], name_size[0], name_size[1], "black", "floralwhite", "Name:")
    Rectangle(time1_turtle, time_position[0], time_position[1], time_size[0], time_size[1], "black", "floralwhite", "Time:")
    
    #Code Maker
    CodeMakerPeg(1)    
    
    #Show & Hint
    Rectangle(pen, show_position[0], show_position[1], show_size[0], show_size[1], "black", "whitesmoke", "Show")
    Rectangle(pen, hint_position[0], hint_position[1], hint_size[0], hint_size[1], "black", "whitesmoke", "Hint")

    #Steps
    for i in range (step_count):
        WriteText(pen, step_center[0], step_center[1]-i*step_height, "black", "Step"+str(i+1)+")", ("Times New Roman", 10, "bold"))

        #Key Pegs & Code Breaker Pegs
        KeyBreakerPeg(1, i)
        CodeBreakerPeg(1, i, "")

        #Clear & OK
        Rectangle(pen, clear_position[0], clear_position[1]-i*step_height, clear_size[0], clear_size[1], "black", "lightcyan", "Clear")
        Rectangle(pen, ok_position[0], ok_position[1]-i*step_height, ok_size[0], ok_size[1], "black", "lightcyan", "OK")

    return

#Colored Peg-------------------------------------------------------------
def ColoredPeg(parameter, index=0):
    #parameter: 1:Reset colors 2:Omit a color 3:Restore
    
    if (parameter == 1): #Reset colors
        for i in range(color_count):
            Dot(header, colored_peg_center[0]+i*colored_peg_space, colored_peg_center[1], code_peg_radius*2, colors[i])
            
    elif (parameter == 2): #Omit a color
        if code_breakers[-1].colors_omitted[index] == 0:
            code_breakers[-1].colors_omitted[index] = 1
        else:
            code_breakers[-1].colors_omitted[index] = 0
        
        if code_breakers[-1].colors_omitted[index] == 1:
            Dot(header, colored_peg_center[0]+index*colored_peg_space, colored_peg_center[1], code_peg_radius*2, "black")
        else:
            Dot(header, colored_peg_center[0]+index*colored_peg_space, colored_peg_center[1], code_peg_radius*2, colors[index])

    elif (parameter == 3): #Restore
        for i in range(color_count):
            if code_breakers[-1].colors_omitted[i] == 1:
                Dot(header, colored_peg_center[0]+i*colored_peg_space, colored_peg_center[1], code_peg_radius*2, "black")
    return

#Code Maker Peg-------------------------------------------------------------
def CodeMakerPeg(parameter):
    #parameter: 1:Clear 3:Show all 4:Show 1 peg(hint) 5:Show all the hints
    global code_maker_peg
    
    if (parameter == 1): #Clear
        for i in range (hole_count):
            Dot(pen, code_maker_peg_center[0]+i*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2, "black")
            Dot(pen, code_maker_peg_center[0]+i*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2-2, "gainsboro")
            WriteText(pen, code_maker_peg_center[0]+i*cod_maker_peg_space-2, code_maker_peg_center[1]-code_peg_radius, "black", "?", ("Times New Roman", 12, "bold"))

    elif (parameter == 3):   #Show all
        for i in range (hole_count):
            Dot(pen, code_maker_peg_center[0]+i*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2, 'black')
            Dot(pen, code_maker_peg_center[0]+i*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2-2, colors[code_breakers[-1].code_maker_peg[i]])

    elif (parameter == 4):   #Show 1 peg (hint)
        Dot(pen, code_maker_peg_center[0]+(code_breakers[-1].hint-1)*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2, 'black')
        Dot(pen, code_maker_peg_center[0]+(code_breakers[-1].hint-1)*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2-2, colors[code_breakers[-1].code_maker_peg[code_breakers[-1].hint-1]])

    elif (parameter == 5):   #Show all the hints
        for i in range (code_breakers[-1].hint):
            Dot(pen, code_maker_peg_center[0]+i*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2, 'black')
            Dot(pen, code_maker_peg_center[0]+i*cod_maker_peg_space, code_maker_peg_center[1], code_peg_radius*2-2, colors[code_breakers[-1].code_maker_peg[i]])
    return

#Omit Color-------------------------------------------------------------
def OmitColor(x, y):
    if code_breakers == [] or not code_breakers[-1].turn:
        return
            
    for i in range(color_count):
        if (((x-(colored_peg_center[0]+(i*colored_peg_space)))**2)+((y - colored_peg_center[1])**2))**0.5 < code_peg_radius:
            ColoredPeg(2, i)            
            break
    return

#Code Breaker Peg-------------------------------------------------------------
def CodeBreakerPeg(parameter, step, color):
    #parameter: 1:Clear 2:Color 3:Restore
    global point_counter
    
    if parameter == 1: #Clear
        for i in range (hole_count):
            Dot(pen, code_breaker_peg_center[0]+i*code_breaker_peg_space, code_breaker_peg_center[1]-step*step_height, code_peg_radius*2, "black")
            Dot(pen, code_breaker_peg_center[0]+i*code_breaker_peg_space, code_breaker_peg_center[1]-step*step_height, code_peg_radius*2-2, "white")
            
    elif parameter == 2:   #Color
        if point_counter != hole_count:
            Dot(pen, code_breaker_peg_center[0]+point_counter*code_breaker_peg_space, code_breaker_peg_center[1]-step*step_height, code_peg_radius*2, colors[color])
            code_breakers[-1].AppendCodeBreakerPeg(color)
            point_counter += 1
            
    elif parameter == 3:   #Restore
        s_counter = 0
        for item1 in code_breakers[-1].code_breaker_peg:
            p_counter = 0
            for item2 in item1:
                Dot(pen, code_breaker_peg_center[0]+p_counter*code_breaker_peg_space, code_breaker_peg_center[1]-s_counter*step_height, code_peg_radius*2, colors[item2])
                p_counter += 1
            s_counter += 1
    return

#Key Breaker Peg-------------------------------------------------------------
def KeyBreakerPeg(parameter, step):
    #parameter: 1:Create 2:Color 3:Restore
    
    if(parameter == 1): #Create
        for i in range (hole_count):
            Dot(pen, key_peg_center[0]+i*key_peg_space, key_peg_center[1]-step*step_height, key_peg_radius*2, "black")
            Dot(pen, key_peg_center[0]+i*key_peg_space, key_peg_center[1]-step*step_height, key_peg_radius*2-2, "white")
            
    elif(parameter == 2):   #Color
        code_breakers[-1].AppendKeyBreakerPeg()
        black_counter = 0
        for i in range(len(code_breakers[-1].key_peg[-1])):
            if code_breakers[-1].key_peg[-1][i] == 2:
                Dot(pen, key_peg_center[0]+i*key_peg_space, key_peg_center[1]-step*step_height, key_peg_radius*2, "black")
                black_counter += 1
            elif code_breakers[-1].key_peg[-1][i] == 1:
                Dot(pen, key_peg_center[0]+i*key_peg_space, key_peg_center[1]-step*step_height, key_peg_radius*2, "gold")

        if(black_counter == hole_count):    #win the game
            EndProgram(2)
            
    elif parameter == 3:   #Restore
        s_counter = 0
        for item1 in code_breakers[-1].key_peg:
            p_counter = 0
            for item2 in item1:
                if item2 == 2:
                    Dot(pen, key_peg_center[0]+p_counter*key_peg_space, key_peg_center[1]-s_counter*step_height, key_peg_radius*2, "black")
                elif item2 == 1:
                    Dot(pen, key_peg_center[0]+p_counter*key_peg_space, key_peg_center[1]-s_counter*step_height, key_peg_radius*2, "gold")
                p_counter += 1
            s_counter += 1
    return

#New Code Breaker-------------------------------------------------------------
def NewCodeBreaker(parameter):
    #parameter: 1:Create New 2:Restore
    global code_breakers
    global point_counter

    if parameter == 1:  #Create New
        while True:
            name = screen.textinput("Enter Name", "Player "+str(len(code_breakers)+1)+".\nEnter Name:")
            if name == "" or name == None:
                turtle.TK.messagebox.showinfo(title="", message="To start a new game, press \"New Game\" button!")
                return
            else:
                break

        #starting_time, turn, name, score, time, hint, game_result, code_maker_peg, code_breaker_peg, key_peg, step_counter
        code_breaker = Code_Breaker(int(time.time()), True, name, 0, 0, 0, "lose", [], [], [], 0, [0 for _ in range(color_count)])
        code_breakers.append(code_breaker)
    
        point_counter = 0
        UpdateNameBox()
    
        thread_1 = threading.Thread(target = UpdateTimeBox, daemon = True)
        thread_1.start()
    
    elif parameter == 2:    #Restore saved game
        with open("SavedGame.txt", "r") as file:
            lines = file.readlines()
        lines = [line.rstrip('\n') for line in lines]
        
        code_maker_peg = lines[7][1:len(lines[7])-1].replace(',', '').split(' ')
        code_maker_peg = [int(item) for item in code_maker_peg]
        
        if lines[8] == '[]':
            code_breaker_peg = []
        else:
            list_ = lines[8][1:len(lines[8])-1].replace(',', '').split(']')
            list_.remove('')
            list_ = [item.lstrip()[1:].split(' ') for item in list_]
            code_breaker_peg = []
            for item in list_:
                code_breaker_peg.append([int(i) for i in item])
            
        if lines[9] == '[]':
            key_peg = []
        else:
            list_ = lines[9][1:len(lines[8])-1].replace(',', '').split(']')
            list_.remove('')
            list_ = [item.lstrip()[1:].split(' ') for item in list_]
            key_peg = []
            for item in list_:
                key_peg.append([int(i) for i in item])

        colors_omitted = lines[11][1:len(lines[11])-1].replace(',', '').split(' ')
        colors_omitted = [int(item) for item in colors_omitted]
            
        #starting_time, turn, name, score, time, hint, game_result, code_maker_peg, code_breaker_peg, key_peg, step_counter, colors_omitted
        code_breaker = Code_Breaker(int(time.time()-int(lines[4])), bool(lines[1]), lines[2], int(lines[3]), int(lines[4]), int(lines[5]), lines[6], code_maker_peg, code_breaker_peg, key_peg, int(lines[10]), colors_omitted)
        code_breakers.append(code_breaker)

        point_counter = 0        
        UpdateNameBox()
        CodeMakerPeg(5)
        CodeBreakerPeg(3,0,0)
        KeyBreakerPeg(3,0)
        ColoredPeg(3)
    
        thread_1 = threading.Thread(target = UpdateTimeBox, daemon = True)
        thread_1.start()
        
        file = open("SavedGame.txt",'w')    #Clear SavedGame.txt file
        file.close()
    return

#Update Code Breakers Box-------------------------------------------------------------
def UpdateCodeBreakersBox():
    code_breakers_turtle.clear()
    Rectangle(code_breakers_turtle, code_breakers_box_position[0], code_breakers_box_position[1], code_breakers_box_size[0], code_breakers_box_size[1], "black", "floralwhite", "")
    WriteText(code_breakers_turtle, code_breakers_box_position[0]+5, code_breakers_box_position[1]-15, "black", "Name\tScore\tTime", font_underline)
    
    if code_breakers != []:
        name = ""
        txt = ""
        for i in range(len(code_breakers)):
            name = code_breakers[i].name
            if(len(name) > 7):
                name = name[0:7]
            txt += "\n"+name+"\t"+str(code_breakers[i].score)+"\t"+str(code_breakers[i].time//60)+":"+str(code_breakers[i].time%60)
        WriteText(code_breakers_turtle, code_breakers_box_position[0]+5, code_breakers_box_position[1]-((len(code_breakers)+1)*14), "black", txt, font_normal)
    return

#Update Name Box-------------------------------------------------------------
def UpdateNameBox():
    name_turtle.clear()
    name = code_breakers[-1].name
    if(len(name) > 12):
        name = name[0:12]
    Rectangle(name_turtle, name_position[0], name_position[1], name_size[0], name_size[1], "black", "floralwhite", "Name: " + name)
    return

#Update Time Box-------------------------------------------------------------
def UpdateTimeBox():
    if code_breakers[-1].time == 0:
        start = time.time()
    else:
        start = int(time.time()-int(code_breakers[-1].time))
        
    while code_breakers[-1].turn and int(time.time() - start) <= time_limit:
        time_ = int(time.time() - start)
        Rectangle(time2_turtle, time_position[0]+30, time_position[1]-2, time_size[0]-35, time_size[1]-4, "floralwhite", "floralwhite", "")
        WriteText(time2_turtle, time_position[0]+35, time_position[1]-17, "black", str(time_//60) + ":" + str(time_%60), font_normal)
        time.sleep(1)

    Rectangle(time2_turtle, time_position[0]+30, time_position[1]-2, time_size[0]-35, time_size[1]-4, "floralwhite", "floralwhite", "")
    if int(time.time() - start) >= time_limit : #Time Out
        EndProgram(3)

    return

#Show History-------------------------------------------------------------
def ShowHistory():
    players = []
    flag = False
    temp_str = ""

    if not os.path.isfile("Players.csv"):
        turtle.TK.messagebox.showinfo(title="History", message="No History!")
        return
        
    with open("Players.csv") as file:
        reader = csv.DictReader(file)
        for row in reader:
            players.append({"name": row["name"], "date": row["date"], "score": row["score"], "time": row["time"], "result": row["result"]})

    if(len(players) > 30):
        flag = True
        players = players[-30:]

    if flag:
        temp_str = "Last 30 Players:\n\n"
    for player in sorted(players, key = lambda player: player["name"]):
        temp_str += player['name'] + " (" + player['result'] + "): score: " + player['score'] + ", time: " + str(int(player["time"])//60)+":"+str(int(player["time"])%60)+"\n"
    turtle.TK.messagebox.showinfo(title="History", message=temp_str)
    return

#Save Current Game-------------------------------------------------------------
def SaveCurrentGame():
    with open("SavedGame.txt", "w") as file:
        file.write(f"{code_breakers[-1].starting_time}\n")
        file.write(f"{code_breakers[-1].turn}\n")
        file.write(f"{code_breakers[-1].name}\n")
        file.write(f"{code_breakers[-1].score}\n")
        
        code_breakers[-1].CalculateTime()
        file.write(f"{code_breakers[-1].time}\n")
        
        file.write(f"{code_breakers[-1].hint}\n")
        file.write(f"{code_breakers[-1].game_result}\n")
        file.write(f"{code_breakers[-1].code_maker_peg}\n")

        if point_counter != 0:
            del code_breakers[-1].code_breaker_peg[-1]
        file.write(f"{code_breakers[-1].code_breaker_peg}\n")
        
        file.write(f"{code_breakers[-1].key_peg}\n")
        file.write(f"{code_breakers[-1].step_counter}\n")
        file.write(f"{code_breakers[-1].colors_omitted}\n")
        code_breakers[-1].turn = False
    return

#End Program-------------------------------------------------------------
def EndProgram(parameter, new_game=0):
    #parameter: 1:End by user 2:Win 3:Time Out 4:Exit by close button
    global code_breakers
    
    if code_breakers != [] and not(parameter == 4 and not code_breakers[-1].turn):
        CodeMakerPeg(3)
        code_breakers[-1].turn = False
        code_breakers[-1].CalculateTime()
        if parameter == 1 or parameter == 3 or parameter == 4:
            code_breakers[-1].game_result = "lose"
        elif parameter == 2:
            code_breakers[-1].game_result = "win"
        code_breakers[-1].CalculateScore()
        UpdateCodeBreakersBox()
        
        #Save player in Players.csv
        if code_breakers != []:
            if not os.path.isfile("Players.csv"):                
                with open("Players.csv", "a", newline='') as file:
                    writer = csv.DictWriter(file, fieldnames = ["name", "date", "score", "time", "result"])
                    writer.writerow({"name": "name", "date": "date", "score": "score", "time": "time", "result": "result"})
            with open("Players.csv", "a", newline='') as file:
                writer = csv.DictWriter(file, fieldnames = ["name", "date", "score", "time", "result"])
                writer.writerow({"name": code_breakers[-1].name, "date": str(date.today()), "score": code_breakers[-1].score, "time": code_breakers[-1].time, "result": code_breakers[-1].game_result})
    
    if(parameter == 1): #End by user
        turtle.TK.messagebox.showinfo(title="End of the game", message="End of the game!\n"+str(code_breakers[-1]))
        if new_game == 0 and len(code_breakers) < code_breaker_count:
            turtle.TK.messagebox.showinfo(title="", message="To start a new game, press \"New Game\" button!")
        
    elif(parameter == 2):   #Win
        turtle.TK.messagebox.showinfo(title="End of the game", message="You win the game!\n"+str(code_breakers[-1]))
        if len(code_breakers) < code_breaker_count:
            turtle.TK.messagebox.showinfo(title="", message="To start a new game, press \"New Game\" button!")
        
    elif(parameter == 3):   #Time Out
        turtle.TK.messagebox.showinfo(title="End of the game", message="Time out! End of the game!\n"+str(code_breakers[-1]))
        if len(code_breakers) < code_breaker_count:
            turtle.TK.messagebox.showinfo(title="", message="To start a new game, press \"New Game\" button!")
    
    elif(parameter == 4):   #Exit by close button
        if code_breakers != []:
            turtle.TK.messagebox.showinfo(title="", message="Thanks for playing!")
        
    return

#Close Program-------------------------------------------------------------
def CloseProgram():
    if code_breakers!= [] and code_breakers[-1].turn:
        result = turtle.TK.messagebox.askyesnocancel('Close Program', 'Do you want to save the game in progress?',icon='warning')
        if result == True:
            SaveCurrentGame()
            turtle.TK.messagebox.showinfo(title="", message="Thanks for playing!")
            screen.bye()        
        elif result == False:
            EndProgram(4)
            screen.bye()
        elif result == None:
            return
    else:
        result = turtle.TK.messagebox.askquestion('Close Program', 'Are you sure you want to close the program?',icon='warning')
        if result == "yes":
            EndProgram(4)
            screen.bye()
        else:
            return

#Main Program-------------------------------------------------------------
def main():
    global code_breakers

    screen.tracer(0)
    screen.bgcolor("white")
    screen.title("Mastermind")
    screen.onclick(CheckClick, 1)
    screen.onclick(OmitColor, 3)
    screen.setup(width=500, height=800, startx=None, starty=0)

    root.protocol("WM_DELETE_WINDOW", CloseProgram)
    
    MakeHeader()
    DecodingBoard()

    if not os.path.isfile("SavedGame.txt") or os.path.getsize('SavedGame.txt') == 0:
        NewCodeBreaker(1)
    else:
        result = turtle.TK.messagebox.askquestion('Saved Game Found', 'Do you want to continue your saved game?')
        if result == "yes":
            NewCodeBreaker(2)
        else:
            file = open("SavedGame.txt",'w')    #Clear SavedGame.txt file
            file.close()
            NewCodeBreaker(1)

    screen.mainloop()    
    return
    
#Call Main------------------------------------------------------------- 
try: 
    if __name__ == "__main__":
        main()
except Exception as e:
    print("Error:", e)
