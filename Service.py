from models import *
import json

def registerService(user, password):
  try:
    auth = Authentication(user=user, password=password)
    db.session.add(auth)
    db.session.commit()
    return {"result": True, "message": "Successfully Registered"}
  except Exception:
    return {"result": False, "message": "Couldn't Register"}