# coding utf8
import itertools
import hashlib
import getpass
import os
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
import threading
import time
from time import strftime

url ="http://www.motorim.org.tw/query/Query_Check_Print.aspx?Car_No="
exitFlag =0
isBusy =0
lock = threading.Lock()

def getLicence(searchMode,threadNumber,OutputType,LNStart,LNEnd,LCShift):        #get licenses
    if searchMode == "1":
        for num in range(int(LNStart),int(LNEnd)+1):
            html =urlopen(url+LC(LCShift+threadNumber)+"-"+str(num).zfill(3)).read().decode("utf-8")
            bsObj =BeautifulSoup(html,"html.parser")
            BN =bsObj.find("span",{"id":"lblBrandName"})
            CC =bsObj.find("span",{"id":"lblCc"})
            CY =bsObj.find("span",{"id":"lblCycle"})  
            OPD =bsObj.find("span",{"id":"lblOpDate"})
            ISD =bsObj.find("span",{"id":"lblIssueDt"})
            t =strftime("%Y/%m/%d  %H:%M:%S")
            try:
                ldd =LC(LCShift+threadNumber)+"-"+str(num).zfill(3)
                brand =BN.get_text()
                emitt =CC.get_text()
                cycle =CY.get_text()
                oDate =OPD.get_text()
                iDate =ISD.get_text()
                print (ldd+"\t"+brand+"\t"+emitt+"\t"+cycle+"\t"+oDate+"\t"+iDate+"\t"+"\t"+t)
                
            except AttributeError:
                print (LC(LCShift+threadNumber)+"-"+str(num).zfill(3)+"\t"+"no data")
    
    elif searchMode =="2":
        w, h = 3, 8
        sector =[[0 for x in range(w)] for y in range(h)]
        sector[0][0],sector[0][1],sector[0][2] = "001", "002" ,"003"
        sector[1][0],sector[1][1],sector[1][2] = "999", "998" ,"997"
        sector[2][0]                           = "500"
        sector[3][0],sector[3][1],sector[3][2] = "501", "502" ,"503"
        sector[4][0],sector[4][1],sector[4][2] = "499", "498" ,"497"
        sector[5][0],sector[5][1],sector[5][2] = "399", "398" ,"397"
        sector[6][0],sector[6][1],sector[6][2] = "440", "441" ,"442"
        sector[7][0]                           = "444"
        rowData =[[[0 for x in range(w)] for y in range(h) ] for z in range(0, int(UserThreadInput))]
    
        for i in range(8):
            for j in range(3):
                if not ((i,j)==(2,1)or(i,j)==(2,2)or(i,j)==(7,1)or(i,j)==(7,2)):
                    html =urlopen(url+LC(LCShift+threadNumber-1)+"-"+sector[i][j]).read().decode("utf-8")
                    bsObj =BeautifulSoup(html,"html.parser")
                    ISD =bsObj.find("span",{"id":"lblIssueDt"})
                    try:
                        iDate =ISD.get_text()
                        rowData[threadNumber-1][i][j] = iDate[-6:]
                    except AttributeError:
                        rowData[threadNumber-1][i][j] = "-"
                else:
                    continue
                
        lock.acquire()                  #File writing
        CommandLineMode(OutputType,searchMode,threadNumber,rowData)
        txtMode(OutputType,searchMode,threadNumber,rowData)
        lock.release() 

    elif searchMode =="3":
#         while True:
#         ma()
        sv =startValue()
#         current_LN =0
        VDK =0
        w, h = 2, 4
        rowData =[[[0 for x in range(w)] for y in range(h) ] for z in range(0, int(UserThreadInput))]
        for i in range(4):
            for j in range(2):
                html =urlopen(url+LC(LCShift+threadNumber-1)+"-"+sv.ClassDetr(VDK,sv)).read().decode("utf-8")              
                bsObj =BeautifulSoup(html,"html.parser")
                ISD =bsObj.find("span",{"id":"lblIssueDt"})
                try:
                    iDate =ISD.get_text()
                    rowData[threadNumber-1][i][j] =sv.ClassDetr(VDK,sv)+"("+iDate[-6:]+")"
