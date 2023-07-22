#app/routes.py

from flask import jsonify, request
from app import app, db
from app.models import CommitteeMember

committee_routes = app

# API for nominating a candidate for the committee
@committee_routes.route('/api/committee/nominate', methods=['POST'])
def nominate_candidate():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'Please provide a valid name.'}), 400

    # Check if the candidate is already nominated
    existing_candidate = CommitteeMember.query.filter_by(name=name).first()
    if existing_candidate:
        return jsonify({'error': 'Candidate is already nominated.'}), 400

    # Create a new committee member
    new_candidate = CommitteeMember(name=name, nomination_status=True)
    db.session.add(new_candidate)
    db.session.commit()

    return jsonify({'message': 'Candidate nominated successfully.'}), 201

# API for getting the list of current committee members
@committee_routes.route('/api/committee/members', methods=['GET'])
def get_committee_members():
    members = CommitteeMember.query.filter_by(elected_status=True).all()
    member_list = [{'id': member.id, 'name': member.name} for member in members]
    return jsonify(member_list)
