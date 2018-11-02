import logging
from server import getServer
from client import getClient
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
logging.getLogger().setLevel(10)

backgroundColor = "#151515"
textColor = "#e6e6e6"

IP = "127.0.0.1"
PORT = 25565

client = None
server = None


def startServer():
    global server
    if server is not None:
        stopServer()
    logging.debug('Starting server')
    server = getServer(PORT)
    server.startServer()
    startClient()


def startClient():
    global client
    if client is not None:
        stopClient()
    logging.debug('Starting client')
    root.openClient(IP, PORT)
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
                          background="#2d3034", width=50, padding=5)
    load = Image.open('./assets/logo.png').resize((26, 26))
    render = ImageTk.PhotoImage(load)
    img = ttk.Label(frame, image=render, style="Logo.TLabel")
    img.image = render
    img.place(x=0, y=0)
    img.pack(side="left")
    ttk.Style().configure("Title.TLabel", foreground=textColor,
                          background="#222", font=('Rajdhani', 15), padding=5)
    ttk.Label(frame, text="cs3201 Text Messenger App",
              style="Title.TLabel").pack(side="left", fill="x", expand=1)

    frame.place(x=0, y=0, relwidth=1)


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("cs3201 Text Messenger")
        self.geometry("350x500")
        self.resizable(0, 0)
        self.configure(background=backgroundColor)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.screen = None
        self.goToPage(MainPage)

    def on_closing(self):
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
        self.screen.pack(fill="both", expand=1)


class MainPage(ttk.Frame):
    def __init__(self, master):
        frameStyle = ttk.Style()
        frameStyle.theme_use('default')
        frameStyle.configure("mainPage.TFrame", background=backgroundColor)
        ttk.Frame.__init__(self, style="mainPage.TFrame")
        global server, client
        if client is not None:
            stopClient()
        if server is not None:
            stopServer()

        ttk.Style().configure("mainPage.TButton", background="#222222", borderwidth=0, highlightbackground="#222222",highlightcolor="#222222",
                              foreground=textColor, padding=(20, 5, 20, 5), font=('Rajdhani', 12))
        ttk.Button(self, style="mainPage.TButton", text="Host a new room",
                   command=lambda: master.goToPage(CreateServer)).pack(expand=1)
        ttk.Button(self, style="mainPage.TButton", text="Connect to an existing room",
                   command=lambda: master.goToPage(ConnectServer)).pack(expand=1)


class CreateServer(ttk.Frame):
    def __init__(self, master):
        ttk.Style().configure("mainFrame.TFrame",
                              foreground="black", background=backgroundColor)
        ttk.Frame.__init__(self, style="mainFrame.TFrame")
        ttk.Label(self, text="Create a new server").pack(
            side="top", fill="x", pady=10)
        ttk.Entry(self, textvariable=PORT).pack()
        ttk.Button(self, text="Create",
                   command=startServer).pack()
        ttk.Button(self, text="Return to start page",
                   command=lambda: master.backToMain()).pack()


class ConnectServer(ttk.Frame):
    def __init__(self, master):
        ttk.Style().configure("mainFrame.TFrame",
                              foreground="black", background=backgroundColor)
        ttk.Frame.__init__(self, style="mainFrame.TFrame")
        ttk.Label(self, text="Create a new server").pack(
            side="top", fill="x", pady=10)
        ttk.Entry(self, textvariable=IP).pack()
        ttk.Entry(self, textvariable=PORT).pack()
        ttk.Button(self, text="Connect",
                   command=lambda: startClient()).pack()
        ttk.Button(self, text="Return to start page",
                   command=lambda: master.backToMain()).pack()


if __name__ == "__main__":
    root = App()
    root.mainloop()
