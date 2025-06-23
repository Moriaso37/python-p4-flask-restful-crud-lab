#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

class Plants(Resource):
    def get(self):
        # Return list of all plants
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json() or {}
        # Validate required fields
        if not all(field in data for field in ("name", "image", "price")):
            return make_response({"error": "Missing required fields"}, 400)

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )
        db.session.add(new_plant)
        db.session.commit()
        return make_response(new_plant.to_dict(), 201)

api.add_resource(Plants, '/plants')


class PlantByID(Resource):
    def get(self, id):
        plant = Plant.query.get_or_404(id, description="Plant not found")
        return make_response(plant.to_dict(), 200)

    def patch(self, id):
        plant = Plant.query.get_or_404(id, description="Plant not found")
        data = request.get_json() or {}

        # Allow partial updates
        for field in ["name", "image", "price"]:
            if field in data:
                setattr(plant, field, data[field])

        db.session.commit()
        return make_response(plant.to_dict(), 200)

    def delete(self, id):
        plant = Plant.query.get_or_404(id, description="Plant not found")
        db.session.delete(plant)
        db.session.commit()
        return make_response({"message": f"Plant id={id} deleted successfully"}, 200)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
