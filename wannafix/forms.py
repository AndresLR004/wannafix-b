from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DecimalField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, NumberRange, InputRequired, Email
import decimal

class LoginForm(FlaskForm):
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        validators=[ DataRequired()]
    )
    submit = SubmitField()

class RegisterForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        validators=[ DataRequired()]
    )
    submit = SubmitField()

class ProfileForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    password = PasswordField(
        # no es obligatori canviar-lo
    )
    submit = SubmitField()

class ResendForm(FlaskForm):
    email = StringField(
        validators = [Email(), DataRequired()]
    )
    submit = SubmitField()

class ServiceForm(FlaskForm):
    title = StringField(
        'Título',
        validators=[DataRequired()]
    )
    description = StringField(
        'Descripción',
        validators=[DataRequired()]
    )
    photo_file = FileField('Foto')
    price = DecimalField(
        'Precio',
        places=2,
        rounding=decimal.ROUND_HALF_UP,
        validators=[DataRequired(), NumberRange(min=0)]
    )
    duration_hours = DecimalField(
        'Duración (Horas)',
        places=2,
        rounding=decimal.ROUND_HALF_UP,
        validators=[DataRequired(), NumberRange(min=0)]
    )
    duration_days = DecimalField(
        'Duración (Días)',
        places=2,
        rounding=decimal.ROUND_HALF_UP,
        validators=[DataRequired(), NumberRange(min=0)]
    )
    category_id = SelectField(
        'Categoría',
        validators=[InputRequired()]
    )
    status_id = SelectField(
        'Estado',
        validators=[InputRequired()]
    )
    submit = SubmitField()
    
    
class CategoryForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    slug = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

class StatusForm(FlaskForm):
    name = StringField(
        validators = [DataRequired()]
    )
    slug = StringField(
        validators = [DataRequired()]
    )
    submit = SubmitField()

# class BlockUserForm(FlaskForm):
#     message = StringField(
#         validators = [DataRequired()]
#     )
#     submit = SubmitField()

# class BanProductForm(FlaskForm):
#     reason = StringField(
#         validators = [DataRequired()]
#     )
#     submit = SubmitField()

# # Formulari generic per a confirmar una acció
class ConfirmForm(FlaskForm):
    submit = SubmitField()