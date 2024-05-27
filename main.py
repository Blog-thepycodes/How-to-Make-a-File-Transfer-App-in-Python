import socket
import os
import tkinter as tk
from tkinter import filedialog, Label, Button, Entry, messagebox
 
 
class FileTransferApp:
   def __init__(self, master):
       self.master = master
       self.master.title("File Transfer App - The Pycodes")
       self.master.geometry("450x560")
       self.master.configure(bg="lightblue")
       self.master.resizable(False, False)
 
 
       self.filename = None  # Instance variable for filename
 
 
       self.create_widgets()
 
 
   def create_widgets(self):
       # Entry for target IP address
       self.ip_entry_label = Label(self.master, text="Target IP:", bg="lightblue", font="arial 12 bold")
       self.ip_entry_label.place(x=190, y=100)
 
 
       self.ip_entry = Entry(self.master, width=40, font="arial 12")
       self.ip_entry.place(x=50, y=130)
 
 
       # Button to select a file
       self.select_file_button = Button(self.master, text="Select File", command=self.select_file, font="arial 11")
       self.select_file_button.place(x=170, y=190)
 
 
       # Button to send file
       self.send_button = Button(self.master, text="Send File", command=self.send_file, font="arial 11")
       self.send_button.place(x=50, y=230)
 
 
       # Button to receive file
       self.receive_button = Button(self.master, text="Receive File", command=self.receive_file, font="arial 11")
       self.receive_button.place(x=300, y=230)
 
 
       # Display local IP address
       self.local_ip_label = Label(self.master, text=f"My Local IP is: {socket.gethostbyname(socket.gethostname())}", bg="lightblue", fg="black", font="arial 10 bold")
       self.local_ip_label.place(x=50, y=280)
 
 
   def select_file(self):
       self.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select File',
                                                  filetypes=(('All files', '*.*'),))
       if not self.filename:
           messagebox.showerror("ERROR", "No file selected")
 
 
   def send_file(self):
       target_ip = self.ip_entry.get()
       if target_ip and self.filename:
           try:
               with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s, open(self.filename, 'rb') as file:
                   s.connect((target_ip, 8080))
                   while file_data := file.read(1024):
                       s.send(file_data)
                   messagebox.showinfo("Success", "Data has been transmitted successfully")
           except Exception as e:
               messagebox.showerror("ERROR", f"Error: {e}")
       else:
           messagebox.showerror("ERROR", "Please enter a target IP and select a file")
 
 
   def receive_file(self):
       filename1 = filedialog.asksaveasfilename(initialdir=os.getcwd(), title='Save Received File in',
                                                filetypes=(('All files', '*.*'),))
       if filename1:
           try:
               with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                   s.bind(('0.0.0.0', 8080))
                   s.listen(1)
                   conn, addr = s.accept()
                   with conn, open(filename1, 'wb') as file:
                       while file_data := conn.recv(1024):
                           file.write(file_data)
                   messagebox.showinfo("Success", "File has been received successfully")
           except Exception as e:
               messagebox.showerror("ERROR", f"Error: {e}")
       else:
           messagebox.showerror("ERROR", "Please enter a valid filename")
 
 
if __name__ == "__main__":
   root = tk.Tk()
   Label(root, text="Simple File Transfer", bg="lightblue", fg="red", font="arial 20 bold").place(x=80, y=50)
   app = FileTransferApp(root)
 
 
   root.mainloop()
