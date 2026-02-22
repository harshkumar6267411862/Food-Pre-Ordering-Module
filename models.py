from datetime import datetime,timezone
from food_ordering_module import db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(20), nullable=False)
    uni_id = db.Column(db.String(8), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="student")  # student/admin/vendor

    orders = db.relationship('Order', backref='student', lazy=True)

    def __repr__(self):
        return f"User('{self.name}', '{self.uni_id}')"

class FoodItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

    available_quantity = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    orders = db.relationship('Order', backref='food', lazy=True)

    def __repr__(self):
        return f"FoodItem('{self.name}', {self.price})"

class TimeSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    slot_time = db.Column(db.String(50), nullable=False)  # e.g. "10:30 - 11:00"
    max_capacity = db.Column(db.Integer, nullable=False)

    orders = db.relationship('Order', backref='slot', lazy=True)

    def __repr__(self):
        return f"TimeSlot('{self.slot_time}')"
    
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food_item.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('time_slot.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(
    db.Enum("Pending", "Preparing", "Ready", "Received"),
    default="Pending"
    )


    order_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Order(User={self.user_id}, Food={self.food_id}, Slot={self.slot_id})"