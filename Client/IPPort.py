import tkinter as tk
from tkinter import messagebox
import subprocess

window  = tk.Tk()
window.geometry("300x100")
IP = ""
Port = ""

def Submit():
  IP = IPInput.get()
  Port = PortInput.get()

  if IP == "" or Port == "":
    messagebox.showinfo("Alert", "Invalid IP or Port")
  else:
    file = open("ServerInfor.txt", "w")
    file.write(f"{IP} {Port}")
    file.close()

    IPFile = open("IsIP.txt", "w")
    IPFile.write("OK")
    IPFile.close()

    messagebox.showinfo(f"Confirm", f"Server IP: {IP}\nPort: {Port}")

    window.destroy()
    subprocess.run(['python', 'login.py'])


def CLoseWindow():
  with open("IsIP.txt", "w") as file:
    file.write("NO")
  window.destroy()


IPInput = tk.Entry(window, width = 20, font = ("Arial", 10))
PortInput = tk.Entry(window, width = 20, font = ("Arial", 10))
SubmitButton = tk.Button(window, text = "OK", width = 10, command = Submit)
IPText = tk.Label(window, text = "Server IP", font = ("Arial", 10))
PortText = tk.Label(window, text = "Port", font = ("Arial", 10))

IPInput.place(x = 100, y = 10)
PortInput.place(x = 100, y = 40)
SubmitButton.place(x = 120, y = 70)
IPText.place(x = 20, y = 10)
PortText.place(x = 20, y = 40)

def main():
  window.protocol("WM_DELETE_WINDOW", CLoseWindow)
  window.mainloop()

main()