from db import DB
from flask import Flask, redirect, render_template, session
from loginform import LoginForm
from regform import RegForm
from models import Models
from werkzeug.utils import secure_filename
import os, time, datetime
from add_instrument import AddInstrumentForm
from date_filter import DateFilterForm
from ingredient_form import IngredientForm, DeleteForm
from decoration_form import DecorationForm


#Заказчик loginDErwk2018 |nZOKu
#Менеджер по закупкам loginDEoni2018 phdlXA
#Менеджер по продажам loginDEpri2018 RI2*T9
#Мастер loginDEitt2018 L+OKpQ
#Директор loginDEgju2018 C7nYc{


app = Flask(__name__)
app.config['SECRET_KEY'] = 'jOaqY9515WL6IxQB'
db = DB('db.db')
#attempts = 0
#enabled = True

@app.route('/login', methods=['GET', 'POST'])
def login():
    #global attempts
    #attempts += 1
    error = None
    #global enabled
    #print(attempts, enabled)
    form = LoginForm()
    #if attempts > 3 and not enabled:
        #time.sleep(5)
        #enabled = True
        #return render_template('login.html', title='Авторизация', form=form, error=error, attempts=attempts, enabled=enabled)
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        models = Models(db.get_connection())
        exists = models.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['role'] = exists[1][2]
            session['content'] = exists[1][-1]
            attempts = 0
            return redirect("/")
        else:
            error = 'Логин или пароль неверны'
            #if attempts > 3:
                #error += ". Подождите 5 секунд" 
                #enabled = False
    return render_template('login.html', title='Авторизация', form=form, error=error, enabled=True)


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    form = RegForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        repassword = form.repassword.data
        fio = form.fio.data
        content = form.content.data
        models = Models(db.get_connection())
        exists = models.login_used(user_name)
        if exists:
            error = 'Пользователь с таким логином уже существует'
            return render_template('register.html', title='Регистрация', form=form, error=error)
        else:
            if password == repassword and user_name not in password:
                if content:
                    filename = secure_filename(content.filename)
                    if os.path.isfile(os.path.join('static', 'img', filename)):
                        while os.path.isfile(os.path.join('static', 'img', filename)):
                            filename = filename.split('.')
                            filename = '.'.join(
                                [filename[0] + 'A', filename[-1]])
                    content.save(os.path.join('static', 'img', filename))
                    models.insert(user_name, password, "Заказчик", fio, filename)
                else:
                    models.insert(user_name, password, "Заказчик", fio)
                exists = models.exists(user_name, password)
                session['username'] = user_name
                session['role'] = exists[1][2]
                session['content'] = exists[1][-1]
            else:
                error = 'Пароль не должен содержать логин. Пароль и проверка пароля должны совпадать.'
                return render_template('register.html', title='Регистрация', form=form, error=error)
        return redirect("/")
    return render_template('register.html', title='Регистрация', form=form, error=error)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('role', 0)
    session.pop('content', 0)
    return redirect('/login')


@app.route('/')
def main():
    if 'role' in session:
        if session['role'] == 'Заказчик':
            return redirect('/customer')
        if session['role'] == 'Менеджер по продажам':
            return redirect('/csmanager')
        if session['role'] == 'Менеджер по закупкам':
            return redirect('/manager')
        if session['role'] == 'Мастер':
            return redirect('/master')
        if session['role'] == 'Директор':
            return redirect('/director')
    return render_template('main.html')


@app.route('/main')
def redirect_to_main():
    return redirect('/')


@app.route('/customer')
def customer():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Заказчик':
        return redirect('/')
    return render_template('customer.html')


@app.route('/csmanager')
def csmanager():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Менеджер по продажам':
        return redirect('/')
    return render_template('csmanager.html')


@app.route('/manager')
def manager():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Менеджер по закупкам':
        return redirect('/')
    return render_template('manager.html')


@app.route('/master')
def master():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Мастер':
        return redirect('/')
    return render_template('master.html')


@app.route('/director')
def director():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор':
        return redirect('/')
    return render_template('director.html')


@app.route('/instruments')
def instruments():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор':
        return redirect('/')
    models = Models(db.get_connection())
    instruments = []
    for row in models.get_instruments():
        d1 = datetime.datetime.now()
        d2 = datetime.datetime.fromisoformat(row[5])
        time = (d1.year - d2.year) * 12 + d1.month - d2.month
        instruments.append([row[0], row[2], time, row[6]])
    return render_template('instruments.html', instruments=instruments)


