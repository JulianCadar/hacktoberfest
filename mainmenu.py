import customtkinter as ctk
width  = 1000
height = 1000
playersAlive = 0
class Player:
    def __init__(self, name, health):
        self.name = name
        self.health = health

def addPlayerToFrame(name):
    playerObj = Player(name,5)
    playersAlive+=1
    playerObjFrame = ctk.CTkFrame(master =playerFrame,width = playerFrame.winfo_width() -25, height = playerFrame.winfo_height()/4)
    playerObjFrame.place(x=25,y=playersAlive*playerObjFrame.winfo_height()/4)
    playerNameLabel = ctk.CTkLabel(master = playerObjFrame,text = playerObj.name)
    playerNameLabel.place(x = 250,y = playerObjFrame.winfo_height()/4)
window = ctk.CTk()
window.geometry(f"{width}x{height}")
window.resizable(False,False)
window.title("Endless Encounters")

playerFrame = ctk.CTkScrollableFrame(master =window, width = width/4, height=height/4)
playerFrame.place(x=25,y=25)




window.mainloop()