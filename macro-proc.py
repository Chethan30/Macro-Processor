#database table creation using sqlite
import sqlite3

#create connection between database and program
conn = sqlite3.connect('db.db')
c = conn.cursor()

#create two tables NAMTAB(Macro name table) and DEFTAB(macro definition table) if yet not created
c.execute("CREATE TABLE IF NOT EXISTS DEFTAB(DEFTABc TEXT PRIMARY KEY ,md TEXT);")
c.execute("CREATE TABLE IF NOT EXISTS NAMTAB(NAMTABc TEXT PRIMARY KEY,DEFTABc TEXT,mn TEXT);")

#if there is any data in table then delete that data
c.execute("DELETE FROM DEFTAB")
conn.commit()

c.execute("DELETE FROM NAMTAB")
conn.commit()

#sp is stack pointer who point the current value of stack
global sp

def reads(file,pos,s,mdlc,c):
    global sp
    global n
    conn = sqlite3.connect('db.db')
    c = conn.cursor()
    lis = ["null",-1] #List used as an array 
    while True:
        #if empty
        if sp == -1 :
            gh = False
            #read next line and go back to main  processing
            file.seek(pos,0)
            stri = file.readline()
            pos = file.tell()
            lis[0]=stri
            lis[1]=pos
            return lis
        else :
            #read this line from DEFTAB
            s[sp+1] = int(s[sp+1]) + 1
            c.execute('SELECT md FROM DEFTAB WHERE DEFTABc = '+str(int(stack[sp+1])))
            
            data = c.fetchall()
            #arg substitution
            asdf = ''
            asdf =asdf+ str(data[0])
            stri = asdf.split(' ')
            stri[0] = stri[0][2:]
            for i in stri :
                if i[0] == '#' :
                    fg = int(i[1:])
                    j=stri.index(i)
                    if sp==0:
                        stri[j] = s[sp+3+fg]
                    else:
                        stri[j] = s[sp+2+fg]
            lrf = len(stri)
            adcd = ''
            for i in range(lrf-1):
                 if stri[i] != '\\n':
                      adcd = adcd+ str(stri[i])+' '
                 else:
                      adcd += '\n'
            lis[0] = adcd
            if "MEND" == stri[0] or "mend" == stri[0] or "Mend" == stri[0] :
                if mdlc == 0:
                    n = sp - int(s[sp]) - 2
                    sp = s[sp]
                else :
                    return lis
            else :
                return lis

                
print("Enter macro:")
NAMTABc = -1 #Record number in NAMTAB
n=0
DEFTABc = -1 #Record number in DEFTAB
mdlc = 0
sp = -1
f = open("input.txt","w") #Opening input file

#take input from user and write it in "input.txt" file 
while True :
    #loop will be run until you type "end"
    sgr = input()
    if sgr=='end' or sgr=='END' or sgr=='End':
        f.write(sgr+" \n")
        break
    f.write(sgr+" \n")
f.close()

#open another file "output.txt" which contains the final output of macro
fo = open("output.txt",'w') #opening in write mode
f = open("input.txt",'r') #opening in read mode 

stack = [] #empty stack for level
ala = [] #empty list for arguments
pos = 0
stack.append(sp) #storing pointer in stack i.e LEVEL

while True:
    
    flag = True
    #read module
    while flag == True:
        flag = False
        l = reads(f,pos,stack,mdlc,c) #calling read function

        # if file not empty 
        if l[1] !=-1:
            pos = l[1]
        stri = str(l[0])
        macrodef = stri.split(" ")
        
        # NAMTAB table
        ng = stri.split(' ')
        c.execute("SELECT mn FROM NAMTAB ;")
        data = c.fetchall()
        for i in range(len(data)):
            ing = ''
            ing+=str(data[i])
            string =ing.split(' ')
            if string[0] == "('"+macrodef[0]:
                flag = True
                try:
                    stack[sp+n+2]= sp
                except:
                    stack.append(sp)
                sp = sp+n+2
                c.execute("SELECT DEFTABc FROM NAMTAB WHERE mn = ?",(data[i]))
                tab = c.fetchall()
                df = str(tab[0])
                ds=df.split("'")
                at = ds[1]
                try:
                    stack[sp+1]= at
                except:
                    stack.append(at)
                n = len(string)-2
                # arg substitution
                try:
                    if sp == 0:
                        for i in range(n):
                            stack[sp+3+y] = macrodef[y+1]
                    else:
                        for y in range(n):
                            stack[sp+2+y] = macrodef[y+1]
                except:
                    for y in range(n):
                          stack.append(macrodef[y+1])
                break
        

    #MACRO table
    #print(stri)
    if stri == 'MACRO \n' or stri == 'macro \n' :
        
        l = reads(f,pos,stack,mdlc,c)
        if l[1] != -1:
            pos = l[1]
        stri = l[0]
        #remove all previous elements from ALA
        del ala[:]
        NAMTABc += 1
        DEFTABc += 1
        #entry in NAMTAB and DEFTAB table
        c.execute("INSERT INTO NAMTAB VALUES(?,?,?)",(NAMTABc, DEFTABc,stri))
        conn.commit()
        c.execute('INSERT INTO DEFTAB VALUES(?,?)',(DEFTABc,stri)) 
        conn.commit()

        

        # ALA prep
        abc = stri.split(' ')
        # length of a list
        lent = len(abc)
        for i in range(1,lent):
            ala.append(abc[i])
        #length of ALA
        lent = len(ala)
        
        mdlc  += 1

        # 2 read module
        while mdlc != 0 :
            l = reads(f,pos,stack,mdlc,c)
            if l[1] != -1:
                pos = l[1]
            stri = l[0]
            #arg substitution
            s = stri.split(' ')
            for i in s:
                for j in ala:
                    if i == j and i!= ' ' and j!='\n' and i!='\n':
                        q = ala.index(j)
                        x = s.index(i)
                        s[x] = '#' + str(q)
                        
            lent = len(s)
            st=''
            for i in range(lent):
                 if s[i]==' ':
                      continue
                 st= st + s[i] + ' '
            
            DEFTABc += 1
            c.execute('INSERT INTO DEFTAB VALUES(?,?)',(DEFTABc,st))
            conn.commit()
            

            if st == 'MACRO \n ' or st == 'macro \n ' :
                mdlc +=1
            if st == 'MEND \n ' or st == 'mend \n ' :
                mdlc -= 1
                  
    #write output in file
    else :
        fo.write(stri)
        if stri == 'end \n' or stri == 'END \n' or stri == 'End \n' :
            break

fo.close()
f.close()

#display final output from "output.txt" file
f = open("output.txt",'r')
f.seek(0,0)
stri = f.read()
print(stri)
f.close()