@app.route('/add_instrument', methods=['GET', 'POST'])
def add_instrument():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор':
        return redirect('/')
    form = AddInstrumentForm()
    if form.validate_on_submit():
        models = Models(db.get_connection())
        models.insert_instrument(form.naimenovanie.data, form.opisanie.data, form.tip_instrumenta.data, form.stepen_iznosa.data, form.postavschik.data, form.data_priobreteniya.data, form.kolichestvo.data)
        return redirect("/instruments")
    return render_template('add_instrument.html', title='Добавить инструмент', form=form)

@app.route('/ingredients', methods=['GET', 'POST'])
def ingredients():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] == 'Заказчик':
        return redirect('/')
    models = Models(db.get_connection())
    ins = models.get_ingredients()
    form = DateFilterForm()
    if form.validate_on_submit():
        ingredients = []
        price = 0.0
        for row in ins:
            if row[11] != '' and row[11] >= str(form.date_from.data) and row[11] <= str(form.date_till.data):
                sku = '0' * (8 - len(str(row[0]))) + str(row[0])
                supply_date = ''
                supplier = models.get_supplier(row[4])
                if (supplier[0]):
                    supply_date = supplier[1][2]
                amount = 0.0
                if row[3] != '':
                    amount = float(row[3])
                if row[7] != '':
                    price += Models.normalize_price(row[7]) * amount
                ingredients.append([sku, row[1], amount, row[2], row[7], row[4], supply_date, row[11], row[0]])
        return render_template('ingredients.html', form=form, ingredients=ingredients,  current=len(ingredients), overall=len(ins), price=price, role=session['role'])    
    ingredients = []
    price = 0.0
    for row in ins:
        sku = '0' * (8 - len(str(row[0]))) + str(row[0])
        supply_date = ''
        supplier = models.get_supplier(row[4])
        if (supplier[0]):
            supply_date = supplier[1][2]
        amount = 0.0
        if row[3] != '':
            amount = float(row[3])
        if row[7] != '':
            price += Models.normalize_price(row[7]) * amount
        ingredients.append([sku, row[1], amount, row[2], row[7], row[4], supply_date, row[11], row[0]])
    return render_template('ingredients.html', form=form, ingredients=ingredients,  current=len(ingredients), overall=len(ins), price=price, role=session['role'])


@app.route('/update_ingredient/<int:artikul>', methods=['GET', 'POST'])
def update_ingredient(artikul):
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор' and session['role'] != 'Менеджер по закупкам':
        return redirect('/')
    models = Models(db.get_connection())
    ing = list(models.get_ingredient(artikul))
    if ing:
        if ing[7] != '':
            ing[7] = float(Models.normalize_price(ing[7]))
        else:
            ing[7] = 0.0
        if ing[3] != '':
            ing[3] = float(ing[3])
        else:
            ing[3] = 0.0
        if ing[11] != '':
            ing[11] = datetime.date.fromisoformat(ing[11])
        else:
            ing[11] = datetime.date.today()
        form = IngredientForm(artikul=ing[0], 
        naimenovanie=ing[1],
        edinitsa_izmereniya=ing[2],
        kolichestvo=ing[3],
        postavschik=ing[4],
        tip_ingredienta=ing[6],
        zakupochnaya_tsena=ing[7],
        gost=ing[8],
        fasovka=ing[9],
        harakteristika=ing[10],
        srok_godnosti=ing[11])
        if form.validate_on_submit():
            filename = ''
            if form.izobrazhenie.data:
                filename = secure_filename(form.izobrazhenie.data.filename)
                if os.path.isfile(os.path.join('static', 'img', filename)):
                    while os.path.isfile(os.path.join('static', 'img', filename)):
                        filename = filename.split('.')
                        filename = '.'.join(
                            [filename[0] + 'A', filename[-1]])
                form.izobrazhenie.data.save(os.path.join('static', 'img', filename))
            models.update_ingredient(form.artikul.data, form.naimenovanie.data, form.edinitsa_izmereniya.data, float(form.kolichestvo.data), form.postavschik.data, form.izobrazhenie.data,
                                     form.tip_ingredienta.data, float(form.zakupochnaya_tsena.data), form.gost.data, form.fasovka.data, form.harakteristika.data, form.srok_godnosti.data)
            return redirect('/ingredients')
    else:
        return redirect('/ingredients')
    return render_template('update_ingredient.html', title='Редактирование ингредиента', form=form)


@app.route('/delete_ingredient/<int:artikul>', methods=['GET', 'POST'])
def delete_ingredient(artikul):
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор' and session['role'] != 'Менеджер по закупкам':
        return redirect('/')
    models = Models(db.get_connection())
    ing = list(models.get_ingredient(artikul))
    if ing:
        form = DeleteForm()
        if form.validate_on_submit():
            models.delete_ingredient(artikul)
            return redirect('/ingredients')
    else:
        return redirect('/ingredients')
    return render_template('delete.html', title='Удаление ингредиента', form=form, name=ing[1], item="ingredients")


