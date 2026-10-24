import customtkinter as ctk
from PIL import Image
import AI

width  = 1000
height = 1000
playersAlive = 0

player_names = []
for i in range(4):
    name = input(f"Enter the name of player {i+1}: ")
    if name =="STOP":
        break
    else:
        player_names.append(name)

def addPlayerToFrame(name, hearts):
    global playersAlive
    playersAlive+=1
    playerNameLabel = ctk.CTkLabel(master = playerFrame,text = name, fg_color="white", border_color="black",border_width=1, text_color="black",font = ("Calibri",30))
    heartImageImport = Image.open("Images/heart full.png")
    heartframe = ctk.CTkFrame(master=playerFrame)
    for _ in range(hearts):
        heartImage = ctk.CTkImage(light_image=heartImageImport,dark_image=heartImageImport,size=(50,50))
        heartLabel = ctk.CTkLabel(master = heartframe,text="",image=heartImage)
        heartLabel.pack(side = "right")

    heartframe.grid(row = playersAlive-1,column=1)
    playerNameLabel.grid(row = playersAlive-1,column=0)
def resetTime():
    global time
    global currentTurn
    time = 20
    currentplayernum = player_names.index(currentTurn)
    currentplayernum+=1
    currentplayernum = currentplayernum%4
    currentTurn = player_names[currentplayernum]
    turnLabel.configure(text = f"It is {currentTurn}'s turn")
    turnDescriptionLabel.configure(text = f"What will {currentTurn} do?")
    timerwidget.configure(text = f"{time}s")
    decrementTime()
def decrementTime():
    global currentTurn
    global time
    if time<=0:
#        resetTime()
        pass
    else:
        time-=1
        timerwidget.configure(text = f"{time}s")
        window.after(1000,decrementTime)
        return
currentTurn = player_names[0]
def getAndPlayTurn(*args):
    global state
    global currentTurn
    global time
    global playersAlive
    global playerFrame
    turnText = turnEntry.get()

    response = AI.chat.send_message(f"player chose: {turnText}")
    state = AI.GameState.model_validate_json(response.text)
    update_textbox()

    time = 20
    currentplayernum = player_names.index(currentTurn)
    currentplayernum+=1
    currentplayernum = currentplayernum%4
    currentTurn = player_names[currentplayernum]
    #print(turnText)
    turnLabel.configure(text = f"It is {currentTurn}'s turn")
    turnDescriptionLabel.configure(text = f"What will {currentTurn} do?")
    turnEntry.delete(0,ctk.END)

    playerFrame.destroy()
    playerFrame = ctk.CTkFrame(master=outerPlayerFrame)
    playerFrame.pack()
    playersAlive=0
    for player in state.party:
        #print(player)
        addPlayerToFrame(player.name, player.hearts)
def update_textbox():
    text = state.current_turn.narrative_resolution + "\n\nPlease enter one of the following:\n\n"
    for choice in state.current_turn.choices:
        text += f"\n[{choice.id}] {choice.description}"

    responseLabel.configure(state="normal")
    responseLabel.delete(1.0, ctk.END)
    responseLabel.insert(
        1.0,
        text
    )
    responseLabel.configure(state="disabled")

initResponseFromAI = AI.gen_game(player_names)

window = ctk.CTk()
window.geometry(f"{width}x{height}")
window.resizable(False,False)
window.title("Endless Encounters")

outerPlayerFrame = ctk.CTkFrame(master =window, width = width/4 +50,height=height/4 +50,)
outerPlayerFrame.place(x=25,y=25)
playerFrame = ctk.CTkFrame(master=outerPlayerFrame)
playerFrame.pack()

for player in player_names:
    #print(player)
    addPlayerToFrame(player, 5)

time = 20
timerwidget = ctk.CTkLabel(master =window,width = 50,height=50, border_width=3,border_color="black",text = f"{time}s",fg_color="white",text_color="black")
timerwidget.place(x=width-60,y=10)

turnLabel = ctk.CTkLabel(master=window, text=f"It is {currentTurn}'s Turn", font = ("Calibri",50),text_color="black",border_color="black",border_width=5, fg_color="white")
turnLabel.place(x=width/2 +100, y=25)

turnDescriptionLabel = ctk.CTkLabel(master=window, text = f"What will {currentTurn} do?")
turnDescriptionLabel.place(x=width/2 -100, y=100)
turnEntry = ctk.CTkEntry(master = window, width=200, height=50)
turnEntry.bind("<Return>",getAndPlayTurn)
turnEntry.place(x=width/2 +100, y= 100)

state = AI.GameState.model_validate_json(initResponseFromAI.text)

responseLabel = ctk.CTkTextbox(master = window, width=500, height=500)
responseLabel.place(x = width/2 -300, y = 500)

update_textbox()

window.after(1000,decrementTime)
window.mainloop()