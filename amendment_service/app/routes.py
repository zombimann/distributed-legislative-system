# app/routes.py

from flask_restful import Resource, reqparse, abort
from app import db
from app.models import Amendment

class AmendmentListResource(Resource):
    def get(self):
        amendments = Amendment.query.all()
        return [{"id": a.id, "title": a.title, "description": a.description, "proposed_by": a.proposed_by} for a in amendments]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True, help="Title is required.")
        parser.add_argument("description", type=str, required=True, help="Description is required.")
        parser.add_argument("proposed_by", type=str, required=True, help="Proposed by is required.")
        args = parser.parse_args()

        amendment = Amendment(title=args["title"], description=args["description"], proposed_by=args["proposed_by"])
        db.session.add(amendment)
        db.session.commit()

        return {"message": "Amendment created successfully.", "id": amendment.id}, 201

class AmendmentResource(Resource):
    def get(self, amendment_id):
        amendment = Amendment.query.get(amendment_id)
        if amendment:
            return {"id": amendment.id, "title": amendment.title, "description": amendment.description, "proposed_by": amendment.proposed_by}
        else:
            return {"message": "Amendment not found."}, 404

    def put(self, amendment_id):
        parser = reqparse.RequestParser()
        parser.add_argument("title", type=str, required=True, help="Title is required.")
        parser.add_argument("description", type=str, required=True, help="Description is required.")
        args = parser.parse_args()

        amendment = Amendment.query.get(amendment_id)
        if amendment:
            amendment.title = args["title"]
            amendment.description = args["description"]
            db.session.commit()
            return {"message": "Amendment updated successfully."}
        else:
            return {"message": "Amendment not found."}, 404

    def delete(self, amendment_id):
        amendment = Amendment.query.get(amendment_id)
        if amendment:
            db.session.delete(amendment)
            db.session.commit()
            return {"message": "Amendment deleted successfully."}, 200
        else:
            return {"message": "Amendment not found."}, 404
