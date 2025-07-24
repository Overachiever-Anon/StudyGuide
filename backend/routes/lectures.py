from flask import Blueprint, jsonify
from ..utils.decorators import jwt_required
import datetime

lectures_bp = Blueprint('lectures_bp', __name__, url_prefix='/api')

# Dummy data
dummy_lectures_data = [
    {
        'id': 1,
        'title': 'Introduction to Quantum Computing',
        'filename': 'quantum_computing_intro.pdf',
        'created_at': datetime.datetime.utcnow().isoformat() + 'Z',
        'size': '2.5 MB',
        'status': 'completed'
    },
    {
        'id': 2,
        'title': 'Advanced Neural Networks',
        'filename': 'ann_deep_dive.pdf',
        'created_at': (datetime.datetime.utcnow() - datetime.timedelta(days=1)).isoformat() + 'Z',
        'size': '5.1 MB',
        'status': 'completed'
    },
    {
        'id': 3,
        'title': 'The Art of Prompt Engineering',
        'filename': 'prompt_engineering_guide.pdf',
        'created_at': (datetime.datetime.utcnow() - datetime.timedelta(days=2)).isoformat() + 'Z',
        'size': '1.8 MB',
        'status': 'processing'
    }
]

dummy_chapters_data = {
    1: [
        {'id': 1, 'title': 'Chapter 1: The Qubit', 'content': 'Content for the first chapter about qubits.'},
        {'id': 2, 'title': 'Chapter 2: Superposition and Entanglement', 'content': 'Content for the second chapter about quantum phenomena.'}
    ],
    2: [
        {'id': 3, 'title': 'Chapter 1: Perceptrons', 'content': 'Content for the chapter on perceptrons.'},
        {'id': 4, 'title': 'Chapter 2: Convolutional Neural Networks', 'content': 'Content for the chapter on CNNs.'}
    ]
}

@lectures_bp.route('/lectures', methods=['GET'])
@jwt_required
def get_lectures(current_user):
    # This route now returns a hardcoded list of lectures for frontend development.
    # The database query has been bypassed.
    return jsonify(dummy_lectures_data), 200

@lectures_bp.route('/lectures/<int:pdf_id>', methods=['GET'])
@jwt_required
def get_lecture(current_user, pdf_id):
    lecture = next((lec for lec in dummy_lectures_data if lec['id'] == pdf_id), None)
    if lecture:
        return jsonify(lecture), 200
    return jsonify({'message': 'Lecture not found'}), 404

@lectures_bp.route('/lectures/<int:pdf_id>/chapters', methods=['GET'])
@jwt_required
def get_chapters(current_user, pdf_id):
    chapters = dummy_chapters_data.get(pdf_id)
    if chapters:
        return jsonify(chapters), 200
    # Return empty list if no chapters are defined for this lecture ID
    return jsonify([]), 200
