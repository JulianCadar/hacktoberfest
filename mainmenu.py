import customtkinter as ctk
from PIL import Image
width  = 1000
height = 1000
playersAlive = 0

players = []
from main import Player
for i in range(4):
    name = input(f"Enter the name of player {i+1}, or enter STOP to finish entering players: ")
    if name =="STOP":
        break
    else:
        players.append(Player(name,5))



def addPlayerToFrame(name):
    global playersAlive
    playerObj = Player(name,5)
    playersAlive+=1
    playerNameLabel = ctk.CTkLabel(master = playerFrame,text = playerObj.name, fg_color="white", border_color="black",border_width=1, text_color="black",font = ("Calibri",30))
    heartImageImport = Image.open("Images/heart full.png")
    heartframe = ctk.CTkFrame(master=playerFrame)
    for _ in range(playerObj.health):
        heartImage = ctk.CTkImage(light_image=heartImageImport,dark_image=heartImageImport,size=(50,50))
        heartLabel = ctk.CTkLabel(master = heartframe,text="",image=heartImage)
        heartLabel.pack(side = "right")

    heartframe.grid(row = playersAlive-1,column=1)
    playerNameLabel.grid(row = playersAlive-1,column=0)
def decrementTime():
    global time
    if time<1:
        return
    else:
        time-=1
        timerwidget.configure(text = f"{time}s")
        window.after(1000,decrementTime)


window = ctk.CTk()
window.geometry(f"{width}x{height}")
window.resizable(False,False)
window.title("Endless Encounters")

playerFrame = ctk.CTkFrame(master =window, width = width/4 +50,height=height/4 +50,)
playerFrame.place(x=25,y=25)

for player in players:
    print(player.name)
    addPlayerToFrame(player.name)

time = 20
timerwidget = ctk.CTkLabel(master =window,width = 50,height=50, border_width=3,border_color="black",text = f"{time}s",fg_color="white",text_color="black")
timerwidget.place(x=width-60,y=10)



window.after(1000,decrementTime)
window.mainloop()