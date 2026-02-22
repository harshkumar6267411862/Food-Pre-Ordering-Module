import secrets
import os
from flask_login import login_user, current_user, logout_user
from food_ordering_module import app,bcrypt,db
from flask import render_template,redirect,url_for,request,flash,abort
from food_ordering_module.form import Registrationform,Loginform,OrderForm
from food_ordering_module.models import User,FoodItem, TimeSlot, Order
from flask_login import login_required
from sqlalchemy import func
from datetime import date

@app.route("/")
@app.route("/home")
@login_required
def home():

    # ---------------- STUDENT DASHBOARD ---------------- #
    if current_user.role == "student":

        total_spent = db.session.query(
            func.sum(Order.total_price)
        ).filter_by(user_id=current_user.id).scalar() or 0

        total_orders = Order.query.filter_by(
            user_id=current_user.id
        ).count()

        orders_by_day = db.session.query(
            func.date(Order.order_time),
            func.count(Order.id)
        ).filter_by(user_id=current_user.id)\
         .group_by(func.date(Order.order_time))\
         .all()

        peak_slot = db.session.query(
            Order.slot_id,
            func.count(Order.id).label("order_count")
        ).group_by(Order.slot_id)\
         .order_by(func.count(Order.id).desc())\
         .first()

        peak_slot_time = None

        if peak_slot:
            slot = TimeSlot.query.get(peak_slot.slot_id)
            peak_slot_time = slot.slot_time

        return render_template(
            "home.html",
            total_spent=total_spent,
            total_orders=total_orders,
            orders_by_day=orders_by_day,
            peak_slot_time=peak_slot_time,
            title="Student Dashboard"
        )

    # ---------------- ADMIN / VENDOR ---------------- #
    elif current_user.role in ["admin", "vendor"]:
        return redirect(url_for("admin_dashboard"))


    # ---------------- FALLBACK (SAFETY) ---------------- #
    return redirect(url_for("login"))



@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Registrationform()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,uni_id=form.uni_id.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created! you can now log-in', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html',title='User Resgistration',form=form)



@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Loginform()
    if form.validate_on_submit():
        user = User.query.filter_by(uni_id=form.uni_id.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('login failed. Check credentials.','danger')
    return render_template('login.html',title='User Login',form=form)



@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))



@app.route("/order", methods=['GET', 'POST'])
@login_required
def order_food():

    form = OrderForm()

    # Populate dropdowns dynamically
    form.food_id.choices = [
        (food.id, food.name) for food in FoodItem.query.filter_by(is_available=True).all()
    ]

    form.slot_id.choices = [
        (slot.id, slot.slot_time) for slot in TimeSlot.query.all()
    ]

    if form.validate_on_submit():

        food = FoodItem.query.get(form.food_id.data)
        slot = TimeSlot.query.get(form.slot_id.data)

        # Check food availability
        if form.quantity.data > food.available_quantity:
            flash("Not enough quantity available.", "danger")
            return redirect(url_for("order_food"))

        # Check slot capacity
        slot_orders_count = Order.query.filter_by(slot_id=slot.id).count()
        if slot_orders_count >= slot.max_capacity:
            flash("Selected time slot is full.", "danger")
            return redirect(url_for("order_food"))

        total_price = food.price * form.quantity.data

        order = Order(
            user_id=current_user.id,
            food_id=food.id,
            slot_id=slot.id,
            quantity=form.quantity.data,
            total_price=total_price
        )

        # Reduce food quantity
        food.available_quantity -= form.quantity.data

        db.session.add(order)
        db.session.commit()

        flash("Order placed successfully!", "success")
        return redirect(url_for("home"))

    return render_template("order.html", form=form, title="Order Food")

@app.route("/my-orders")
@login_required
def my_orders():

    orders = Order.query.filter_by(user_id=current_user.id)\
                        .order_by(Order.order_time.desc())\
                        .all()

    return render_template(
        "my_orders.html",
        title="My Orders",
        orders=orders
    )

@app.route("/admin/dashboard")
@login_required
def admin_dashboard():

    if current_user.role != "admin":
        abort(403)

    active_orders = Order.query.filter(
        Order.status != "Received"
    ).count()

    today = date.today()

    received_today = db.session.query(func.count(Order.id))\
        .filter(
            Order.status == "Received",
            func.date(Order.order_time) == today
        ).scalar()

    # Peak slot
    peak_slot = db.session.query(
        Order.slot_id,
        func.count(Order.id).label("order_count")
    ).group_by(Order.slot_id)\
     .order_by(func.count(Order.id).desc())\
     .first()

    peak_slot_time = None

    if peak_slot:
        slot = TimeSlot.query.get(peak_slot.slot_id)
        peak_slot_time = slot.slot_time

    return render_template(
        "admin_dashboard.html",
        active_orders=active_orders,
        received_today=received_today,
        peak_slot_time=peak_slot_time
    )


@app.route("/admin/manage-orders")
@login_required
def manage_orders():

    if current_user.role != "admin":
        abort(403)

    orders = Order.query.order_by(Order.order_time.desc()).all()

    return render_template(
        "manage_orders.html",
        orders=orders
    )

@app.route("/admin/update-status/<int:order_id>/<string:new_status>")
@login_required
def update_order_status(order_id, new_status):

    if current_user.role != "admin":
        abort(403)

    allowed_status = ["Pending", "Preparing", "Ready", "Received"]

    if new_status not in allowed_status:
        abort(400)

    order = Order.query.get_or_404(order_id)
    order.status = new_status
    db.session.commit()

    return redirect(url_for("manage_orders"))




