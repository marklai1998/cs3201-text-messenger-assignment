# CS3201 Text Messenger Assignment
## Introduction
This repository is created for `City University HK` course `CS3201 - Computer Networks` programming assignment
All credit goes to: Mark Lai

## Assignment requirement
Aim to create a TCP based text messenger app for 2 or more participant.
Both participants can both send receive messages.
Multi-threading and non blocking topology is a bonus.

## Library used
| Library   | Usage                                          |
| --------- | ---------------------------------------------- |
| logging   | Implement appropriate logging style on console |
| threading | Multi-threading and non blocking loop          |
| tkinter   | UI implementation                              |
| PIL       | Import logo image for UI representation        |
| socket    | Handle both the client and server connections  |

## File description
| File      | Usage                                                                        |
| --------- | ---------------------------------------------------------------------------- |
| main.py   | Main logic and UI implementation                                             |
| client.py | Handle the client connection and the chatroom UI                             |
| server.py | Server hosting, handle all the client connection and broadcasting of message |

## Logic flow
### Join an existing room
User will be prompted to type in the correct IP and port and a socket will be created with a try catch
Error message will prompt if server can't reach for whatever reason
After the connection made, user will be switch to the chatroom UI

### Host a new room
User will only be prompted for the port, and the IP will keep as default (127.0.0.1)
A server will be created and run in background
After creating the server, user will create a client connect to localhost with the same port
After the connection made, user will be switch to the chatroom UI

