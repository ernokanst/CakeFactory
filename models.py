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
        cursor.close()
        self.connection.commit()

    def insert_user(self, login, parol, rol="Заказчик", fio="", foto="default.png"):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO polzovatel 
                          (login, parol, rol, fio, foto) 
                          VALUES (?,?,?,?,?)''', (login, parol, rol, fio, foto))
        cursor.close()
        self.connection.commit()
        
    def insert_decoration(self, artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO ukrashenie 
                          (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves) 
                          VALUES (?,?,?,?,?,?,?,?,?)''', (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ukrasheniya, zakupochnaya_tsena, ves))
        cursor.close()
        self.connection.commit()    
    
    def insert_ingredient(self, artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost='', fasovka='', harakteristika=''):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO ingredient 
                          (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost, fasovka, harakteristika) 
                          VALUES (?,?,?,?,?,?,?,?,?,?,?)''', (artikul, naimenovanie, edinitsa_izmereniya, kolichestvo, postavschik, izobrazhenie, tip_ingredienta, zakupochnaya_tsena, gost, fasovka, harakteristika))
        cursor.close()
        self.connection.commit()     

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