@app.route('/decorations', methods=['GET', 'POST'])
def decorations():
    if 'role' not in session:
        return redirect('/login')
    if session['role'] == 'Заказчик':
        return redirect('/')
    models = Models(db.get_connection())
    dec = models.get_decorations()
    form = DateFilterForm()
    if form.validate_on_submit():
        decorations = []
        price = 0.0
        for row in dec:
            if row[9] != '' and row[9] >= str(form.date_from.data) and row[9] <= str(form.date_till.data):
                sku = '0' * (8 - len(str(row[0]))) + str(row[0])
                supply_date = ''
                supplier = models.get_supplier(row[4])
                if (supplier[0]):
                    supply_date = supplier[1][2]
                amount = 0.0
                if row[3] != '':
                    amount = float(row[3])
                if row[7] != '':
                    price += float(row[7]) * amount
                decorations.append([sku, row[1], amount, row[2], row[7], row[4], supply_date, row[9], row[0]])
        return render_template('decorations.html', form=form, decorations=decorations,  current=len(decorations), overall=len(dec), price=price, role=session['role'])    
    decorations = []
    price = 0.0
    for row in dec:
        sku = '0' * (8 - len(str(row[0]))) + str(row[0])
        supply_date = ''
        supplier = models.get_supplier(row[4])
        if (supplier[0]):
            supply_date = supplier[1][2]
        amount = 0.0
        if row[3] != '':
            amount = float(row[3])
        if row[7] != '':
            price += float(row[7]) * amount
        decorations.append([sku, row[1], amount, row[2], row[7], row[4], supply_date, row[9], row[0]])
    return render_template('decorations.html', form=form, decorations=decorations,  current=len(decorations), overall=len(dec), price=price, role=session['role'])


@app.route('/update_decoration/<int:artikul>', methods=['GET', 'POST'])
def update_decoration(artikul):
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор' and session['role'] != 'Менеджер по закупкам':
        return redirect('/')
    models = Models(db.get_connection())
    dec = list(models.get_decoration(artikul))
    if dec:
        if dec[7] != '':
            dec[7] = float(dec[7])
        else:
            dec[7] = 0.0
        if dec[3] != '':
            dec[3] = float(dec[3])
        else:
            dec[3] = 0.0
        if dec[9] != '':
            dec[9] = datetime.date.fromisoformat(dec[9])
        else:
            dec[9] = datetime.date.today()
        form = DecorationForm(artikul=dec[0], 
        naimenovanie=dec[1],
        edinitsa_izmereniya=dec[2],
        kolichestvo=dec[3],
        postavschik=dec[4],
        tip_ukrasheniya=dec[6],
        zakupochnaya_tsena=dec[7],
        ves=dec[8],
        srok_godnosti=dec[9])
        if form.validate_on_submit():
            filename = ''
            if form.izobrazhenie.data:
                filename = secure_filename(form.izobrazhenie.data.filename)
                if os.path.isfile(os.path.join('static', 'img', filename)):
                    while os.path.isfile(os.path.join('static', 'img', filename)):
                        filename = filename.split('.')
                        filename = '.'.join(
                            [filename[0] + 'A', filename[-1]])
                form.izobrazhenie.data.save(os.path.join('static', 'img', filename))
            models.update_decoration(form.artikul.data, form.naimenovanie.data, form.edinitsa_izmereniya.data, float(form.kolichestvo.data), form.postavschik.data, form.izobrazhenie.data,
                                     form.tip_ukrasheniya.data, float(form.zakupochnaya_tsena.data), form.ves.data, form.srok_godnosti.data)
            return redirect('/decorations')
    else:
        return redirect('/decorations')
    return render_template('update_decoration.html', title='Редактирование украшения для торта', form=form)


@app.route('/delete_decoration/<int:artikul>', methods=['GET', 'POST'])
def delete_decoration(artikul):
    if 'role' not in session:
        return redirect('/login')
    if session['role'] != 'Директор' and session['role'] != 'Менеджер по закупкам':
        return redirect('/')
    models = Models(db.get_connection())
    dec = list(models.get_decoration(artikul))
    if dec:
        form = DeleteForm()
        if form.validate_on_submit():
            models.delete_decoration(artikul)
            return redirect('/decorations')
    else:
        return redirect('/decorations')
    return render_template('delete.html', title='Удаление украшения для торта', form=form, name=dec[1], item="decorations")


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
