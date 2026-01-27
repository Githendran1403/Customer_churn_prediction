from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PredictionForm(FlaskForm):
    customer_name = StringField('Customer Name', validators=[DataRequired(), Length(min=2, max=100)])
    tenure = FloatField('Tenure (Months)', validators=[DataRequired(), NumberRange(min=0, max=100)])
    monthly_charges = FloatField('Monthly Charges (₹)', validators=[DataRequired(), NumberRange(min=0, max=50000)])
    total_charges = FloatField('Total Charges (₹)', validators=[DataRequired(), NumberRange(min=0, max=500000)])
    
    contract_type = SelectField('Contract Type', 
                               choices=[('Month-to-month', 'Month-to-month'),
                                       ('One year', 'One year'),
                                       ('Two year', 'Two year')],
                               validators=[DataRequired()])
    
    payment_method = SelectField('Payment Method',
                                choices=[('Electronic check', 'Electronic check'),
                                        ('Mailed check', 'Mailed check'),
                                        ('Bank transfer (automatic)', 'Bank transfer (automatic)'),
                                        ('Credit card (automatic)', 'Credit card (automatic)'),
                                        ('UPI', 'UPI (Unified Payments Interface)'),
                                        ('Net Banking', 'Net Banking'),
                                        ('Digital Wallet', 'Digital Wallet (Paytm/PhonePe/GPay)')],
                                validators=[DataRequired()])
    
    submit = SubmitField('Predict Churn')