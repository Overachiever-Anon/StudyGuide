from flask import Blueprint, jsonify, request
from ..extensions import db
from ..utils.decorators import jwt_required

exams_bp = Blueprint('exams_bp', __name__, url_prefix='/api')

@exams_bp.route('/lectures/<int:pdf_id>/exams', methods=['POST'])
@jwt_required
def create_exam(current_user, pdf_id):
    from ..models import PDF, Exam
    data = request.get_json()
    title = data.get('title')

    if not title:
        return jsonify({'message': 'Exam title is required'}), 400

    pdf = PDF.query.filter_by(id=pdf_id, user_id=current_user.id).first()
    if not pdf:
        return jsonify({'message': 'Lecture not found or access denied'}), 404

    new_exam = Exam(title=title, pdf_id=pdf.id)
    db.session.add(new_exam)
    db.session.commit()

    return jsonify({
        'message': 'Exam created successfully',
        'exam': {
            'id': new_exam.id,
            'title': new_exam.title,
            'created_at': new_exam.created_at
        }
    }), 201

@exams_bp.route('/lectures/<int:pdf_id>/exams', methods=['GET'])
@jwt_required
def get_exams(current_user, pdf_id):
    from ..models import PDF, Exam
    pdf = PDF.query.filter_by(id=pdf_id, user_id=current_user.id).first()
    if not pdf:
        return jsonify({'message': 'Lecture not found or access denied'}), 404

    exams = Exam.query.filter_by(pdf_id=pdf.id).order_by(Exam.created_at.desc()).all()
    
    exams_data = [
        {
            'id': exam.id,
            'title': exam.title,
            'created_at': exam.created_at
        }
        for exam in exams
    ]

    return jsonify(exams_data), 200

@exams_bp.route('/exams/<int:exam_id>', methods=['GET'])
@jwt_required
def get_exam_details(current_user, exam_id):
    from ..models import Exam
    exam = Exam.query.get(exam_id)
    if not exam or exam.pdf.user_id != current_user.id:
        return jsonify({'message': 'Exam not found or access denied'}), 404

    exam_data = {
        'id': exam.id,
        'title': exam.title,
        'created_at': exam.created_at.isoformat(),
        'pdf_id': exam.pdf_id
    }

    return jsonify(exam_data), 200

@exams_bp.route('/exams/<int:exam_id>/questions', methods=['POST'])
@jwt_required
def add_question_to_exam(current_user, exam_id):
    data = request.get_json()
    question_text = data.get('question_text')
    options = data.get('options')
    correct_answer = data.get('correct_answer')

    if not all([question_text, options, correct_answer]):
        return jsonify({'message': 'Missing data for question'}), 400

    exam = Exam.query.get(exam_id)
    if not exam or exam.pdf.user_id != current_user.id:
        return jsonify({'message': 'Exam not found or access denied'}), 404

    new_question = Question(
        question_text=question_text,
        options=options,
        correct_answer=correct_answer,
        exam_id=exam.id
    )
    db.session.add(new_question)
    db.session.commit()

    return jsonify({
        'message': 'Question added successfully',
        'question': {
            'id': new_question.id,
            'question_text': new_question.question_text
        }
    }), 201

@exams_bp.route('/exams/<int:exam_id>/questions', methods=['GET'])
@jwt_required
def get_exam_questions(current_user, exam_id):
    exam = Exam.query.get(exam_id)
    if not exam or exam.pdf.user_id != current_user.id:
        return jsonify({'message': 'Exam not found or access denied'}), 404

    questions = Question.query.filter_by(exam_id=exam.id).all()
    
    questions_data = [
        {
            'id': q.id,
            'question_text': q.question_text,
            'options': q.options,
            'correct_answer': q.correct_answer
        }
        for q in questions
    ]

    return jsonify(questions_data), 200
