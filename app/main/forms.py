import datetime
from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, RadioField, DecimalField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Email, Optional

class ResumeForm(FlaskForm):
    resume = RadioField(
        'Do you want to resume your application?',
        choices=[('yes', 'Yes, resume the application'), ('no', 'No, delete saved progress and start over')],
        validators=[DataRequired()]
    )

class JavaAccountForm(FlaskForm):
    java_account = RadioField(
        'Do you have a Minecraft: Java Edition account?',
        choices=[('yes', 'Yes'), ('no-bedrock', 'No, I have a Minecraft (Bedrock Edition) account'), ('no', 'No, I do not have any Minecraft account')],
        validators=[DataRequired()]
    )

class UsernameForm(FlaskForm):
    minecraft_username = StringField('Minecraft Username', validators=[DataRequired()])

class LandPermissionForm(FlaskForm):
    land_permission = RadioField(
        'Do you own the land or have permission to build?',
        choices=[('yes-owned', 'Yes, I own the land'), ('yes-permission', 'Yes, I have permission'), ('no', 'No')],
        validators=[DataRequired()]
    )

class ConstructionTypeForm(FlaskForm):
    construction_type = RadioField(
        'What type of construction are you planning?',
        choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('industrial', 'Industrial'), ('other', 'Other')],
        validators=[DataRequired()]
    )

class CoordinatesForm(FlaskForm):
    coord_x = DecimalField('X Coordinate', places=0, validators=[DataRequired()])
    coord_z = DecimalField('Z Coordinate', places=0, validators=[DataRequired()])

class SocietyImpactForm(FlaskForm):
    social_impact_description = TextAreaField(
        'Describe how your construction might impact Samland’s society',
        validators=[DataRequired()]
    )

class VisualDescriptionForm(FlaskForm):
    visual_description = TextAreaField(
        "Describe what the construction will look like",
        validators=[DataRequired()]
    )

class ConstructionDateForm(FlaskForm):
    # Start date fields
    start_day = IntegerField("Day", validators=[
        DataRequired(), NumberRange(min=1, max=31)
    ])
    start_month = IntegerField("Month", validators=[
        DataRequired(), NumberRange(min=1, max=12)
    ])
    start_year = IntegerField("Year", validators=[
        DataRequired(), NumberRange(min=1900, max=2100)
    ])

    # End date fields
    end_day = IntegerField("Day", validators=[
        DataRequired(), NumberRange(min=1, max=31)
    ])
    end_month = IntegerField("Month", validators=[
        DataRequired(), NumberRange(min=1, max=12)
    ])
    end_year = IntegerField("Year", validators=[
        DataRequired(), NumberRange(min=1900, max=2100)
    ])

    def validate(self, extra_validators=None):
        if not super().validate():
            return False

        try:
            self.start_date = datetime.date(self.start_year.data, self.start_month.data, self.start_day.data)
        except ValueError:
            self.start_day.errors.append("Enter a valid start date")
            return False

        try:
            self.end_date = datetime.date(self.end_year.data, self.end_month.data, self.end_day.data)
        except ValueError:
            self.end_day.errors.append("Enter a valid end date")
            return False

        if self.start_date > self.end_date:
            self.end_day.errors.append("End date must be after the start date")
            return False

        return True

class EmailForm(FlaskForm):
    email = StringField("Email", validators=[Optional(), Email(message="Enter a valid email address")])
