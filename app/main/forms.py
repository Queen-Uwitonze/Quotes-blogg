from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField
from wtforms.validators import Required,Email
from ..models import Subscribe
class BlogForm(FlaskForm):
   
    blog = TextAreaField('blog',validators=[Required()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):

    description= TextAreaField('comment', validators=[Required()])
    submit = SubmitField('Submit')

class SubscribeForm(FlaskForm):
    email = StringField('Your Email Address',validators=[Required(),Email()])
    submit = SubmitField('Submit')
    
    # def validate_email(self,data_field):
    #         if Subscribe.query.filter_by(email =data_field.data).first():
    #             raise ValidationError('There is an account with that email')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')

