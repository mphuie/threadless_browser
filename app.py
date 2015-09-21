import datetime
from flask import Flask, render_template
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin, ModelAdmin
from flask_peewee.rest import RestAPI, RestResource
from peewee import *

DATABASE = {
    'name': 'example.db',
    'engine': 'peewee.SqliteDatabase',
}
DEBUG = True
SECRET_KEY = 'ssshhhh'

app = Flask(__name__)
app.config.from_object(__name__)

db = Database(app)

class Design(db.Model):
  design_id = IntegerField()
  name = TextField()
  image_url = TextField()
  status = IntegerField(default=0)
  price = FloatField(default=0.0)

class DesignResource(RestResource):
    paginate_by = 100

api = RestAPI(app)
api.register(Design, DesignResource)
api.setup()

@app.route("/")
def home():
  return render_template("list.html")

@app.route("/design/<int:id>/hide")
def hide(id):
  design = Design.get(Design.id == id)
  design.status = -5
  design.save()
  return "OK"

if __name__ == '__main__':
  
  Design.create_table(fail_silently=True)

  app.run()