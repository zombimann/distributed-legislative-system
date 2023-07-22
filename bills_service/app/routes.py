# app/routes.py
from flask import request, jsonify, make_response
from app import app, db
from app.models import Bill
from app.utils import validate_jwt

# Create a new bill
@app.route('/api/bills', methods=['POST'])
@validate_jwt
def create_bill():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')
    author_id = data.get('author_id')

    if not title or not description or not author_id:
        return jsonify({'message': 'Title, description, and author_id are required.'}), 400

    bill = Bill(title=title, description=description, tags=tags, author_id=author_id)
    db.session.add(bill)
    db.session.commit()

    return jsonify({'message': 'Bill created successfully.', 'bill_id': bill.id}), 201

# Get a list of all bills
@app.route('/api/bills', methods=['GET'])
def get_all_bills():
    bills = Bill.query.all()
    return jsonify([{'id': bill.id, 'title': bill.title, 'description': bill.description,
                     'tags': bill.tags, 'author_id': bill.author_id} for bill in bills]), 200

# Get details of a specific bill
@app.route('/api/bills/<int:bill_id>', methods=['GET'])
def get_bill_details(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return jsonify({'message': 'Bill not found.'}), 404

    return jsonify({'id': bill.id, 'title': bill.title, 'description': bill.description,
                    'tags': bill.tags, 'author_id': bill.author_id}), 200

# Edit an existing bill
@app.route('/api/bills/<int:bill_id>/edit', methods=['PUT'])
@validate_jwt
def edit_bill(bill_id):
    bill = Bill.query.get(bill_id)
    if not bill:
        return jsonify({'message': 'Bill not found.'}), 404

    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    tags = data.get('tags')

    if title:
        bill.title = title
    if description:
        bill.description = description
    if tags:
        bill.tags = tags

    db.session.commit()

    return jsonify({'message': 'Bill updated successfully.'}), 200
