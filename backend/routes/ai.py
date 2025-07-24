from flask import Blueprint, request, jsonify
from ..utils.decorators import jwt_required
from ..utils.question_generator import generate_questions_from_text

ai_bp = Blueprint('ai_bp', __name__, url_prefix='/api')

@ai_bp.route('/chapters/<int:chapter_id>/generate-questions', methods=['POST'])
@jwt_required
def generate_questions_route(current_user, chapter_id):
    from ..models import Chapter, Exam
    data = request.get_json()
    exam_id = data.get('exam_id')

    if not exam_id:
        return jsonify({'message': 'Exam ID is required.'}), 400

    # Authorization check: Ensure the user owns the content
    chapter = Chapter.query.get(chapter_id)
    if not chapter or chapter.pdf.user_id != current_user.id:
        return jsonify({'message': 'Chapter not found or access denied'}), 404
    
    exam = Exam.query.get(exam_id)
    if not exam or exam.pdf.user_id != current_user.id:
        return jsonify({'message': 'Exam not found or access denied'}), 404

    try:
        num_generated = generate_questions_from_text(chapter_id, exam_id)
        if num_generated > 0:
            return jsonify({'message': f'{num_generated} questions generated successfully.'}), 201
        else:
            return jsonify({'message': 'Failed to generate questions. Please check the logs.'}), 500
    except Exception as e:
        # Log the error properly in a real application
        print(f"Error in question generation route: {e}")
        return jsonify({'message': 'An internal error occurred.'}), 500