#                     rowData[threadNumber-1][i][j] = ClassDetr(VDK,sv,enable)+"{}".format("("+iDate[-6:]+")")
                    VDK +=1
                except AttributeError:
                    continue
            
        lock.acquire()                  #File writing
        CommandLineMode(OutputType,searchMode,threadNumber,rowData)
        txtMode(OutputType,searchMode,threadNumber,rowData)
        lock.release() 
        return

# class myClass:
#     var =0
#     
#     @staticmethod
#     def sub(c):
#         c +=1 
#         return c
# def ma():
#     cls =myClass
#     print(cls.sub(cls.var))


class startValue:
    Istart =0
    IIstart =501
    IIIstart =500
    IVstart =1000
    value =0
    
    @staticmethod
    def ClassDetr(ValidDataChk,vcls):
        if ValidDataChk <2:
            if ValidDataChk ==0:
                vcls.value = vcls.Istart
        vcls.value+=1
        return str(vcls.value).zfill(3)

def sec1(threadNumber):
    arr =[0 for z in range(int(UserThreadInput))]
    arr[0]
def sec2(c):
    arr =[501 for z in range(int(UserThreadInput))]
def sec3(c):
    arr =[500 for z in range(int(UserThreadInput))]
def sec4(c):
    arr =[1000 for z in range(int(UserThreadInput))]


# @test1("value":0) 
def ClassDetr1(ValidDataChk):    
    Istart =0
    IIstart =501
    IIIstart =500
    IVstart =1000
    
    if ValidDataChk <2:
        if ValidDataChk ==0:
            value = Istart
        value+=1
        return str(value).zfill(3)
        
    elif (ValidDataChk >=2) and (ValidDataChk <4):
        if ValidDataChk ==2:
            value = IIstart
        value-=1
        return str(value)
    
    elif (ValidDataChk >=4) and (ValidDataChk <6):
        if ValidDataChk ==4:
            value =IIIstart
        value+=1
        return str(value)
    
    else: 
        if ValidDataChk ==6:
            value =IVstart
        value-=1
        return str(value)
        
def CommandLineMode(OutputType,searchMode,threadNumber,rowData):
    while OutputType=="1":
        if searchMode =="2":
            print(LC(LCShift+threadNumber-1)+"\t", end='')
            for a in rowData[threadNumber-1]:
                for b in a:
                    if b !=0:   
                        print(b, end="\t")
            print("\n", end='')
        elif searchMode =="3":
            print(LC(LCShift+threadNumber-1)+"\t", end='')
            for a in rowData[threadNumber-1]:
                for b in a:
                    if b !=0:   
                        print(b, end=" ")
            print("\n", end='')
        break
        
def txtMode(OutputType,searchMode,threadNumber,rowData):
    g4t ="\t\t\t\t"
    while OutputType=="2":
        if searchMode =="2":
            f =open(filename,'a')
            f.write(LC(LCShift+threadNumber-1)+"\t")
            for a in rowData[threadNumber-1]:
                for b in a:
                    if b !=0:   
                        f.write(b+'\t')
            f.write('\n')
            f.close()
        elif searchMode =="3":
            f =open(filename,'a')
            for a in rowData[threadNumber-1]:
                for b in a:
                    if b !=0:   
                        f.write(b+g4t)
            print("\n", end='')
            f.close()
        break

LCn =0
def LC(LCn):            #LC =License Characters
    firstC = chr(65 + (int)( (LCn - 1) / 676 ))
    secondC = chr(65 + ((int)( (LCn - 1) / 26 )% 26))
    thirdC = chr(65 + ((LCn - 1) % 26 ))
    return(firstC +secondC +thirdC)
    
LNn =0                  #LN =License Numbers
def LN(LNn):
    firstN = (int)(LNn / 90)
    secondN = (int)((LNn % 90) / 9)
    thirdN = (int)((int)(LNn % 9) + (int)((LNn % 9) + 6) / 10)
    return(str(firstN) +str(secondN) +str(thirdN))

