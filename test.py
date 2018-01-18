# coding utf8
import xlsxwriter
from time import strftime

workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()
licenseData =["AAA-001","aa","147","bb","199201","19920103","20171225","AF4","cc","dd","2017/12/27  18:05:39"]
tary =["yee","woo"]
row =0
col =0
t =strftime("%Y/%m/%d  %H:%M:%S")
# try:
# for ls, bn, em, cy, od, gd, td, ts, tc, tr, tt in (licenseData):
for ls,bn in (tary):
    worksheet.write(row+2, col+1, ls)
    worksheet.write(row+3, col+1, bn)
#     worksheet.write(row+4, col+1, em)
#     worksheet.write(row+5, col+1, cy)
#     worksheet.write(row+6, col+1, od)
#     worksheet.write(row+7, col+1, gd)
#     worksheet.write(row+8, col+1, td)
#     worksheet.write(row+9, col+1, ts)
#     worksheet.write(row+10, col+1, tc)
#     worksheet.write(row+11, col+1, tr)
#     worksheet.write(row+12, col+1, tt)
# except ValueError:
#     print(licenseData.__len__())
workbook.close()
    
    


