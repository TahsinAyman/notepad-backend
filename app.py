from multiprocessing import reduction
import re
from flask import *
from models import *
from Service import *


@app.route("/", methods=["GET"])
def index():
  return jsonify({"result": True, "message": "Backend API notepad"})

@app.route("/register/", methods=["POST"])
def register():
  try:
    data = request.get_json(force=True)
    user = data.get("user")
    password = data.get("password")
    auth = Authentication(user=user, password=password)
    db.session.add(auth)
    db.session.commit()
    return jsonify({"result": True, "message": "Registered"})
  except Exception:
    return jsonify({"result": False, "message": "Couldn't Register"})


@app.route("/login/", methods=["POST"])
def login():
  try:
    data = request.get_json(force=True)
    user = data.get("user")
    password = data.get("password")
    
    if Authentication.query.filter_by(user=user, password=password).first():
      return jsonify({"result": True, "message": "Logged In"})
    else:
      raise Exception
  except Exception:
    return jsonify({"result": False, "message": "Couldn't Login"})

@app.route("/notes/add/", methods=["POST"])
def add_notes():
  try:
    data = request.get_json(force=True)
    id = data.get("id")
    user = data.get("user")
    title = data.get("title")
    note = data.get("note")

    if not Authentication.query.filter_by(user=user).first():
      raise Exception

    notes = Notes(id=id, user=user, title=title, note=note)
    db.session.add(notes)
    db.session.commit()

    return jsonify({"result": True, "message": "Successfully Added Notes"})
  except Exception:
    return jsonify({"result": False, "message": "Couldn't Add"})

@app.route("/notes/<user>/", methods=["GET"])
def query_notes(user):
  try:
    notes = [json.loads(i.__str__()) for i in Notes.query.filter_by(user=user).all()]
    return jsonify(notes)
  except Exception:
    return jsonify([])

@app.route("/notes/<id>", methods=["DELETE"])
def delete_notes(id):
  try:
    notes = Notes.query.filter_by(id=id).first()
    db.session.delete(notes)
    db.session.commit()
    return jsonify({"result": True, "message": "Successfully Deleted"})
  except Exception:
    return jsonify({"result": False, "message": "Couldn't Delete"})

@app.route("/notes/<id>", methods=["PUT"])
def update_notes(id):
  try:
    data = request.get_json(force=True)
    notes = Notes.query.filter_by(id=id).first()


    if data.get("title"):
      notes.title = data.get("title")

    if data.get('note'):
      notes.note = data.get("note")

    db.session.commit()
    return jsonify({"result": True, "message": "Successfully Updated"})
  except Exception:
    return jsonify({"result": False, "message": "Couldn't Update"})


@app.route("/note/query/<user>/<title>", methods=['GET'])
def note_query_title(user, title):
	try:
		data = request.get_json(force=True)
		notes = [json.loads(i.__str__()) for i in Notes.query.filter_by(user=user, title=title).all()]
		return jsonify(notes)
	except Exception:
		return jsonify([])
		

if __name__ == "__main__":
  app.run(debug=True, host="localhost", port=8000)
