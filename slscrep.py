# coding utf8
import itertools
import time
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread
import threading
import datetime
# import xlsxwriter

url ="http://www.motorim.org.tw/query/Query_Check_Print.aspx?Car_No="
ts =time.time()

#    /*AAA-0000 to ZZZ-9999(need add xlsx function)*/
def w2():
    for i in range(65,91):
        for j in range(65, 91):
            for k in range(65, 91):
                for num in range(1,10000):
                    html =urlopen(url+chr(i)+chr(j)+chr(k)+"-"+str(num).zfill(4)).read().decode("utf-8")
                    bsObj =BeautifulSoup(html,"html.parser")
                    CC =bsObj.find("span",{"id":"lblCc"})
                    OPD =bsObj.find("span",{"id":"lblOpDate"})
                    ISD =bsObj.find("span",{"id":"lblIssueDt"})
                    try:
                        print (chr(i)+chr(j)+chr(k)+"-"+str(num).zfill(4)+"\t"+CC.get_text()+"\t"+OPD.get_text()+"\t"+ISD.get_text())
                    except:
                        print (chr(i)+chr(j)+chr(k)+"-"+str(num).zfill(4)+"\t"+"no data")
#    /*AAA-0000 to ZZZ-9999*/


#    /*AAA-000 to ZZZ-999(need add xlsx function)*/
def w3():
    for i in range(65,91):
        for j in range(65, 91):
            for k in range(65, 91):
                for num in range(1,1000):
                    html =urlopen(url+chr(i)+chr(j)+chr(k)+"-"+str(num).zfill(3)).read().decode("utf-8")
                    bsObj =BeautifulSoup(html,"html.parser")
                    CC =bsObj.find("span",{"id":"lblCc"})
                    OPD =bsObj.find("span",{"id":"lblOpDate"})
                    ISD =bsObj.find("span",{"id":"lblIssueDt"})
                    try:
                        print (chr(i)+chr(j)+chr(k)+"-"+str(num).zfill(3)+"\t"+CC.get_text()+"\t"+OPD.get_text()+"\t"+ISD.get_text())
                    except:
                        print (chr(i)+chr(j)+chr(k)+"-"+str(num).zfill(3)+"\t"+"no data")
    
#    /*AAA-000 to ZZZ-999*/

#    /*get license number via thread number*/
def w32(threadNumber,LNStart,LNEnd,LCShift):
    for num in range(int(LNStart),int(LNEnd)):
        html =urlopen(url+LC(LCShift+threadNumber)+"-"+str(num).zfill(3)).read().decode("utf-8")
        #
#         print(url+LC(LCShift+threadNumber)+"-"+str(num).zfill(3))
#         input("Press Enter to continue...")
        #
        bsObj =BeautifulSoup(html,"html.parser")
        CC =bsObj.find("span",{"id":"lblCc"})
        OPD =bsObj.find("span",{"id":"lblOpDate"})
        ISD =bsObj.find("span",{"id":"lblIssueDt"})
        try:
            print (LC(LCShift+threadNumber)+"-"+str(num).zfill(3)+"\t"+CC.get_text()+"\t"+OPD.get_text()+"\t"+ISD.get_text())
        except:
            print (LC(LCShift+threadNumber)+"-"+str(num).zfill(3)+"\t"+"no data")
    time.sleep(1)
    print(str(threading.current_thread())+"is done.")
#    /*get license number via thread number*/

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

def LCCalc():
        exit =""
        while exit =="":
            print("LCShift Calculation")
            t_LCS =int(input("test value of LCShift: "))
            for i in range(0,UserThreadInput):
                print(LC(t_LCS+i))
            exit =input("Press enter to do another calculation, exit by type ANYTHING.")

def LCHandle(c):
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
    
def LNHandle(i):
    if i >899:
        print("Out of range, Considered as 899.")
        i =899
    if i <0:
        print("Out of range, Considered as 0.")
        i =0
    return i

def LCHelp():
    print("LCShift is for shifting LC, basically if you either enter 1 or no input, it starts scraping License from AAA,AAB,AAC...\
        (according to your thread-using number, it could be more or less then that)\n\
        if you want to calculate shift amount of LC, simply enter \"calc\" and it'll show the result.")
    print("--------Example--------")
    print("thread-using =3 ,LCShift =1")
    print("    output:AAA,AAB,AAC")
    print("thread-using =7 ,LCShift =601")
    print("    output:AXC,AXD,AXE,...,AXH,AXI")
    print("thread-using =2 ,LCShift =2705")
    print("    output:EAA,EAB\n")

def animate():          #loading animation
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')
    
#    
#
#            /*main program here*/
#
#
# threadNumber =0
# done =False
# ani =Thread(target=animate)
# ani.start()

LCShift =0
LNStart =0
LNEnd =0
while True:
    try:
        UserThreadInput =input("Enter thread-using number (enter nothing will using 4): ")
        if UserThreadInput =="" or int(UserThreadInput) <0:
            UserThreadInput =4
        break
    except ValueError:
        print("Please enter an integer.")
while True:
    LCShift =LCHandle(LCShift)
    if LCShift =="?" or LCShift =="help":
        LCHelp()
        continue
    if LCShift =="calc":
        LCCalc()
        continue
    if LCShift+int(UserThreadInput) >17576: #over ZZZ or below AAA (NOT IMPLIED YET)
        print("From: "+LC(LCShift)+" to: "+LC(LCShift+int(UserThreadInput) ))
        print("This result might not what you wanted, enter \"calc\" or \"?\" seek for help.\n") #fuck the negative
        continue
    print("LC from: "+LC(LCShift)+" to "+LC(LCShift+int(UserThreadInput))
    break
while True:
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
        input("Press Enter to continue...")
        break
    except ValueError:
        print("Please enter an integer.")
for threadNumber in range(1,int(UserThreadInput)+1):
    Thread(target=w32,args=(threadNumber,LN(LNStart),LN(LNEnd),LCShift,)).start()
print(LNEnd)


#    /*multiple thread workload*/



#    /*home selection*/
# print ("環保署機車定期檢驗資訊管理系統  scraping")
# print ("1.Dumping AAA-0000 to ZZZ-9999(needs several days)")
# print ("2.Dumping AAA-000 to ZZZ-999(needs several days)")
# print ("3.Customize license range")
# print ("4.test")
# sel =input("\nSelection : ")
# if sel == 1:
#     w2()
# elif sel ==2:
#     w3()

#    /*home selection*/



# html =urlopen(url+"AAA-0001").read().decode("utf-8")
# bsObj =BeautifulSoup(html,"html.parser")
# CC =bsObj.find("span",{"id":"lblCc"})
# OPD =bsObj.find("span",{"id":"lblOpDate"})
# ISD =bsObj.find("span",{"id":"lblIssueDt"})
# print CC.get_text()+"\t"+OPD.get_text()+"\t"+ISD.get_text()