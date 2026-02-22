from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,BooleanField,DateField,IntegerField, SelectField
from wtforms.validators import DataRequired,Length,Email,ValidationError,EqualTo,NumberRange
from flask_login import current_user
from food_ordering_module.models import User

class Registrationform(FlaskForm):
    name = StringField('Name',
                           validators=[DataRequired(),Length(min=3,max=20)]
                           )
    
    uni_id = StringField('Uni_id',
                       validators=[DataRequired(),Length(min=8, max=8)]
                       )
    password = PasswordField('Password',
                             validators=[DataRequired()])
    
    submit = SubmitField('Register')

    
    def validate_id(self,uni_id):
        user = User.query.filter_by(uni_id=uni_id.data).first()
        if user:
            raise ValidationError(
                'Please Enter Valid University ID.'
            )

class Loginform(FlaskForm):
    uni_id = StringField('uni_id',validators=[DataRequired(),Length(min=8, max=8)])
    password = PasswordField('Password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class OrderForm(FlaskForm):

    food_id = SelectField("Select Food", coerce=int, validators=[DataRequired()])

    slot_id = SelectField("Select Time Slot", coerce=int, validators=[DataRequired()])

    quantity = IntegerField(
        "Quantity",
        validators=[DataRequired(), NumberRange(min=1, max=5)]
    )

    submit = SubmitField("Place Order")