def LCCalc():           #calculate LCShift
        exitf =""
        while exitf =="":
            print("LCShift Calculation")
            t_LCS =int(input("test value of LCShift: "))
            for i in range(0,int(UserThreadInput)):
                print(LC(t_LCS+i))
            exitf =input("Press enter to do another calculation, exit by type ANYTHING.\n")

def LCHandle(c):        #check LCShift's validation
    while True:
        c =input("LCShift? (enter \"?\" for more information): ")
        c =str(c).lower()
        if c =="?" or c =="calc" or c =="help":
            return c
        else:
            try:
                c =int(c)
                return c
            except ValueError:
                print("You just entered something weird, please check again or type \"?\" seek for help.")
    
def LNHandle(i):        #check LN's validation
    if i >899:
        print("Out of range, Considered as 899.")
        i =899
    if i <=0:
        print("Out of range, Considered as 1.")
        i =1
    return i

def LCHelp():           #LCShift help
    print("LCShift is for shifting LC, basically if you either enter 1 or no input, it starts scraping License from AAA,AAB,AAC...\
        (according to your thread-using number, it could be more or less then that)\n\
        if you want to calculate shift amount of LC, simply enter \"calc\" and it'll show the result.")
    print("--------Example--------\n\
        thread-using =3 ,LCShift =1\n\
                \t output:AAA,AAB,AAC\n\
        thread-using =7 ,LCShift =601\n\
                \t output:AXC,AXD,AXE,...,AXH,AXI\n\
        thread-using =2 ,LCShift =2705\n\
                \t output:EAA,EAB\n")

def animate():          #loading animation
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

def start():            #Security issue
    if anotherTask =="n":
        k = hashlib.sha256()
        f =open("key.kh","r")
        th =getpass.getpass()
        thb =th.encode()
        k.update(thb)
        h =f.read()
        res = (k.hexdigest() == h)
        f.close()
        return th,res
    return

"""

main program start from here

"""

LCShift =0
LNStart =0
LNEnd =0
anotherTask ="n"

if anotherTask =="n":
    while start() == ("owo!",True):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\
