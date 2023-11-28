import tkinter as tk
import socket
import subprocess
from tkinter import messagebox

window = tk.Tk()
window.title("Sign up")
window.geometry("400x250")

file = open("ServerInfor.txt", "r")
Info = file.read().strip().split(" ")
ServerIP = Info[0]
ServerPort = int(Info[1])
BUFFER_SIZE = 4096

SignUpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def Return():
  window.destroy()
  subprocess.run(['python', 'login.py'])

def OTP():
  check = 0
  command = "OTP"
  SignUpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  SignUpSocket.connect((ServerIP, ServerPort))
  SignUpSocket.send(command.encode())
  SignUpSocket.recv(BUFFER_SIZE).decode()
  email = EmailInput.get()
  if "@" in email and ".com" in email:
    check = 1
  else:
    messagebox.showinfo("Warning", "Invalid email")
    check = 0
  if check == 1:
    SignUpSocket.send(email.encode())
  elif check == 0:
    SignUpSocket.send("".encode())
  SignUpSocket.close()

def SignUp():
  check = 0
  secureCode = security.get()
  if secureCode == "":
    messagebox.showinfo("Alert", "Input your OTP")
  else:
    check = 1

  if check == 1:
    #SignUp
    SignUpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SignUpSocket.connect((ServerIP, ServerPort))

    #Send command
    command = "SignUp"
    SignUpSocket.send(command.encode())
    SignUpSocket.recv(BUFFER_SIZE).decode()
    user = username.get()
    passw = password.get()
    confr = confirm.get()

    SignUpSocket.send(secureCode.encode())
    Permission = SignUpSocket.recv(BUFFER_SIZE).decode()

    if (user == "" or passw == ""):
      messagebox.showinfo("Error", "Invalid username or password")
    else:
      if (confr != passw):
        messagebox.showinfo("Error", "Incorrect confirm password")
      else:
        if (Permission == "Deny"):
          messagebox.showinfo("Error", "Wrong OTP")
        elif (Permission == "Permit"):
          User = user + " " + passw
          SignUpSocket.send(str(User).encode())
          messagebox.showinfo("Congrat!!", "Welcome to our server")

    #Send
    SignUpSocket.close()

#Input
UsernameText = tk.Label(window, text = "Username: ", font = ("Arial", 10))
username = tk.Entry(window, width = 35, font = ("Arial", 10))
PasswordText = tk.Label(window, text = "Password: ", font = ("Arial", 10))
password = tk.Entry(window, width = 35, font = ("Arial", 10))
ConfirmText = tk.Label(window, text = "Confirm: ", font = ("Arial", 10))
confirm = tk.Entry(window, width = 35, font = ("Arial", 10))
SecurityText = tk.Label(window, text = "Security code: ", font = ("Arial", 10))
security = tk.Entry(window, width = 5, font = ("Arial", 10))
EmailText = tk.Label(window, text = "Email: ", font = ("Arial", 10))
EmailInput = tk.Entry(window, width = 25, font = ("Arial", 10))

#Button
SignUpButton = tk.Button(window, text = "Sign Up", width = 10, command = SignUp)
ReturnButton = tk.Button(window, text = "Return", width = 10, command = Return)
OTPButton = tk.Button(window, text = "Get OTP", width = 7, command = OTP)

#Place
UsernameText.place(x = 20, y = 20)
username.place(x = 120, y = 20)
PasswordText.place(x = 20, y = 50)
password.place(x = 120, y = 50)
ConfirmText.place(x = 20, y = 80)
confirm.place(x = 120, y = 80)

EmailText.place(x = 20, y = 110)
EmailInput.place(x = 120, y = 110)
SecurityText.place(x = 20, y = 140)
security.place(x = 120, y = 140)
ReturnButton.place(x = 80, y = 200)
SignUpButton.place(x = 200, y = 200)
OTPButton.place(x = 307, y = 110)


window.mainloop()
b = 1