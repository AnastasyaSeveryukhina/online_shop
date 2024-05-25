from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import db
from models import User, Product, Order, OrderProduct
import logging
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

logging.basicConfig(level=logging.DEBUG)


# страница с шаблоном для всех остальных
@app.route('/')
def base():
    return render_template('base.html')

# главная страница
@app.route('/index')
def index():
    return render_template('index.html')

# страница с каталогом, где выбор категроий
@app.route('/catalog')
def catalog():
    return render_template('catalog.html')

# корзина
@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    items = OrderProduct.query.all()
    products = Product.query.all()
    product_dict = {}
    for product in products:
        product_dict[product.id] = product

    return render_template('cart.html', user=user, data=items, products=product_dict)

# вход в личный кабинет
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('profile'))
        else:
            flash('Invalid email or password')
    return render_template('login.html')

# выход из личного кабинета
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

# регистрация, заполнение бд User
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
        else:
            new_user = User(first_name=first_name, last_name=last_name, email=email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            return redirect(url_for('profile'))
    return render_template('register.html')

# личный кабинет
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        flash('You need to be logged in to view this page')
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found')
        return redirect(url_for('login'))
    return render_template('profile.html', user=user)

# редактирование данных профиля
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found')
        return redirect(url_for('login'))
    if request.method == 'POST':
        new_first_name = request.form['first_name']
        new_last_name = request.form['last_name']
        new_email = request.form['email']
        new_password = request.form['password']
        user.first_name = new_first_name
        user.last_name = new_last_name
        user.email = new_email
        if new_password:
            user.set_password(new_password)
        db.session.commit()
        flash('Account updated successfully')
        return redirect(url_for('profile'))
    return render_template('edit_profile.html', user=user)

# история заказов
@app.route('/order_history')
def order_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found')
        return redirect(url_for('login'))
    return render_template('order_history.html', user=user)


# добавление товара в корзину?
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        quantity = request.form['quantity']
        product_id = request.form['product_id']
        if "created_order" not in session:
            try:
                new_order = Order(user_id=session['user_id'], total_price=0)
                db.session.add(new_order)
                db.session.commit()
                session['created_order'] = new_order.id
            except Exception as e:
                return f"Error: {e}"

        new_order_product = OrderProduct(product_id=product_id, quantity=quantity, order_id=session['created_order'])
        try:
            db.session.add(new_order_product)
            db.session.commit()
            return redirect(url_for('cart'))
        except Exception as e:
            return f"Error: {e}"
    else:
        return render_template('checkout.html')

# очистить корзину
@app.route('/clear-cart', methods=['POST'])
def clear_cart():
    # Here you would implement the logic to clear the cart in the database
    flash('Cart cleared successfully')
    return jsonify({'message': 'Cart cleared successfully'})

#  просто таблица пользователей
@app.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# заказы
@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('orders.html', orders=orders)

# страница товаров для мужчин
@app.route('/for_men')
def for_men():
    products = Product.query.filter_by(category='Мужчины').all()
    return render_template('for_men.html', data=products)

# страница товаров для женщин
@app.route('/for_women')
def for_women():
    products = Product.query.filter_by(category='Женщины').all()
    return render_template('for_women.html', data=products)

# страница товаров для детей
@app.route('/for_kids')
def for_kids():
    products = Product.query.filter_by(category='Дети').all()
    return render_template('for_kids.html', data=products)

# страница аксессуаров
@app.route('/accessories')
def accessories():
    products = Product.query.filter_by(category='Аксессуары').all()
    return render_template('accessories.html', data=products)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", debug=True)
