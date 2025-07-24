"""
API routes for artifact generation and management
"""

from flask import Blueprint, jsonify, request
from ..extensions import db
from ..services.ai_artifact_generator import AIArtifactGenerator
import os

artifacts_bp = Blueprint('artifacts', __name__)
ai_artifact_generator = AIArtifactGenerator()

@artifacts_bp.route('/generate', methods=['POST'])
def generate_new_artifact():
    """Generate interactive artifacts from PDF content"""
    from ..models import Artifact, PDF, ProcessingJob
    
    try:
        data = request.get_json()
        pdf_id = data.get('pdf_id')
        artifact_types = data.get('types', ['study_guide', 'quiz'])
        
        if not pdf_id:
            return jsonify({'error': 'PDF ID is required'}), 400
        
        pdf = PDF.query.get(pdf_id)
        if not pdf:
            return jsonify({'error': 'PDF not found'}), 404
        
        job = ProcessingJob(
            job_type='artifact_generation',
            status='processing',
            progress=0,
            pdf_id=pdf_id
        )
        db.session.add(job)
        db.session.commit()
        
        try:
            pdf_path = os.path.join('uploads', pdf.filename)
            result = ai_artifact_generator.process_pdf_for_artifacts(pdf_path, pdf.title)

            if result.get('error'):
                job.status = 'failed'
                job.error_message = result['error']
                db.session.commit()
                return jsonify({'error': result['error']}), 500
            
            job.progress = 50
            db.session.commit()
            
            artifacts_created = []
            
            if 'study_guide' in artifact_types and result['artifacts'].get('study_guide'):
                study_guide = Artifact(
                    title=f"{pdf.title} - Interactive Study Guide",
                    artifact_type='study_guide',
                    react_code=result['artifacts']['study_guide'],
                    json_metadata={
                        'analysis': result['analysis'],
                        'chapter_count': len(result['chapters'])
                    },
                    pdf_id=pdf_id
                )
                db.session.add(study_guide)
                artifacts_created.append({
                    'type': 'study_guide',
                    'title': study_guide.title
                })
            
            if 'quiz' in artifact_types and result['artifacts'].get('quiz'):
                quiz = Artifact(
                    title=f"{pdf.title} - Interactive Quiz",
                    artifact_type='quiz',
                    react_code=result['artifacts']['quiz'],
                    json_metadata={
                        'question_count': 5,
                        'difficulty': result['analysis'].get('complexity_level', 'intermediate')
                    },
                    pdf_id=pdf_id
                )
                db.session.add(quiz)
                artifacts_created.append({
                    'type': 'quiz',
                    'title': quiz.title
                })
            
            job.status = 'completed'
            job.progress = 100
            job.result_data = {
                'artifacts_created': artifacts_created,
                'analysis': result['analysis']
            }
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'job_id': job.id,
                'artifacts_created': artifacts_created,
                'analysis': result['analysis']
            })
            
        except Exception as e:
            job.status = 'failed'
            job.error_message = str(e)
            db.session.commit()
            raise e
            
    except Exception as e:
        return jsonify({'error': f'Artifact generation failed: {str(e)}'}), 500

@artifacts_bp.route('/pdf/<int:pdf_id>', methods=['GET'])
def get_artifacts_for_pdf(pdf_id):
    """Get all artifacts for a specific PDF"""
    from ..models import Artifact
    
    try:
        artifacts = Artifact.query.filter_by(pdf_id=pdf_id).all()
        
        artifacts_data = []
        for artifact in artifacts:
            artifacts_data.append({
                'id': artifact.id,
                'title': artifact.title,
                'type': artifact.artifact_type,
                'created_at': artifact.created_at.isoformat(),
                'json_metadata': artifact.json_metadata
            })
        
        return jsonify({
            'success': True,
            'artifacts': artifacts_data
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artifacts_bp.route('/<int:artifact_id>', methods=['GET'])
def get_artifact(artifact_id):
    """Get specific artifact with React code"""
    from ..models import Artifact
    
    try:
        artifact = Artifact.query.get(artifact_id)
        if not artifact:
            return jsonify({'error': 'Artifact not found'}), 404
        
        return jsonify({
            'success': True,
            'artifact': {
                'id': artifact.id,
                'title': artifact.title,
                'type': artifact.artifact_type,
                'content': artifact.react_code,
                'json_metadata': artifact.json_metadata,
                'created_at': artifact.created_at.isoformat(),
                'updated_at': artifact.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artifacts_bp.route('/<int:artifact_id>', methods=['DELETE'])
def delete_artifact(artifact_id):
    """Delete an artifact"""
    from ..models import Artifact
    
    try:
        artifact = Artifact.query.get(artifact_id)
        if not artifact:
            return jsonify({'error': 'Artifact not found'}), 404
        
        db.session.delete(artifact)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Artifact deleted'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artifacts_bp.route('/processing-jobs/<int:job_id>/status', methods=['GET'])
def get_job_status(job_id):
    """Get processing job status"""
    from ..models import ProcessingJob
    
    try:
        job = ProcessingJob.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'success': True,
            'job_status': {
                'id': job.id,
                'status': job.status,
                'progress': job.progress,
                'error_message': job.error_message,
                'result_data': job.result_data
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artifacts_bp.route('/debug-inspect', methods=['GET'])
def debug_inspect_artifacts():
    """Temporary debug route to inspect artifact data in the database."""
    from ..models import Artifact
    print("\n--- TRIGGERING ARTIFACT DEBUG INSPECTION ---")
    try:
        artifacts = Artifact.query.all()
        if not artifacts:
            print("DEBUG: No artifacts found in the database.")
            return jsonify({'message': 'No artifacts found.'}), 200

        for artifact in artifacts:
            code_length = len(artifact.react_code) if artifact.react_code else 0
            print(f"DEBUG - ID: {artifact.id}, Title: {artifact.title}, React Code Length: {code_length}")
            if code_length == 0:
                print(f"  -> WARNING: Artifact {artifact.id} has NO React code!")
        
        print("--- ARTIFACT DEBUG INSPECTION COMPLETE ---\n")
        return jsonify({'message': 'Debug inspection complete. Check server logs.'}), 200

    except Exception as e:
        print(f"DEBUG ERROR: An error occurred while inspecting artifacts: {e}")
        return jsonify({'error': str(e)}), 500

@artifacts_bp.route('/processing-jobs/<int:job_id>', methods=['GET'])
def get_job(job_id):
    """Get processing job"""
    try:
        from ..models import ProcessingJob
        job = ProcessingJob.query.get(job_id)
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        return jsonify({
            'success': True,
            'job': {
                'id': job.id,
                'type': job.job_type,
                'status': job.status,
                'progress': job.progress,
                'error_message': job.error_message,
                'result_data': job.result_data,
                'created_at': job.created_at.isoformat(),
                'updated_at': job.updated_at.isoformat()
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
