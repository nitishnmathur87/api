from flask import Flask, request, jsonify

#import the main Flask, request, jsonify, SQLAlchemy classes. the request class lets us distinguish between the HTTP verbs.

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

#next is to make a variable name app containing a usuable instance of the Flask class and a variable db containing a usuable instance of the SQLAlchemy class

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/ufosightings'

#connect the flask app to the MySQL database.

class Sighting(db.Model):
  __tablename__ = 'sightings'
  id = db.Column(db.Integer, primary_key = True)
  sighted_at = db.Column(db.Integer)
  reported_at = db.Column(db.Integer)
  location = db.Column(db.String(100))
  shape = db.Column(db.String(10))
  duration = db.Column(db.String(10))
  description = db.Column(db.Text)
  lat = db.Column(db.Float(6))
  lng = db.Column(db.Float(6))

#create a model representing the table in the database so that a query can be done from the flask app

@app.route('/sightings/', methods=['GET'])
def sightings():
	if request.method == 'GET':
		lim = request.args.get('limit', 10)
		off = request.args.get('offset', 0)

		radius = request.args.get('radius', 10)
		location = request.args.get('location', ',')
		lat, lng = location.split(',')
		if lat and lng and radius:
			query = "SELECT id,  location, ( 3959 * acos( cos( radians( %(latitude)s ) ) * cos( radians( lat ) ) * cos( radians( lng ) - radians( %(longitude)s ) ) + sin( radians( %(latitude)s ) ) * sin( radians( lat ) ) ) ) AS distance FROM sightings HAVING distance < %(radius)s ORDER BY distance LIMIT %(limit)s" % {"latitude": lat, "longitude": lng, "radius": radius, "limit": lim}
			results = Sighting.query.from_statement(query).all()
		else:
			results = Sighting.query.limit(lim).offset(off).all()
# same as SQL query of SELECT * from sightings LIMIT 10 OFFSET 0;
		json_results = []
		for result in results:
			d = {'sighted_at': result.sighted_at,
			     'reported_at': result.reported_at,
			     'location': result.location,
           		     'shape': result.shape,
           		     'duration': result.duration,
           		     'description': result.description,
           		     'lat': result.lat,
           		     'lng': result.lng}
			json_results.append(d)
		return jsonify(items=json_results)


@app.route('/sightings/<int:sighting_id>', methods=['GET'])
def sighting(sighting_id):
  if request.method == 'GET':
    result = Sighting.query.filter_by(id=sighting_id).first()

#For example, Sighting.query.filter_by(id=1).first() would be equivalent to the SQL statement SELECT * from sightings WHERE id=1;

    json_result = {'sighted_at': result.sighted_at,
                   'reported_at': result.reported_at,
                   'location': result.location,
                   'shape': result.shape,
                   'duration': result.duration,
                   'description': result.description,
                   'lat': result.lat,
                   'lng': result.lng}

    return jsonify(items=json_result)
#set up the URLs for the API

if __name__ == '__main__':
	app.run(debug=True)

# use the function app.run() to run it on the localserver. Debug flag  is set to true so that the error messages can be seen.
