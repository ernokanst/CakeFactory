from db import DB
from models import Models
import csv, os
import random


db = DB('db.db')
model = Models(db.get_connection())
model.init_tables()
with open('static/input/Пользователи.csv', newline='') as csvfile:
    users = csv.reader(csvfile, delimiter=',')
    for row in users:
        if row[4] == 'Role': continue
        image = row[2]
        if (image + '.jpg') in os.listdir('static/img'):
            image = image + '.jpg'
        elif (image + '.png') in os.listdir('static/img'):
            image = image + '.png'
        elif (image + '.gif') in os.listdir('static/img'):
            image = image + '.gif'
        else:
            image = 'default.png'
        model.insert_user(row[2], row[3], row[4], row[0]+row[1], image)
with open('static/input/Украшения для торта.csv', newline='') as csvfile:
    users = csv.reader(csvfile, delimiter=';')
    for row in users:
        if row[1] == 'Наименование': continue
        image = ''
        if (row[0] + '.jpg') in os.listdir('static/img'):
            image = row[0] + '.jpg'
        price = row[5]
        if price != '':
            price = price.replace("'", '')
            price = price.replace(",", '.')
            price = float(price)
        model.insert_decoration(int(row[0]), row[1], row[2], int(row[3]), '', image, row[4], price, row[6])
skus = ['']
with open('static/input/Ингредиенты.csv', newline='') as csvfile:
    users = csv.reader(csvfile, delimiter=';')
    for row in users:
        if row[1] == 'Наименование': continue
        sku = row[0]
        if sku != '':
            sku = int(sku)
        while sku in skus:
            sku = random.randint(0, 99999999)
        skus.append(sku)
        image = ''
        if (row[0] + '.jpg') in os.listdir('static/img'):
            image = row[0] + '.jpg'
        model.insert_ingredient(sku, row[1], row[2], row[3], '', image, row[4], row[5], row[6], row[7], row[8])