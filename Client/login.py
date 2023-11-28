import tkinter as tk
import socket
import subprocess
from tkinter import messagebox

LoginWindow = tk.Tk()
LoginWindow.title("Login")
LoginWindow.geometry("400x150")

# ServerIP = "127.0.0.2"
# ServerPort = 8000
BUFFER_SIZE = 4096

LoginSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
  LoginWindow.protocol("WM_DELETE_WINDOW", CloseWindow)
  with open("IsIP.txt", "r") as file:
    ServerInfo = file.read().strip()
  if ServerInfo == "OK":
    file = open("ServerInfor.txt", "r")
    Info = file.read().strip().split(" ")
    global ServerIP
    global ServerPort
    ServerIP = Info[0]
    ServerPort = int(Info[1])
  LoginWindow.mainloop()

def Login():
  #Login
  LoginSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    LoginSocket.connect((ServerIP, ServerPort))
  except:
    messagebox.showinfo("Alert", "Can't connect to server")

  #Send command
  command = "Login"
  LoginSocket.send(command.encode())
  LoginSocket.recv(BUFFER_SIZE).decode()

  #Send login info
  user = username.get()
  passw = password.get()
  LoginInfo = user + " " + passw
  LoginSocket.send(str(LoginInfo).encode())
  permit = LoginSocket.recv(BUFFER_SIZE).decode()
  # print(permit)
  if (permit == "Admit"):
    with open('login.txt', 'w') as file:
      file.write("Success")
    LoginWindow.destroy()
    # subprocess.run(['python', 'client.py'])
  elif (permit == "Deny"):
    messagebox.showinfo("Alert", "Invalid username or password")
  LoginSocket.close()

def SignUp():
  LoginWindow.destroy()
  subprocess.run(['python', 'SignUp.py'])

def CloseWindow():
  with open('login.txt', 'w') as file:
    file.write("Deny")
  LoginWindow.destroy()


#Input
UsernameText = tk.Label(LoginWindow, text = "Username: ", font = ("Arial", 10))
username = tk.Entry(LoginWindow, width = 35, font = ("Arial", 10))
PasswordText = tk.Label(LoginWindow, text = "Password: ", font = ("Arial", 10))
password = tk.Entry(LoginWindow, width = 35, font = ("Arial", 10))

#Button
LoginButton = tk.Button(LoginWindow, text = "Login", width = 10, command = Login)
SignUpButton = tk.Button(LoginWindow, text = "Sign Up", width = 10, command = SignUp)

#Place
UsernameText.place(x = 20, y = 20)
username.place(x = 120, y = 20)
PasswordText.place(x = 20, y = 50)
password.place(x = 120, y = 50)
LoginButton.place(x = 120, y = 100)
SignUpButton.place(x = 250, y = 100)



main()

