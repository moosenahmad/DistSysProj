#Using Tkinter for GUI and buttons
from Tkinter import *
import tkMessageBox
import Tkinter
#GUI ENDS
#TIMER TO MEASURE LATENCY
import timeit
#TIMER END
#SOCKETS
import socket
host = '0.0.0.0'        # Symbolic name meaning all available interfaces
port = 8080     # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))

print host , port
s.listen(1)
conn = []
addr = []
clients = int(raw_input("How many clients would you like to accept? "))
#SOCKETS END

#Using Tkinter for GUI and buttons
 
window = Tk()
 
window.title("Homework")
 
window.geometry('150x300')

txt = Entry(window,width=20)
 
txt.grid(column=0, row=0)

Lb1 = Listbox(window,selectmode='multiple',exportselection=False)
Lb1.grid(row = 3, column = 0)

def added():
	if(Lb1.curselection()):
		multiselect = Lb1.curselection()
		print("Client file sent to selected users")
		for i in multiselect[::-1]:
			text = Lb1.get(i)
			length = len(addr)
			count = 0
			while(count < length):
				if(text == addr[count][0]):
					start = timeit.default_timer()
					conn[count].sendall("clientfile".encode('utf-8'))
					ready = conn[count].recv(1024).decode('utf-8')
					print("{}: {}".format(addr[count][0],ready))
					if(ready == "ready"):
						f = open('clients.txt','rb')
						l = f.read(1024)

						while(l):
							conn[count].sendall(l)
							l = f.read(1024)
						
						f.close()
						conn[count].sendall("done...transfer")

					check = conn[count].recv(1024).decode('utf-8')
					print("{}: {}".format(addr[count][0],check))
					print 'Latency ', timeit.default_timer()-start ,'\n'				
					break;
				count += 1
		
	else: tkMessageBox.showinfo('Member Error', 'No member selected')

def removed():
	if(Lb1.curselection()):
		multiselect = Lb1.curselection()
		for i in multiselect[::-1]:
			Lb1.delete(i)
	else: tkMessageBox.showinfo('Member Error', 'No member selected')

def unicast():
	if(Lb1.curselection()):
		select = Lb1.curselection()
		if len(select) < 2:
			text = Lb1.get(Lb1.curselection())
			length = len(addr)
			count = 0
			while(count < length):
				if(text == addr[count][0]):
					print("Unicast to " + str(addr[count][0]))
					start = timeit.default_timer()
					conn[count].sendall(txt.get().encode('utf-8'))
					print 'Latency ', timeit.default_timer()-start ,'\n'
				count += 1
		else: tkMessageBox.showinfo('Member Error', 'More than one member selected, please use Multicast')
    	else: tkMessageBox.showinfo('Member Error', 'No member selected')

def multicast():
	if(Lb1.curselection()):
		multiselect = Lb1.curselection()
		print("Multicast to selected users")
		start = timeit.default_timer()
		for i in multiselect[::-1]:
			text = Lb1.get(i)
			length = len(addr)
			count = 0
			while(count < length):
				if(text == addr[count][0]):
					conn[count].sendall(txt.get().encode('utf-8'))
				count += 1
		print 'Latency ', timeit.default_timer()-start ,'\n'
	else: tkMessageBox.showinfo('Member Error', 'No member selected')

def disconnect():
	if(Lb1.curselection()):
		multiselect = Lb1.curselection()
		for i in multiselect[::-1]:
			text = Lb1.get(i)
			length = len(addr)
			count = 0
			while(count < length):
				if(text == addr[count][0]):
					conn[count].sendall("cmdclose".encode('utf-8'))
					print('Closed ' + str(addr[count][0]))
					addr.pop(count)
					conn[count].close()
					Lb1.delete(i)
				count += 1
	else: tkMessageBox.showinfo('Member Error', 'No member selected')


btn = Button(window, text="Send Member List", command=added)
 
btn.grid(column=0, row=1)

btn = Button(window, text="Remove Member", command=removed)

btn.grid(column=0, row=4)

btn = Button(window, text="Unicast", command=unicast)
 
btn.grid(column=0, row=5)

btn = Button(window, text="Multicast", command=multicast)
 
btn.grid(column=0, row=6)

btn = Button(window, text="Disconnect", command=disconnect)

btn.grid(column=0, row=7)

def connected():
	count = 0
	myfile = open('clients.txt', 'w')
	while count < clients:
		s.listen(1)
		conntemp, addrtemp = s.accept()
		conn.append(conntemp)
		addr.append(addrtemp)
		Lb1.insert(END, addr[count][0])
		myfile.write(addr[count][0]+'\n')
		Lb1.update_idletasks()
		conn[count].sendall("Connection accepted".encode('utf-8'))
		count +=1
	myfile.close()

window.after(2000, connected)
window.mainloop()

