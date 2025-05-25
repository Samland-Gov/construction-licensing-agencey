import datetime
from flask import redirect, render_template, request, session, url_for

from app.main import bp

from app.main.forms import ResumeForm, JavaAccountForm, UsernameForm, LandPermissionForm, ConstructionTypeForm, CoordinatesForm, SocietyImpactForm, VisualDescriptionForm, ConstructionDateForm, EmailForm

def save_answer(field, value):
    session.setdefault("application_data", {})
    session["application_data"][field] = value
    session.modified = True

def get_answer(field):
    return session.get("application_data", {}).get(field, None)

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/apply/", methods=["GET"])
def apply_index():
    next_step = url_for("main.question_1")
    if "application_data" in session:
        next_step = url_for("main.resume")
    return render_template("apply/index.html", next_step=next_step)

@bp.route("/apply/resume", methods=["GET", "POST"])
def resume():
    form = ResumeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            if form.resume.data == "yes":
                last_question = session["last_question"]
                return redirect(url_for(f"main.question_{last_question}"))
            else:
                session.pop("application_data", None)
                session.pop("last_question", None)
                return redirect(url_for("main.question_1"))
    return render_template("apply/resume.html", form=form)

@bp.route("/apply/question-1", methods=["GET", "POST"])
def question_1():
    form = JavaAccountForm()
    if form.validate_on_submit():
        save_answer("java_account", form.java_account.data)
        session["last_question"] = 1
        if form.java_account.data == "no":
            return redirect(url_for("main.ineligible"))
        if form.java_account.data == "no-bedrock":
            return redirect(url_for("main.ineligible"))
        return redirect(url_for("main.question_2"))
    form.java_account.data = get_answer("java_account")
    return render_template("apply/question-1.html", form=form)

@bp.route("/apply/question-2", methods=["GET", "POST"])
def question_2():
    form = UsernameForm()
    if form.validate_on_submit():
        save_answer("minecraft_username", form.minecraft_username.data)
        session["last_question"] = 2
        return redirect(url_for("main.question_3"))
    form.minecraft_username.data = get_answer("minecraft_username")
    return render_template("apply/question-2.html", form=form)

@bp.route("/apply/question-3", methods=["GET", "POST"])
def question_3():
    form = LandPermissionForm()
    if form.validate_on_submit():
        save_answer("land_permission", form.land_permission.data)
        session["last_question"] = 3
        if form.land_permission.data == "no":
            return redirect(url_for("main.ineligible"))
        return redirect(url_for("main.question_4"))
    form.land_permission.data = get_answer("land_permission")
    return render_template("apply/question-3.html", form=form)

@bp.route("/apply/question-4", methods=["GET", "POST"])
def question_4():
    form = ConstructionTypeForm()
    if form.validate_on_submit():
        save_answer("construction_type", form.construction_type.data)
        session["last_question"] = 5
        return redirect(url_for("main.question_5"))
    form.construction_type.data = get_answer("construction_type")
    return render_template("apply/question-4.html", form=form)

@bp.route("/apply/question-5", methods=["GET", "POST"])
def question_5():
    form = CoordinatesForm()
    if form.validate_on_submit():
        save_answer("coord_x", form.coord_x.data)
        save_answer("coord_z", form.coord_z.data)
        session["last_question"] = 5
        return redirect(url_for("main.question_6"))
    form.coord_x.data = get_answer("coord_x")
    form.coord_z.data = get_answer("coord_z")
    return render_template("apply/question-5.html", form=form)

@bp.route("/apply/question-6", methods=["GET", "POST"])
def question_6():
    form = SocietyImpactForm()
    if form.validate_on_submit():
        save_answer("social_impact_description", form.social_impact_description.data)
        session["last_question"] = 6
        return redirect(url_for("main.question_7"))
    form.social_impact_description.data = get_answer("social_impact_description")
    return render_template("apply/question-6.html", form=form)

@bp.route("/apply/question-7", methods=["GET", "POST"])
def question_7():
    form = VisualDescriptionForm()
    if form.validate_on_submit():
        save_answer("visual_description", form.visual_description.data)
        session["last_question"] = 7
        return redirect(url_for("main.question_8"))
    form.visual_description.data = get_answer("visual_description")
    return render_template("apply/question-7.html", form=form)

@bp.route("/apply/question-8", methods=["GET", "POST"])
def question_8():
    form = ConstructionDateForm()

    if form.validate_on_submit():
        # These are set in the form's validate() method
        save_answer("start_date", form.start_date.isoformat())
        save_answer("end_date", form.end_date.isoformat())
        session["last_question"] = 8
        return redirect(url_for("main.confirmation"))  # or next step

    # Pre-populate form fields if data exists in session
    start_date_str = get_answer("start_date")
    if start_date_str:
        try:
            start_date = datetime.date.fromisoformat(start_date_str)
            form.start_day.data = start_date.day
            form.start_month.data = start_date.month
            form.start_year.data = start_date.year
        except ValueError:
            pass

    end_date_str = get_answer("end_date")
    if end_date_str:
        try:
            end_date = datetime.date.fromisoformat(end_date_str)
            form.end_day.data = end_date.day
            form.end_month.data = end_date.month
            form.end_year.data = end_date.year
        except ValueError:
            pass

    return render_template("apply/question-8.html", form=form)

@bp.route("/apply/confirmation", methods=["GET"])
def confirmation():
    data = session.get("application_data", {})
    return render_template("apply/confirmation.html", data=data)

@bp.route("/apply/submit", methods=["GET", "POST"])
def submit_application():
    if "application_data" not in session and "reference_number" not in session:
        return redirect(url_for("main.apply_index"))

    form = EmailForm()
    if request.method == "POST":
        reference_number = session.get("reference_number", "unknown")
        if form.validate_on_submit():
            return render_template("apply/success.html", form=form, reference_number=reference_number, email_sent=True)
        else:
            return render_template("apply/success.html", form=form, reference_number=reference_number, email_sent=False)

    # Handle storage, email, DB, etc.
    # For now, just print the data to console
    data = session.get("application_data", {})
    if len(data) == 0:
        return redirect(url_for("main.apply_index"))
    reference_number = data.get("minecraft_username", "unknown") + "-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    print("Application submitted with data:", data)

    session.pop("application_data", None)
    session.pop("last_question", None)
    session["reference_number"] = reference_number
    return render_template("apply/success.html", form=form, reference_number=reference_number)

@bp.route("/apply/ineligible", methods=["GET"])
def ineligible():
    session.pop("application_data", None)
    session.pop("last_question", None)
    session.pop("reference_number", None)
    return render_template("apply/ineligible.html")