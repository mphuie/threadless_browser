import datetime
from flask import Flask, render_template, jsonify
from flask_peewee.auth import Auth
from flask_peewee.db import Database
from flask_peewee.admin import Admin, ModelAdmin
from flask_peewee.rest import RestAPI, RestResource
from peewee import *

DATABASE = {
    'name': 'threadless.db',
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

class Product(db.Model):
  name = TextField()
  size = TextField()
  in_stock = BooleanField(null=True)
  price = FloatField(default=0.0)
  design = ForeignKeyField(Design, related_name='products', null=True)

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

@app.route('/myfilter')
def myfilter():
  designs_query = Design.raw("select * from design where id in (SELECT distinct(design_id) FROM  product where size = 'L' and name like '%Men%' and price < 30 limit 30)")
  designs = [{ 'name': d.name, 'id': d.id, 'design_id': d.design_id } for d in designs_query]
  return render_template("myfilter.html", designs=designs)

@app.route('/api/myfilter')
def myfilter_api():
  designs_query = Design.raw("select * from design where id in (SELECT distinct(design_id) FROM  product where size = 'L' and name like '%Men%' and price < 50 ) and status = 0")
  designs = [{ 'name': d.name, 'id': d.id, 'design_id': d.design_id, 'image_url': d.image_url } for d in designs_query]
  return jsonify(designs=designs)

@app.route('/api/keeps')
def keeps_api():
  print 'hi!'
  designs_query = Design.select().where(Design.status > 0)
  designs = [{ 'name': d.name, 'id': d.id, 'design_id': d.design_id, 'image_url': d.image_url } for d in designs_query]
  return jsonify(designs=designs)

@app.route('/keeps')
def mykeeps():
  return render_template("keeps.html")


@app.route('/api/design/<int:id>')
def design_detail(id):
  pass

@app.route("/design/<int:id>/hide")
def hide(id):
  design = Design.get(Design.id == id)
  design.status = -5
  design.save()
  return "OK"

@app.route("/design/<int:id>/keep")
def keep(id):
  design = Design.get(Design.id == id)
  design.status = 5
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
