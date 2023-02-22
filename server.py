from flask import Flask, render_template, redirect, url_for
from forms import TeamForm, ProjectForm
from model import User, Team, Project, connect_to_db, db

app = Flask(__name__)

app.secret_key = "keep this secret"

user_id = 1

@app.route("/")
def home():
    team_form = TeamForm()
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)
    return render_template("home.html", team_form = team_form, project_form = project_form)

@app.route("/add-team", methods=["POST"])
def add_team():
    team_form = TeamForm()
    if team_form.validate_on_submit():
        with app.app_context():
            team_name = team_form.team_name.data
            new_team = Team(team_name, user_id)
            db.session.add(new_team)
            db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/add_project", methods=["POST"])
def add_project():
    project_form = ProjectForm()
    project_form.update_teams(User.query.get(user_id).teams)

    if project_form.validate_on_submit():
        with app.app_context():
            project_name = project_form.project_name.data
            description = project_form.description.data
            completed = project_form.completed.data
            team_assigned = project_form.team_assigned.data
            new_project = Project(project_name, description, completed, team_assigned)
            db.session.add(new_project)
            db.session.commit()
        return redirect(url_for("home"))
    else:
        return redirect(url_for("home"))

@app.route("/teams", methods=["GET"])
def view_teams():
    teams = Team.query.all()
    projects = Project.query.all()
    return render_template("teams.html", teams=teams, projects=projects)

@app.route("/projects", methods=["GET"])
def view_projects():
    projects = Project.query.all()
    return render_template("projects.html", projects=projects)

@app.route("/delete_project/<project_id>")
def delete_project(project_id):
    with app.app_context():
        project_to_delete = Project.query.filter_by(id = project_id).first()
        print(project_to_delete)
        db.session.delete(project_to_delete)
        db.session.commit()
        return redirect(url_for("view_projects"))

@app.route("/update_completed/<project_id>")
def update_completed(project_id):
    with app.app_context():
        project_to_update = Project.query.filter_by(id = project_id).first()
        if project_to_update.completed:
            project_to_update.completed = False
        else:
            project_to_update.completed = True
        db.session.add(project_to_update)
        db.session.commit()
        return redirect(url_for("view_projects"))


if __name__ == "__main__":
    connect_to_db(app)
    app.run(debug = True)
