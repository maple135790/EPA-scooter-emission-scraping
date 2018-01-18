# coding utf8
import itertools
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup
from threading import Thread, current_thread
import threading
import time
import xlsxwriter
from time import strftime



url ="http://www.motorim.org.tw/query/Query_Check_Print.aspx?Car_No="
ldss =([])
# licenset =set()
# brandt =set()
# emittt =set()
# cyclet =set()
# oDatet =set()
# iDatet =set()

expenses = (
    ['Rent', 1000,"yes"],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)


def w32(threadNumber,LNStart,LNEnd,LCShift):        #get licenses
    for num in range(int(LNStart),int(LNEnd)+1):
        html =urlopen(url+LC(LCShift+threadNumber)+"-"+str(num).zfill(3)).read().decode("utf-8")
        bsObj =BeautifulSoup(html,"html.parser")
        BN =bsObj.find("span",{"id":"lblBrandName"})
        CC =bsObj.find("span",{"id":"lblCc"})
        CY =bsObj.find("span",{"id":"lblCycle"})  
        OPD =bsObj.find("span",{"id":"lblOpDate"})
        ISD =bsObj.find("span",{"id":"lblIssueDt"})
        FinalMEMO =bsObj.find("tr",{"bgcolor":"#FFFFFF"})
        t =strftime("%Y/%m/%d  %H:%M:%S")
        
#         print(FinalMEMO.contents[2*8+1].get_text())     #final test date
#         print(FinalMEMO.contents[2*1+1].get_text())     #final test station
#         print(FinalMEMO.contents[2*2+1].get_text())     #test class
#         print(FinalMEMO.contents[2*7+1].get_text())     #test result
#         input("wait..")

        try:
#             print (LC(LCShift+threadNumber)+"-"+str(num).zfill(3)+"\t"+BN.get_text()+"\t"\
#                    +CC.get_text()+"\t"+CY.get_text()+"\t"+OPD.get_text()+"\t"+ISD.get_text()+"\t"\
#                    +t)
            ldd =LC(LCShift+threadNumber)+"-"+str(num).zfill(3)
            brand =BN.get_text()
            emitt =CC.get_text()
            cycle =CY.get_text()
            oDate =OPD.get_text()
            iDate =ISD.get_text()
            
            ldss =([ldd,brand,emitt])
            
            
        except AttributeError:
            print (LC(LCShift+threadNumber)+"-"+str(num).zfill(3)+"\t"+"no data")
#             lds.add([ldd])
#             licenset.add(LC(LCShift+threadNumber)+"-"+str(num).zfill(3))
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

def LCCalc():           #calculate LCShift
        exit =""
        while exit =="":
            print("LCShift Calculation")
            t_LCS =int(input("test value of LCShift: "))
            for i in range(0,UserThreadInput):
                print(LC(t_LCS+i))
            exit =input("Press enter to do another calculation, exit by type ANYTHING.")

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
while True:     #Setting thread-using number
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
                
for threadNumber in range(-1,int(UserThreadInput)):     #Creating threads
    Thread(target=w32,args=(threadNumber+1,LN(LNStart),LN(LNEnd),LCShift,)).start()


time.sleep(3)
while threading.current_thread() ==threading.main_thread() and threading.active_count() ==1:
#     adi =0
#     row =0
#     col =0
#     workbook = xlsxwriter.Workbook('test1.xlsx')
#     worksheet = workbook.add_worksheet()
#     for d1,d2,d3,d4,d5,d6 in (lds):
#         worksheet.write(row+2+adi, col+1, d1)
#         worksheet.write(row+2+adi, col+2, d2)
#         worksheet.write(row+2+adi, col+3, d3)
#         worksheet.write(row+2+adi, col+4, d4)
#         worksheet.write(row+2+adi, col+5, d5)
#         worksheet.write(row+2+adi, col+6, d6)
#         adi +=1
#     
#     workbook.close()
    print(ldss)
    input("wait...")
    break
