from bs4 import BeautifulSoup
import requests
web=requests.get('http://digidb.io/digimon-list/')
data=BeautifulSoup(web.content,'html.parser')

head=[]
for i in data.findAll('th'):
    head.append(i.text)
head.insert(1,'Picture')
# print(head)

num=[]
for i in data.findAll('b'):
    num.append(i.string[1:])
num=num[1:]
# print(num)

gambar=[]
for i in data.findAll('img'):
    gambar.append(i['src'])
gambar=gambar[2:-2]
# print(gambar)

name=[]
for i in data.findAll('a'):
    name.append(i.text)
name=name[11:-17]
# print(name)

isi=[]
for i in data.findAll('center'):
    isi.append(i.text)
isi=isi[:-1]
# print(isi)

counter=0
listDigi=[]
listKecil=[]

for i in isi:
    listKecil.append(i)
    counter+=1
    if counter%11==0:
        listDigi.append(listKecil)
        listKecil=[]

for i in range(len(listDigi)):
    listDigi[i].insert(0,name[i])
    listDigi[i].insert(0,gambar[i])
    listDigi[i].insert(0,num[i])
# print(listDigi)

digimon=[]
for i in listDigi:
    dictDigi=dict(zip(head,i))
    digimon.append(dictDigi)
# print(digimon)

import json
with open('digimon.json','w') as y:
    json.dump(digimon,y)

import csv
with open('digimon.csv','w',newline='') as x:
    a=csv.DictWriter(x,fieldnames=head)
    a.writeheader()
    a.writerows(digimon)

import xlsxwriter
file=xlsxwriter.Workbook('digimon.xlsx')
sheet=file.add_worksheet('digimon')
for i in head:
    sheet.write(0,head.index(i),i)
row=1
for a,b,c,d,e,f,g,h,i,j,k,l,m,n in listDigi:
    sheet.write(row,0,a)
    sheet.write(row,1,b)
    sheet.write(row,2,c)
    sheet.write(row,3,d)
    sheet.write(row,4,e)
    sheet.write(row,5,f)
    sheet.write(row,6,g)
    sheet.write(row,7,h)
    sheet.write(row,8,i)
    sheet.write(row,9,j)
    sheet.write(row,10,k)
    sheet.write(row,11,l)
    sheet.write(row,12,m)
    sheet.write(row,13,n)
    row+=1
file.close()

tupleDigi=[]
for i in listDigi:
    tupleDigi.append(tuple(i))
# print(tupleDigi)

import mysql.connector
db=mysql.connector.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='rudeboy99',
    database='digimon',
)

# print(db)
c=db.cursor()
# c.execute('create database digimon')
# tabel='create table digi(No int,Picture varchar(100),Digimon varchar(20),Stage varchar(20),Type varchar(20),Attribute varchar(20),Memory int,Equip_Slots int,HP int,SP int,Atk int,Def int,Intel int,Spd int)'
# c.execute(tabel)
sql='insert into digi (No,Picture,Digimon,Stage,Type,Attribute,Memory,Equip_Slots,HP,SP,Atk,Def,Intel,Spd) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
val=tupleDigi
c.executemany(sql,val)
db.commit()