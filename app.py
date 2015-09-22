import datetime
from flask import Flask, render_template, jsonify
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

class DesignAdmin(ModelAdmin):
    columns = ('name', 'image_url', 'status', 'price')

api = RestAPI(app)
api.register(Design, DesignResource)
api.setup()

auth = Auth(app, db)
admin = Admin(app, auth)
admin.register(Design, DesignAdmin)

admin.setup()

@app.route("/")
def home():
  return render_template("list.html")

@app.route("/design/<int:id>/hide")
def hide(id):
  design = Design.get(Design.id == id)
  design.status = -5
  design.save()
  return "OK"

@app.route("/uncategorized")
def show_uncategorized():
  designs = Design.select().where(Design.status == 0).limit(100)

  uncategorized = []
  for design in designs:
    uncategorized.append({ "id": design.id, "image_url": design.image_url })

  return jsonify(data=uncategorized)

if __name__ == '__main__':
  
  Design.create_table(fail_silently=True)

  app.run()