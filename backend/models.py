from .extensions import db
import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

class PDF(db.Model):
    __tablename__ = 'pdfs'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    storage_path = db.Column(db.String(500), nullable=True)  # Path to the file in Supabase storage
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('pdfs', lazy=True))
    chapters = db.relationship('Chapter', backref='pdf', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<PDF {self.filename}>'

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdfs.id'), nullable=False)

    def __repr__(self):
        return f'<Chapter {self.title}>'

class Exam(db.Model):
    __tablename__ = 'exams'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdfs.id'), nullable=False)
    pdf = db.relationship('PDF', backref=db.backref('exams', lazy=True, cascade="all, delete-orphan"))
    questions = db.relationship('Question', backref='exam', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Exam {self.title}>'

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.Text, nullable=False)
    options = db.Column(db.JSON, nullable=False)  # e.g., ['Option A', 'Option B', 'Option C']
    correct_answer = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text)  # Detailed explanation for the answer
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.id'), nullable=False)

    def __repr__(self):
        return f'<Question {self.id}>'

class Artifact(db.Model):
    """Interactive study guides, visualizations, and learning components"""
    __tablename__ = 'artifacts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    artifact_type = db.Column(db.String(50), nullable=False)  # 'study_guide', 'quiz', 'visualization'
    react_code = db.Column(db.Text, nullable=False)  # Generated React component code
    json_metadata = db.Column(db.JSON)  # Additional configuration and data
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdfs.id'), nullable=False)
    pdf = db.relationship('PDF', backref=db.backref('artifacts', lazy=True, cascade="all, delete-orphan"))
    
    def __repr__(self):
        return f'<Artifact {self.title}>'

class ProcessingJob(db.Model):
    """Track PDF processing and artifact generation jobs"""
    __tablename__ = 'processing_jobs'
    id = db.Column(db.Integer, primary_key=True)
    job_type = db.Column(db.String(50), nullable=False)  # 'pdf_processing', 'artifact_generation'
    status = db.Column(db.String(20), nullable=False, default='pending')  # 'pending', 'processing', 'completed', 'failed'
    progress = db.Column(db.Integer, default=0)  # 0-100
    error_message = db.Column(db.Text)
    result_data = db.Column(db.JSON)  # Store processing results
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    pdf_id = db.Column(db.Integer, db.ForeignKey('pdfs.id'), nullable=False)
    pdf = db.relationship('PDF', backref=db.backref('processing_jobs', lazy=True, cascade="all, delete-orphan"))
    
    def __repr__(self):
        return f'<ProcessingJob {self.job_type} - {self.status}>'