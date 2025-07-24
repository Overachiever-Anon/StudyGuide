import click
from flask.cli import with_appcontext
from .extensions import db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    # Import all models here so they are registered with SQLAlchemy
    from . import models
    db.create_all()
    click.echo('Initialized the database.')

import json

@click.command('seed-db')
@with_appcontext
def seed_db_command():
    """Seeds the database with sample data."""
    from .models import User, PDF, Artifact
    from .extensions import bcrypt

    click.echo('Seeding database...')

    # Clear existing data
    db.session.query(Artifact).delete()
    db.session.query(PDF).delete()
    db.session.query(User).delete()
    db.session.commit()

    # Create sample user
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='demouser', email='demo@example.com', password_hash=hashed_password)
    db.session.add(user)
    db.session.commit()

    # Create sample PDF
    pdf = PDF(
        filename='sample_document.pdf',
        title='Introduction to Computer Science',
        content='This is a sample PDF about the basics of computer science, covering topics like algorithms, data structures, and programming paradigms.',
        user_id=user.id
    )
    db.session.add(pdf)
    db.session.commit()

    # Create sample Artifact with fallback React code
    react_code = get_fallback_study_guide_code('Introduction to Computer Science', pdf.content)
    artifact = Artifact(
        title='Interactive Study Guide for CS101',
        artifact_type='study_guide',
        react_code=react_code,
        json_metadata={'source': 'seed_data'},
        pdf_id=pdf.id
    )
    db.session.add(artifact)
    db.session.commit()

    click.echo('Database seeded with sample data.')

def get_fallback_study_guide_code(title: str, content: str) -> str:
    """Generates the fallback study guide React code."""
    component_name = ''.join(filter(str.isalnum, title.title()))
    safe_content = json.dumps(content[:500].strip() + '...')
    return f"""import React, {{ useState }} from 'react';

const CheckCircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="inline-block h-5 w-5 text-green-500"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
);

const CircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="inline-block h-5 w-5 text-gray-400"><circle cx="12" cy="12" r="10"/></svg>
);

export default function {component_name}StudyGuide() {{
  const [completedSections, setCompletedSections] = useState(new Set());
  const [currentSection, setCurrentSection] = useState('section_1');

  const sections = [
    {{
      id: 'section_1',
      title: 'Introduction',
      content: {safe_content},
      type: 'text'
    }},
    {{
      id: 'section_2', 
      title: 'Interactive Quiz',
      content: 'Test your knowledge with this interactive quiz.',
      type: 'quiz'
    }}
  ];

  const markComplete = (sectionId) => {{
    setCompletedSections(prev => new Set([...prev, sectionId]));
  }};

  const progress = (completedSections.size / sections.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20 text-gray-200 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-8">
          {title}
        </h1>
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700 mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-gray-300">Progress</span>
            <span className="text-purple-400">{{Math.round(progress)}}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all duration-500"
              style={{{{ width: `${{progress}}%` }}}}
            />
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-4">
              <h3 className="text-lg font-semibold text-white mb-4">Sections</h3>
              {{sections.map(section => (
                <button
                  key={{section.id}}
                  className={{`w-full text-left p-3 rounded-lg mb-2 flex items-center transition-colors ${{currentSection === section.id ? 'bg-purple-600/30 text-purple-300' : 'text-gray-300 hover:bg-gray-700/50'}}`}}
                  onClick={{() => setCurrentSection(section.id)}}
                >
                  {{completedSections.has(section.id) ? <CheckCircleIcon /> : <CircleIcon />}}
                  <span className="ml-2">{{section.title}}</span>
                </button>
              ))}}
            </div>
          </div>
          <div className="lg:col-span-3">
            {{sections.map(section => (
              <div key={{section.id}} className={{currentSection === section.id ? 'block' : 'hidden'}}>
                <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-white">{{section.title}}</h2>
                    {{!completedSections.has(section.id) && (
                      <button
                        className="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
                        onClick={{() => markComplete(section.id)}}
                      >
                        Mark as Completed
                      </button>
                    ) }}
                  </div>
                  <div className="prose prose-invert max-w-none text-gray-300 leading-relaxed">
                    <p>{{section.content}}</p>
                  </div>
                </div>
              </div>
            ))}}
          </div>
        </div>
      </div>
    </div>
  );
}}
"""

def register_cli_commands(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
