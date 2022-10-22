import socket
from threading import Thread
from tkinter import *
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sockstream is for tcp, INET is for ipv4
ip_address = "127.0.0.1"
port = 8000

client.connect((ip_address, port))
print("Successfully connected to the server!")

class GUI:
    def __init__(self): #just like "this" in js, constructor in js like init
        self.Window = Tk()
        self.Window.withdraw() #allow another window to come on top of it
        self.LoginWindow = Toplevel()
        self.LoginWindow.title("Login")
        self.LoginWindow.resizable(width=False, height=False)
        self.LoginWindow.configure(width=400, height=200)
        self.intro = Label(self.LoginWindow, text="Please login to continue...", justify=CENTER, font="sans-serif 14 bold")
        self.intro.place(relheight=0.15, relx=0.2, rely= 0.07)
        self.name = Label(self.LoginWindow, text="Name: ", font="sans-seirf 12")
        self.name.place(relheight=0.2, relx=0.2,rely=0.1)
        self.entryName = Entry(self.LoginWindow, text="", font="sans-serif 14")
        self.entryName.place(relheight=0.12, relwidth= 0.4, relx= 0.35, rely=0.2)
        self.entryName.focus()
        self.go = Button(self.LoginWindow, text="Log In", font="sans-serif 14 bold", command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55)

        self.Window.mainloop()
    def recieve(self):
        while(True):
            try:
                msg = client.recv(2048).decode("utf-8")
                if msg=="NICKNAME":
                    client.send(self.entryName.encode("utf-8"))
                else:
                    self.showmsg(msg)

            except:
                print("Oops! An error occured")
                client.close()
                break;
    def goAhead(self, name):
        self.LoginWindow.destroy()
        self.username = name
        recieveThread=Thread(target=self.recieve)
        recieveThread.start()
        self.layout(name)

    def layout(self, name):
        self.name = name
        self.Window.deiconify() #give focus to main window an
        self.Window.title("CHAT ROOM")
        self.Window.resizable(width=False, height=False)
        self.Window.configure(width=470, height=550, bg="cyan")
        self.labelHead = Label(self.Window, bg="cyan", fg="black", text=self.name, font="sans-serif 13 bold", pady=5)
        self.labelHead.place(relwidth=1)
        self.horizontalLine = Label(self.Window, width=450, bg="red")
        self.horizontalLine.place(relwidth=1, rely=0.07, relheight=0.012)
        self.textArea = Text(self.Window, width=20, height=2, bg="lightcyan", fg="black", font="sans-serif 14 bold", padx=5, pady=5)
        self.textArea.config(state=DISABLED)
        self.textArea.place(relheight=0.745, relwidth=1, rely=0.08)
        self.labelBottom = Label(self.Window, bg="cyan", fg="black", font="sans-serif 14 bold", height=18)
        self.labelBottom.place(relwidth=1, rely=0.825)
        self.entrymsg = Entry(self.labelBottom, bg="darkcyan", fg="black", font="sans-serif 13 bold")
        self.entrymsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entrymsg.focus()
        self.sendButton = Button(self.labelBottom, bg="cyan", fg="black", font="sans-serif 10 bold", text="SEND", command=lambda: self.sendMsg(self.entrymsg.get())) #lamba is just like arrow function
        self.sendButton.place(relwidth=0.22, relx=0.77, rely=0.008, relheight=0.06)
        self.textArea.config(cursor="arrow")
        self.scrollBar = Scrollbar(self.textArea)
        self.scrollBar.place(relheight=1, relx=0.974)
        self.scrollBar.config(command=self.textArea.yview)
    def sendMsg(self, msg):
        self.textArea.config(state=DISABLED)
        self.msg = msg
        self.entrymsg.delete(0, END)
        self.writeThread = Thread(target=self.write)
        self.writeThread.start()
    
    def showMsg(self, msg):
        self.textArea.config(state=NORMAL)
        self.textArea.insert(END, msg+"\n")
        self.textArea.config(state=DISABLED)
        self.textArea.see(END)

    def write(self):
        self.textArea.config(state=DISABLED)
        while(True):
                msg = "{}: {}".format(self.name, self.msg)
                print(msg)
                print(client)
                client.send(msg.encode("utf-8"))
                self.showMsg(msg)
                break


    

        
    #the moment we run the client file, it wil start the recieve thread along with the send thread



    
g=GUI()