Select Search Mode: (Enter nothing will use default 3)\n\
        1. Start and End with certain License Number (eg. AAA-001 - AZK-231)\n\
        2. Search by order (8 sectors, old)\n\
        3. Search by order (4 classes, new)\n")
        searchMode =input("Choice: ")
        
        if searchMode == "1":
            while True:
                try:
                    UserThreadInput =input("Enter thread-using number (enter nothing will using 0): ")
                    if UserThreadInput =="" or int(UserThreadInput) <0:
                        UserThreadInput =0
                    break
                except ValueError:
                    print("Please enter an integer.")
            
            while True:     #Setting LCShift
                LCShift =LCHandle(LCShift)
                if LCShift =="?" or LCShift =="help":
                    LCHelp()
                    continue
                if LCShift =="calc":
                    LCCalc()
                    continue
                if LCShift+int(UserThreadInput) >17576 or LCShift <=0: #over ZZZ or below AAA
                    print("From: "+LC(LCShift)+" to: "+LC(LCShift+int(UserThreadInput) ))
                    print("This result might not what you wanted (or you just entered a non-positive number),\n\
            enter \"calc\" or \"?\" seek for help.\n") 
                    continue
                print("LC from: "+LC(LCShift)+" to "+LC(LCShift+int(UserThreadInput)))
                input("Press Enter to continue...\n")
                break
        
            while True:     #Setting LNStart & LNEnd
                try:
                    LNStart =(int)(input("LNStart? "))
                    LNStart =LNHandle(LNStart)
                    LNEnd =(int)(input("LNEnd? "))
                    LNEnd =LNHandle(LNEnd)
                    if LNStart >LNEnd:
                        print("Looks like you have low score on math: start at "+str(LNStart)+" end at "+str(LNEnd))
                        print("Please re-enter")
                        continue
                    print("LN From:　"+LN(LNStart)+" to: "+LN(LNEnd))
                    input("Press Enter to continue...\n")
                    break
                except ValueError:
                    print("Please enter an integer.")
            
            while True:     #Setting Output result type
                OutputType =input("Output type: 1.Command Line output  2. txt file output (Default =1): ")
                if OutputType !="1" and OutputType !="2" and OutputType != "":
                    print("Wrong input.")
                elif OutputType =="":
                    OutputType ="2"
                else:
                    break
                              
            for threadNumber in range(-1,int(UserThreadInput)):     #Creating threads
                Thread(target=getLicence,args=(searchMode,threadNumber+1,LN(LNStart),LN(LNEnd),LCShift,)).start()
                    
        elif (searchMode == "2") or (searchMode =='3') or (searchMode == ''):
            while True:
                try:
                    UserThreadInput =input("Enter thread-using number (enter nothing will using 1): ")
                    if UserThreadInput =="" or int(UserThreadInput) <0:
                        UserThreadInput =1
                    break
                except ValueError:
                    print("Please enter an integer.")
                
            while True:     #Setting LCShift
                LCShift =LCHandle(LCShift)
                if LCShift =="?" or LCShift =="help":
                    LCHelp()
                    continue
                if LCShift =="calc":
                    LCCalc()
                    continue
                if LCShift+int(UserThreadInput) >17576 or LCShift <=0: #over ZZZ or below AAA
                    print("From: "+LC(LCShift)+" to: "+LC(LCShift+int(UserThreadInput) ))
                    print("This result might not what you wanted (or you just entered a non-positive number),\n\
            enter \"calc\" or \"?\" seek for help.\n") 
                    continue
                print("LC from: "+LC(LCShift)+" to "+LC(LCShift+int(UserThreadInput)-1))
                input("Press Enter to continue...\n")
                break
            
            while True:     #Setting Output result type
                OutputType =input("Output type: 1.Command Line output  2. txt file output (Default =2): ")
                if OutputType !="1" and OutputType !="2" and OutputType != "":
                    print("Wrong input.")
                elif OutputType =="":
                    OutputType ="2"
                else:
                    break
            
            if OutputType =="2":    #filename handling
                filename =input("File name (Default \"LicenseOutput\"): ")
                if filename =="":
                    filename ="LicenseOutput"
                filename =filename+".txt"
            
            if searchMode =="2":    #initialize output format
                if OutputType =="1":
                    print("Series\t001\t002\t003\t999\t998\t997\t500\t501\t502\t503\t499\t498\t497\t399\t398\t397\t440\t441\t442\t444")
                else:
                    if os.path.exists(filename):
                        input("File already exists. Press any key to confirm deleting")
                        os.remove(filename)
                    open(filename,'a').write("series\t001\t002\t003\t999\t998\t997\t500\t501\t502\t503\t499\t498\t497\t399\t398\t397\t440\t441\t442\t444\n")
            else:
                g4t ="\t\t\t\t"
                if OutputType =="1":    
                    print("Series\tClass I"+g4t+"Class II"+g4t+"Class III"+g4t+"Class IV")
                else:
                    if os.path.exists(filename):
                        input(filename+" already exists. Press any key to confirm deleting")
                        os.remove('filename.txt')
                    open(filename,'a').write("Series\tClass I"+g4t+"Class II"+g4t+"Class III"+g4t+"Class IV")
            
            threads =[]     #Creating threads
            for threadNumber in range(0,int(UserThreadInput)):     
                    thrd =Thread(target=getLicence,args=(searchMode,threadNumber+1,OutputType,LN(LNStart),LN(LNEnd),LCShift,))
                    threads.append(thrd)
            
            for thread in threads:  #Start threads
                thread.start()
            
            for thread in threads:  #Wait for threads end
                thread.join()
            
            if OutputType =="1":
                anotherTask =input("\nDone, start another task \"n\", terminate program \"x\" or any key: ").lower()
            else:
                size =os.stat(filename).st_size
                path =os.getcwd()
                print("\nDone\noutput file size: "+str(size)+" Bytes\n\
                Path: "+path+"\n\
                Filename: "+filename)
                anotherTask =input("Start another task \"n\", terminate program \"x\" or any key: ").lower()
        else:
            print("Please enter correct Search Mode Number.\n")
    else:
        if anotherTask =="n":
            input("Wrong password, fail to launch.")   
