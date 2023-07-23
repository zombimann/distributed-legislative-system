# app/routes.py

from flask import Blueprint, jsonify, request
from app import db
from app.models import Bill, Vote

voting_bp = Blueprint('voting_bp', __name__)

# Route for creating a new bill
@voting_bp.route('/api/bills', methods=['POST'])
def create_bill():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    author = data.get('author')
    tags = data.get('tags')

    if not title or not description or not author:
        return jsonify({'message': 'Title, description, and author are required'}), 400

    bill = Bill(title=title, description=description, author=author, tags=tags)
    db.session.add(bill)
    db.session.commit()

    return jsonify({'message': 'Bill created successfully'}), 201

# Route for editing an existing bill
@voting_bp.route('/api/bills/<int:id>', methods=['PUT'])
def edit_bill(id):
    bill = Bill.query.get(id)
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')

    if not title or not description:
        return jsonify({'message': 'Title and description are required'}), 400

    bill.title = title
    bill.description = description
    bill.tags = tags
    db.session.commit()

    return jsonify({'message': 'Bill updated successfully'}), 200

# Route for voting on a bill
@voting_bp.route('/api/bills/<int:id>/vote', methods=['POST'])
def vote_on_bill(id):
    bill = Bill.query.get(id)
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404

    data = request.get_json()
    user_id = data.get('user_id')
    vote = data.get('vote')

    if vote is None:
        return jsonify({'message': 'Vote value is required'}), 400

    # Perform validation checks if needed (e.g., user_id validity)

    vote_entry = Vote.query.filter_by(user_id=user_id, bill_id=id).first()
    if vote_entry:
        return jsonify({'message': 'User already voted on this bill'}), 400

    vote_entry = Vote(user_id=user_id, bill_id=id, vote=vote)
    db.session.add(vote_entry)
    db.session.commit()

    return jsonify({'message': 'Vote recorded successfully'}), 201

# Route for getting all bills
@voting_bp.route('/api/bills', methods=['GET'])
def get_bills():
    bills = Bill.query.all()
    bill_list = []
    for bill in bills:
        bill_list.append({
            'id': bill.id,
            'title': bill.title,
            'description': bill.description,
            'author': bill.author,
            'tags': bill.tags
        })
    return jsonify(bill_list), 200

# Route for getting details of a specific bill
@voting_bp.route('/api/bills/<int:id>', methods=['GET'])
def get_bill_details(id):
    bill = Bill.query.get(id)
    if not bill:
        return jsonify({'message': 'Bill not found'}), 404
    return jsonify({
        'id': bill.id,
        'title': bill.title,
        'description': bill.description,
        'author': bill.author,
        'tags': bill.tags
    }), 200

# Other route handlers for retrieving committee information, voting results, etc. go here
