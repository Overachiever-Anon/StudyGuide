from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import fitz  # PyMuPDF

from ..extensions import db
from ..utils.decorators import jwt_required
from ..utils.chapter_splitter import split_into_chapters

# Define the blueprint
upload_bp = Blueprint('upload_bp', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
@jwt_required
def upload_file(current_user):
    from ..models import PDF, Chapter  # Defer import
    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part in the request'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        try:
            # Read file stream into memory
            file_stream = file.read()
            
            # Open PDF with PyMuPDF from memory
            pdf_document = fitz.open(stream=file_stream, filetype="pdf")
            
            # Extract text from all pages
            content = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                content += page.get_text()
            
            pdf_document.close()
            
            # Create a new PDF record in the database
            new_pdf = PDF(
                filename=filename,
                title=filename.rsplit('.', 1)[0],  # Use filename without extension as title
                content=content,
                user_id=current_user.id
            )
            
            db.session.add(new_pdf)
            db.session.flush()  # Flush to get the new_pdf.id before committing

            # Split content into chapters and save them
            chapters = split_into_chapters(content)
            for chapter_title, chapter_content in chapters:
                new_chapter = Chapter(
                    title=chapter_title,
                    content=chapter_content,
                    pdf_id=new_pdf.id
                )
                db.session.add(new_chapter)
            
            db.session.commit()
            
            return jsonify({'message': 'File uploaded and processed successfully', 'pdf_id': new_pdf.id}), 201

        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500
    else:
        return jsonify({'message': 'File type not allowed'}), 400
