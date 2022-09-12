from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask("app")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)
CORS(app)

class Authentication(db.Model):
  __tablename__ = "auth"
  user = db.Column(db.String(50), primary_key=True, nullable=False)
  password = db.Column(db.String(100), nullable=False)

  def __str__(self):
    return json.dumps(obj={"user": self.user, "password": self.password}, indent=4)


class Notes(db.Model):
  __tablename__ = "notes"
  id = db.Column(db.Integer, primary_key=True)
  user = db.Column(db.String(50), nullable=False)
  title = db.Column(db.String(1000))
  note = db.Column(db.String(1000000000000000), nullable=False)

  def __str__(self):
    return json.dumps(obj={"id": self.id, "user": self.user, "title": self.title, "note": self.note}, indent=4)

if __name__ == "__main__":
  db.create_all()
  