class Models:
    def __init__(self, connection):
        self.connection = connection

    def init_tables(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS polzovatel 
                            (login TEXT NOT NULL,
                             parol TEXT NOT NULL,
                             rol TEXT NOT NULL,
                             fio TEXT,
                             foto TEXT,
                             PRIMARY KEY (login, parol)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS izdelie 
                            (naimenovanie TEXT PRIMARY KEY NOT NULL,
                             razmery TEXT NOT NULL
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS zakaz
                            (nomer INTEGER NOT NULL,
                             data TEXT NOT NULL,
                             naimenovanie TEXT NOT NULL,
                             izdelie TEXT NOT NULL,
                             zakazchik TEXT NOT NULL,
                             menedzher TEXT,
                             stoimost REAL,
                             planovaya_data TEXT,
                             primery TEXT,
                             PRIMARY KEY (nomer, data),
                             FOREIGN KEY(izdelie) REFERENCES izdelie(naimenovanie),
                             FOREIGN KEY(zakazchik) REFERENCES polzovatel(login),
                             FOREIGN KEY(menedzher) REFERENCES polzovatel(login)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tip_oborudovaniya
                            (tip_oborudovaniya TEXT PRIMARY KEY NOT NULL
                             )''')        
        cursor.execute('''CREATE TABLE IF NOT EXISTS oborudovanie
                            (markirovka TEXT PRIMARY KEY NOT NULL,
                             tip_oborudovaniya TEXT NOT NULL,
                             harakteristiki TEXT,
                             FOREIGN KEY(tip_oborudovaniya) REFERENCES tip_oborudovaniya(tip_oborudovaniya)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS spetsifikatsiya_operatsii
                            (izdelie TEXT NOT NULL,
                             operatsiya TEXT NOT NULL,
                             poryadkovyy_nomer INTEGER NOT NULL,
                             tip_oborudovaniya TEXT,
                             vremya TEXT NOT NULL,
                             PRIMARY KEY (izdelie, operatsiya, poryadkovyy_nomer),
                             FOREIGN KEY(izdelie) REFERENCES izdelie(naimenovanie)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS spetsifikatsiya_polufabrikaty
                            (izdelie TEXT NOT NULL,
                             polufabrikat TEXT NOT NULL,
                             kolichestvo INTEGER NOT NULL,
                             PRIMARY KEY (izdelie, polufabrikat),
                             FOREIGN KEY(izdelie) REFERENCES izdelie(naimenovanie),
                             FOREIGN KEY(polufabrikat) REFERENCES izdelie(naimenovanie)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS postavschik
                            (naimenovanie TEXT PRIMARY KEY NOT NULL,
                             adres TEXT,
                             srok_dostavki TEXT NOT NULL
                             )''')           
        cursor.execute('''CREATE TABLE IF NOT EXISTS ukrashenie
                            (artikul INTEGER PRIMARY KEY NOT NULL,
                             naimenovanie TEXT NOT NULL,
                             edinitsa_izmereniya TEXT NOT NULL,
                             kolichestvo INTEGER NOT NULL,
                             postavschik TEXT,
                             izobrazhenie TEXT,
                             tip_ukrasheniya TEXT NOT NULL,
                             zakupochnaya_tsena REAL NOT NULL,
                             ves REAL NOT NULL,
                             srok_godnosti TEXT NOT NULL,
                             FOREIGN KEY(postavschik) REFERENCES postavschik(naimenovanie)
                             )''')        
        cursor.execute('''CREATE TABLE IF NOT EXISTS spetsifikatsiya_ukrasheniya
                            (izdelie TEXT NOT NULL,
                             ukrashenie INTEGER NOT NULL,
                             kolichestvo INTEGER NOT NULL,
                             PRIMARY KEY (izdelie, ukrashenie),
                             FOREIGN KEY(izdelie) REFERENCES izdelie(naimenovanie),
                             FOREIGN KEY(ukrashenie) REFERENCES ukrashenie(artikul)
                             )''')       
        cursor.execute('''CREATE TABLE IF NOT EXISTS ingredient
                            (artikul INTEGER PRIMARY KEY NOT NULL,
                             naimenovanie TEXT NOT NULL,
                             edinitsa_izmereniya TEXT NOT NULL,
                             kolichestvo INTEGER NOT NULL,
                             postavschik TEXT,
                             izobrazhenie TEXT,
                             tip_ingredienta TEXT NOT NULL,
                             zakupochnaya_tsena TEXT NOT NULL,
                             gost TEXT,
                             fasovka TEXT,
                             harakteristika TEXT,
                             srok_godnosti TEXT NOT NULL,
                             FOREIGN KEY(postavschik) REFERENCES postavschik(naimenovanie)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS spetsifikatsiya_ingredienty
                            (izdelie TEXT NOT NULL,
                             ingredient INTEGER NOT NULL,
                             kolichestvo INTEGER NOT NULL,
                             PRIMARY KEY (izdelie, ingredient),
                             FOREIGN KEY(izdelie) REFERENCES izdelie(naimenovanie),
                             FOREIGN KEY(ingredient) REFERENCES ingredient(artikul)
                             )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS instrument
                            (naimenovanie TEXT NOT NULL,
                             opisanie TEXT,
                             tip_instrumenta TEXT NOT NULL,
                             stepen_iznosa TEXT,
                             postavschik TEXT,
                             data_priobreteniya TEXT NOT NULL,
                             kolichestvo TEXT NOT NULL,
                             FOREIGN KEY(postavschik) REFERENCES postavschik(naimenovanie)
                             )''')        
        cursor.close()
        self.connection.commit()

    def insert_user(self, login, parol, rol="Заказчик", fio="", foto="default.png"):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO polzovatel 
                          (login, parol, rol, fio, foto) 
                          VALUES (?,?,?,?,?)''', (login, parol, rol, fio, foto))
        cursor.close()
        self.connection.commit()
        
    def insert_decoration(self, artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves, srok_godnosti=''):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO ukrashenie 
                          (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves, srok_godnosti) 
                          VALUES (?,?,?,?,?,?,?,?,?,?)''', (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves, srok_godnosti))
        cursor.close()
        self.connection.commit()    
    
    def insert_ingredient(self, artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost='', fasovka='', harakteristika='', srok_godnosti=''):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO ingredient 
                          (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost, fasovka, harakteristika, srok_godnosti) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''', (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost, fasovka, harakteristika, srok_godnosti))
        cursor.close()
        self.connection.commit()
    
    def update_ingredient(self, artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost='', fasovka='', harakteristika='', srok_godnosti=''):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE ingredient SET
                          naimenovanie = ?, edinitsa_izmereniya = ?, kolichestvo = ?, postavschik = ?, izobrazhenie = ?, tip_ingredienta = ?, zakupochnaya_tsena = ?, gost = ?, fasovka = ?, harakteristika = ?, srok_godnosti = ?
                          WHERE artikul = ?''', (naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost, fasovka, harakteristika, srok_godnosti, artikul))
        cursor.close()
        self.connection.commit()    
    
    def insert_instrument(self, naimenovanie, opisanie, tip_instrumenta, stepen_iznosa, postavschik, data_priobreteniya, kolichestvo):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO instrument 
                          (naimenovanie, opisanie, tip_instrumenta, stepen_iznosa, postavschik, data_priobreteniya, kolichestvo) 
                          VALUES (?,?,?,?,?,?,?)''', (naimenovanie, opisanie, tip_instrumenta, stepen_iznosa, postavschik, data_priobreteniya, kolichestvo))
        cursor.close()
        self.connection.commit()
    
    def get_instruments(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM instrument")
        rows = cursor.fetchall()
        return rows
    
    def get_ingredient(self, artikul):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM ingredient WHERE artikul = ?", (artikul,))
        row = cursor.fetchone()
        return row if row else False
    
    def delete_ingredient(self, artikul):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM ingredient WHERE artikul = ?''',
                           (str(artikul),))
        cursor.close()
        self.connection.commit()    
    
    def get_ingredients(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM ingredient")
        rows = cursor.fetchall()
        return rows
    
    def update_decoration(self, artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves, srok_godnosti=''):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE ukrashenie SET
                          naimenovanie = ?, edinitsa_izmereniya = ?, kolichestvo = ?, postavschik = ?, izobrazhenie = ?, tip_ukrasheniya = ?, zakupochnaya_tsena = ?, ves = ?, srok_godnosti = ?
                          WHERE artikul = ?''', (naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves, srok_godnosti, artikul))
        cursor.close()
        self.connection.commit()
        
    def get_decoration(self, artikul):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM ukrashenie WHERE artikul = ?", (artikul,))
        row = cursor.fetchone()
        return row if row else False
    
    def delete_decoration(self, artikul):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM ukrashenie WHERE artikul = ?''',
                           (str(artikul),))
        cursor.close()
        self.connection.commit()    
    
    def get_decorations(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM ukrashenie")
        rows = cursor.fetchall()
        return rows    
    
    def get_supplier(self, naimenovanie):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM postavschik WHERE naimenovanie = ?", (naimenovanie,))
        row = cursor.fetchone()
        return (True, row) if row else (False,)
    
    def normalize_price(p):
        price = p
        if "руб" in price:
            price = price.split("руб")[0]
            if "до" in price:
                price = price.split("до")[1]
        if "р/т" in price:
            price = price.replace("р/т", '')
        if "'" in price:
            price = price.replace("'", '')
        if "." in price:
            price = price.split(".")
        if "," in price:
            price = price.split(",")
        if "-" in price:
            price = price.split("-")
        if isinstance(price, list):
            price = float(price[0]) + float("0." + price[1])
        else:
            price = float(price)
        return price
        
    
    def get(self, login):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM polzovatel WHERE login = ?", (str(login),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM polzovatel")
        rows = cursor.fetchall()
        return rows

    def exists(self, login, parol):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM polzovatel WHERE login = ? AND parol = ?", (login, parol))
        row = cursor.fetchone()
        return (True, row) if row else (False,)

    def login_used(self, login):
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT * FROM polzovatel WHERE login = ?", (login,))
        row = cursor.fetchone()
        return True if row else False
