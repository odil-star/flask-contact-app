from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Модель контакта
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=True)


# Создание таблицы, если её ещё нет
with app.app_context():
    db.create_all()


# Главная страница
@app.route("/")
def home():
    return render_template("index.html")


# О нас
@app.route("/about")
def about():
    return render_template("about.html")


# Добавить контакт
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        description = request.form.get("description")

        if name and phone:
            new_contact = Contact(name=name, phone=phone, description=description)
            db.session.add(new_contact)
            db.session.commit()
            return redirect("/contacts")

    return render_template("contact.html")



# Показать все контакты
@app.route("/contacts")
def contacts():
    all_contacts = Contact.query.all()
    return render_template("contacts.html", contacts=all_contacts)


# Редактировать контакт
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)

    if request.method == "POST":
        contact.name = request.form["name"]
        contact.phone = request.form["phone"]
        contact.description = request.form["description"]
        db.session.commit()
        return redirect("/contacts")

    return render_template("edit.html", contact=contact)


# Удалить контакт
@app.route("/delete/<int:id>")
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return redirect("/contacts")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
