from flask import Blueprint, request, jsonify
from ..models import db, Lecture
from ..utils.decorators import login_required
import os
from ..extensions import supabase
from werkzeug.utils import secure_filename
import time
from supabase.lib.client_options import ClientOptions

bp = Blueprint('upload', __name__, url_prefix='/api/upload')

@bp.route('', methods=['POST'])
@login_required
def upload_file(current_user):
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        try:
            filename = secure_filename(file.filename)
            # Create a unique path for the file to prevent overwrites
            file_path_in_bucket = f"{current_user.id}/{int(time.time())}-{filename}"
            
            bucket_name = os.environ.get("SUPABASE_BUCKET_NAME")
            if not bucket_name:
                 return jsonify({'error': 'Supabase bucket name not configured'}), 500

            # --- UPDATED SECTION ---
            # Check if the bucket exists. If not, create it.
            # The new way to make a bucket public is with FileOptions.
            try:
                supabase.storage.get_bucket(bucket_name)
            except Exception:
                # If get_bucket fails, it likely doesn't exist. Let's create it.
                supabase.storage.create_bucket(
                    name=bucket_name,
                    options=ClientOptions(public=True) # Correct way to make a bucket public
                )
            # --- END UPDATED SECTION ---

            # Upload to Supabase Storage
            file_content = file.read()
            file.seek(0) # Reset file pointer after reading

            supabase.storage.from_(bucket_name).upload(
                path=file_path_in_bucket,
                file=file_content,
                file_options={"content-type": "application/pdf"}
            )

            # Create a new lecture record in the database
            new_lecture = Lecture(
                user_id=current_user.id,
                title=filename,
                file_path=file_path_in_bucket
            )
            db.session.add(new_lecture)
            db.session.commit()

            return jsonify({
                'id': new_lecture.id,
                'title': new_lecture.title,
                'file_path': new_lecture.file_path
            }), 201

        except Exception as e:
            return jsonify({'error': f'An error occurred: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type, only PDF is allowed'}), 400
