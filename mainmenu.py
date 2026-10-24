import customtkinter as ctk
width  = 1600
height = 900
window = ctk.CTk()
window.geometry(f"{width}x{height}")
window.resizable(False,False)
window.title("Endless Encounters")
heartsFrame = ctk.CTkScrollableFrame(master = window, width = width/2, height = height/8)
heartsFrame.place(x=100,y= 200)

aiStory = ctk.CTkLabel(master = window, text = "Insert ai text here that we will replace later")
aiStory.place(x = 100,y=100)



window.mainloop()