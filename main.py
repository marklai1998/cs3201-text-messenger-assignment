import logging
from server import getServer
from client import getClient
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
logging.getLogger().setLevel(10)

backgroundColor = "#FFF"
textColor = "#333"

IP = None
PORT = None

client = None
server = None


def startServer():
    global server
    if server is not None:
        stopServer()
    logging.debug('Starting server')
    server = getServer(int(PORT.get()))
    server.startServer()
    startClient()


def startClient():
    global client
    if client is not None:
        stopClient()
    logging.debug('Starting client')
    root.openClient(IP.get(), int(PORT.get()))
    client.startClient()


def stopServer():
    global server
    if server is not None:
        server.stopServer()
        server = None


def stopClient():
    global client
    if client is not None:
        client.stopClient()
        client = None


def header(self):
    frame = ttk.Frame(self)

    ttk.Style().configure("Logo.TLabel", foreground="black",
                          background="#1976d2", width=50, padding=8)
    load = Image.open('./assets/logo.png').resize((30, 30))
    render = ImageTk.PhotoImage(load)
    img = ttk.Label(frame, image=render, style="Logo.TLabel")
    img.image = render
    img.place(x=0, y=0)
    img.pack(side="left")
    ttk.Style().configure("Title.TLabel", foreground="#FFF",
                          background="#2196f3", font=('Rajdhani', 15), padding=10)
    ttk.Label(frame, text="CS3201 Text Messenger App",
              style="Title.TLabel").pack(side="left", fill="x", expand=1)

    frame.place(x=0, y=0, relwidth=1)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("cs3201 Text Messenger")
        self.geometry("350x700")
        self.resizable(0, 0)
        self.configure(background=backgroundColor)
        self.protocol("WM_DELETE_WINDOW", self.onClosing)
        self.screen = None
        self.goToPage(MainPage)
        global PORT, IP
        PORT = tk.StringVar()
        PORT.set(25565)
        IP = tk.StringVar()
        IP.set("127.0.0.1")

        frameStyle = ttk.Style()
        frameStyle.theme_use('default')
        frameStyle.configure(
            "mainFrame.TFrame", background=backgroundColor, padding=(0, 35, 0, 0))

        buttonStyle = ttk.Style()
        buttonStyle.theme_use('default')
        buttonStyle.configure("global.TButton", background="#2196f3", borderwidth=0,
                              foreground="#FFF", padding=(20, 5, 20, 5), font=('Rajdhani', 12))
        buttonStyle.map("global.TButton", background=[('focus', "#1976d2")])

        labelStyle = ttk.Style()
        labelStyle.theme_use('default')
        labelStyle.configure("global.TLabel", background=backgroundColor,
                             foreground=textColor, padding=(0, 20, 0, 20), font=('Rajdhani', 15))

        fieldLabelStyle = ttk.Style()
        fieldLabelStyle.theme_use('default')
        fieldLabelStyle.configure("field.TLabel", background="#e9e9e9",
                                  foreground=textColor, padding=(15, 5, 15, 5), font=('Rajdhani', 15))

        fieldStyle = ttk.Style()
        fieldStyle.theme_use('default')
        fieldStyle.configure("field.TEntry", borderwidth=0, fieldbackground="#f5f5f5",
                             padding=(10, 6, 10, 6))

    def onClosing(self):
        if client is not None:
            stopClient()
        if server is not None:
            stopServer()
        root.destroy()

    def goToPage(self, frameClass):
        newFrame = frameClass(self)
        self.initPage(newFrame)

    def backToMain(self):
        self.goToPage(MainPage)

    def openClient(self, IP, PORT):
        global client
        client = getClient(self, IP, PORT)
        self.initPage(client)

    def initPage(self, newFrame):
        if self.screen is not None:
            self.screen.destroy()
        self.screen = newFrame
        header(self)
        self.screen.pack(fill="both", expand=1, pady=(46, 0))


class MainPage(ttk.Frame):
    def __init__(self, master):
        ttk.Style().theme_use('default')
        ttk.Frame.__init__(self, style="mainFrame.TFrame")
        global server, client
        if client is not None:
            stopClient()
        if server is not None:
            stopServer()

        ttk.Button(self, style="global.TButton", text="Host a new room",
                   command=lambda: master.goToPage(CreateServer)).pack(expand=1)

        ttk.Button(self, style="global.TButton", text="Connect to an existing room",
                   command=lambda: master.goToPage(ConnectServer)).pack(expand=1)


class CreateServer(ttk.Frame):
    def __init__(self, master):
        ttk.Style().theme_use('default')
        ttk.Frame.__init__(self, style="mainFrame.TFrame")

        ttk.Label(self, text="Create a new server",
                  style="global.TLabel").pack()

        frame = ttk.Frame(self, style="mainFrame.TFrame",
                          padding=(0, 15, 0, 20))

        global PORT
        ttk.Label(frame, text="Port",
                  style="field.TLabel").pack(side="left")
        ttk.Entry(frame, textvariable=PORT,
                  style="field.TEntry", font=('Rajdhani', 15)).pack(side="left", fill="x", expand=1)
        frame.pack(fill="x")

        frame2 = ttk.Frame(self, style="mainFrame.TFrame",
                           padding=(0, 15, 0, 20))
        ttk.Button(frame2, text="Create", style="global.TButton",
                   command=startServer).pack()
        frame2.pack(fill="x")

        ttk.Button(self, text="Back to main page", style="global.TButton",
                   command=lambda: master.backToMain()).pack()


class ConnectServer(ttk.Frame):
    def __init__(self, master):
        ttk.Style().theme_use('default')
        ttk.Frame.__init__(self, style="mainFrame.TFrame")

        ttk.Label(self, text="Connecting to existing server",
                  style="global.TLabel").pack()

        global PORT, IP

        ipFrame = ttk.Frame(self, style="mainFrame.TFrame",
                            padding=(0, 15, 0, 20))
        ttk.Label(ipFrame, text="IP",
                  style="field.TLabel").pack(side="left")
        ttk.Entry(ipFrame,
                  style="field.TEntry", textvariable=IP, font=('Rajdhani', 15)).pack(side="left", fill="x", expand=1)
        ipFrame.pack(fill="x")

        portFrame = ttk.Frame(self, style="mainFrame.TFrame",
                              padding=(0, 15, 0, 20))
        ttk.Label(portFrame, text="PORT",
                  style="field.TLabel").pack(side="left")
        ttk.Entry(portFrame,
                  style="field.TEntry", textvariable=PORT, font=('Rajdhani', 15)).pack(side="left", fill="x", expand=1)
        portFrame.pack(fill="x")

        frame2 = ttk.Frame(self, style="mainFrame.TFrame",
                           padding=(0, 15, 0, 20))
        ttk.Button(frame2, text="Connect", style="global.TButton",
                   command=lambda: startClient()).pack()
        frame2.pack(fill="x")

        ttk.Button(self, text="Back to main page", style="global.TButton",
                   command=lambda: master.backToMain()).pack()


if __name__ == "__main__":
    root = App()
    root.mainloop()
