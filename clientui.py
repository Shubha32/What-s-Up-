import sys
from PyQt4 import QtCore, QtGui, uic
import socket
import numpy as np
import random

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def integer_to_binary(n,m):
    temp = np.zeros((1,m))
    j = m
    while(n!=0):
    
        t1 = n%2
        temp[0][j-1] = t1
        n = n/2
        j = j-1
    
    return temp
def exor(t1,t2,n):
    t3 = np.zeros((1,n))
    for i in range(n):
        if(t1[i]) != (t2[i]):
            t3[0][i] = 1
    return t3[0]


def usr_encode(ch,n,m,encodematrix):
    r = n-m
    a1 = integer_to_binary(ord(ch),m)
       
        
    Eh = np.zeros((1,n))
    j = 0
    for i in range(m):
        Eh[0][i] = a1[0][i]
        

    ans = np.zeros((1,r))
    ans = np.dot(a1,encodematrix)
    for i in range(r):
        if ans[0][i]%2 == 0:
            ans[0][i] = 0
        else:
            ans[0][i] = 1

    j = m
    for i in range(r):
        Eh[0][j] = ans[0][i]
        j = j+1
    st = ''
    for i in Eh[0]:
        st = st+str(int(i))
    return st
def usr_decode(a,n,m,H,new_coset_tab,N,sii):
    a1 = np.zeros((1,n))
    j = 0
    for i in a:
        a1[0][j] = int(i)
        j = j+1
    an = np.dot(a1,H)
    for i in range(r):
        if(an[0][i]%2==0):
            an[0][i] = 0
        else:
            an[0][i] = 1
    d1 = np.zeros((1,n))
    for i in range(len(sii)):
        nr = sii[i]
        if(list(nr)==list(an[0])):
            d1 = exor(a1[0],new_coset_tab[i],n)
            for j in range(len(N)):
                if(list(d1)==list(N[j])):
                    return chr(j)
                    break
 
qtCreatorFile = "clientui.ui" # Enter file here.
m = 8
n = 14#int(input('Enter the length of the encoding bit'))
r = n-m
H = np.zeros((n,r))
for i in range(m):
    for j in range(r):
        H[i][j] = ((i**j)+(j**i))%2
i = m
j = 0
while i<n:
    H[i][j] = 1
    i = i+1
    j = j+1
        
encodematrix = np.zeros((m,r))
for i in range(m):
    for j in range(r):
        encodematrix[i][j] = H[i][j]
N = []

for i in range(0,2**m):
    ans = np.zeros((1,r))
    Eh = np.zeros((1,n))
    temp = integer_to_binary(i,m)
       
    for j in range(m):
        Eh[0][j] = temp[0][j]
    ans = np.dot(temp,encodematrix)
    
    for j in range(r):
        if ans[0][j]%2 == 0:
            ans[0][j] = 0
        else:
            ans[0][j] = 1
    k = m
    for j in range(r):
         Eh[0][k] = ans[0][j]
         k = k+1

    N.append(Eh[0])

coset_tab = []
coset_tab.append(N)

new_coset_tab = []
new_coset_tab.append(N[0])
#print N
for i in range(0,2**n):
    temp = integer_to_binary(i,n)
    temp = temp[0]
    # tssd = input('')
    flag = 0
    if(len(new_coset_tab) == 2**r):
        break
    for j in range(len(coset_tab)):
        row = coset_tab[j]
        for k in range(2**m):
            if list(row[k]) == list(temp):
                    #print 'k loop'
                    flag = 1
                    break
        if(flag == 1):
            break
                    
    if(flag != 1):
        # print temp
        t1 = temp
        t2 = np.zeros((1,n))
        new_row = []
        mini = np.ones((1,n))
        mini = mini[0]
        for k in range(len(N)):
            t2 = N[k]            
            t3 = exor(t1,t2,n)
            if(list(mini).count(1)>list(t3).count(1)):
                mini = t3
            new_row.append(t3)
        #    print new_row
         #   print mini
        coset_tab.append(new_row)
        new_coset_tab.append(mini)
          #  print new_coset_tab
    #print new_coset_tab
new_coset_tab = np.array(new_coset_tab)
sii = np.zeros((2**r,r))
for i in range(len(new_coset_tab)):
    temp = np.zeros((1,n))
    temp[0] = new_coset_tab[i]
        
    sii[i] = np.dot(temp,H)
    for j in range(len(sii[i])):
        if(sii[i][j]%2==0):
            sii[i][j] = 0
        else:
            sii[i][j] = 1
 
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.connectbtn.clicked.connect(self.connect_to_server)
        
        self.sendbtn.clicked.connect(self.send_code)
        self.receivebtn.clicked.connect(self.receive_code)
    def receive_code(self):
        data = ''
        data = s.recv(5000)
        i = 0
        #data = encoded
        bit = np.zeros((1,n))
        out = ''
        i = 0
        temp = ''
       
        for ch in str(data):
            if(i != 0 and i%n == 0):
                 out = out + usr_decode(temp,n,m,H,new_coset_tab,N,sii)
                 temp = ''
            if(i == len(data)-1):
                 out = out+ usr_decode(temp,n,m,H,new_coset_tab,N,sii)
            temp = temp+ch
            i = i+1
        
        self.t3.setText(out)
    def send_code(self):
        word = self.t4.toPlainText()
        encoded = ''
        for ch in str(word):
          encoded = encoded + usr_encode(ch,n,m,encodematrix)
        #print encoded
        s.send(encoded.encode())
        return

    def connect_to_server(self):
        
        host = self.t1.toPlainText()
        port = int(self.t2.toPlainText())
        s.connect((host,port))
        print 'connected'
        
    
    

 
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
