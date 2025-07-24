#!/usr/bin/env python3
"""
Quick demo server to showcase the AI-powered artifact generation system
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Demo artifact React code - this is what the AI would generate
DEMO_STUDY_GUIDE = '''
const { useState } = React;
// Use lucide icons from CDN
const CheckCircle = (props) => React.createElement('svg', { className: props.className || 'w-4 h-4', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '2' }, React.createElement('path', { d: 'm9 12 2 2 4-4' }), React.createElement('circle', { cx: '12', cy: '12', r: '10' }));
const Circle = (props) => React.createElement('svg', { className: props.className || 'w-4 h-4', viewBox: '0 0 24 24', fill: 'none', stroke: 'currentColor', strokeWidth: '2' }, React.createElement('circle', { cx: '12', cy: '12', r: '10' }));

const BooleanLogicStudyGuide = () => {
  const [completedSections, setCompletedSections] = useState(new Set());
  const [currentSection, setCurrentSection] = useState('section_1');

  const sections = [
    {
      id: 'section_1',
      title: '1.1 Boolean Basics',
      content: 'Boolean logic deals with true and false values. These are the fundamental building blocks of digital logic and computer science.',
      type: 'text'
    },
    {
      id: 'section_2',
      title: '1.2 Truth Tables',
      content: 'Truth tables show all possible combinations of inputs and their corresponding outputs.',
      type: 'truth_table'
    },
    {
      id: 'section_3',
      title: '1.3 Interactive Quiz',
      content: 'Test your knowledge with this interactive quiz.',
      type: 'quiz'
    }
  ];

  const markComplete = (sectionId) => {
    setCompletedSections(prev => new Set([...prev, sectionId]));
  };

  const progress = (completedSections.size / sections.length) * 100;

  const TruthTable = () => (
    <div className="overflow-x-auto mt-4">
      <table className="w-full border-collapse border border-gray-600">
        <thead>
          <tr className="bg-gradient-to-r from-purple-900/50 to-blue-900/50">
            <th className="border border-gray-600 p-2 text-white">A</th>
            <th className="border border-gray-600 p-2 text-white">B</th>
            <th className="border border-gray-600 p-2 text-white">A AND B</th>
            <th className="border border-gray-600 p-2 text-white">A OR B</th>
          </tr>
        </thead>
        <tbody>
          <tr className="hover:bg-gray-800/50">
            <td className="border border-gray-600 p-2 text-center text-white">T</td>
            <td className="border border-gray-600 p-2 text-center text-white">T</td>
            <td className="border border-gray-600 p-2 text-center text-green-400">T</td>
            <td className="border border-gray-600 p-2 text-center text-green-400">T</td>
          </tr>
          <tr className="hover:bg-gray-800/50">
            <td className="border border-gray-600 p-2 text-center text-white">T</td>
            <td className="border border-gray-600 p-2 text-center text-white">F</td>
            <td className="border border-gray-600 p-2 text-center text-red-400">F</td>
            <td className="border border-gray-600 p-2 text-center text-green-400">T</td>
          </tr>
          <tr className="hover:bg-gray-800/50">
            <td className="border border-gray-600 p-2 text-center text-white">F</td>
            <td className="border border-gray-600 p-2 text-center text-white">T</td>
            <td className="border border-gray-600 p-2 text-center text-red-400">F</td>
            <td className="border border-gray-600 p-2 text-center text-green-400">T</td>
          </tr>
          <tr className="hover:bg-gray-800/50">
            <td className="border border-gray-600 p-2 text-center text-white">F</td>
            <td className="border border-gray-600 p-2 text-center text-white">F</td>
            <td className="border border-gray-600 p-2 text-center text-red-400">F</td>
            <td className="border border-gray-600 p-2 text-center text-red-400">F</td>
          </tr>
        </tbody>
      </table>
    </div>
  );

  const QuizSection = () => {
    const [selectedAnswer, setSelectedAnswer] = useState(null);
    const [showResult, setShowResult] = useState(false);
    
    const question = {
      text: "What is the result of TRUE AND FALSE?",
      options: ["TRUE", "FALSE", "UNDEFINED", "ERROR"],
      correct: 1,
      explanation: "The AND operation only returns TRUE when both inputs are TRUE. Since one input is FALSE, the result is FALSE."
    };

    return (
      <div className="mt-4">
        <h4 className="text-lg font-medium text-white mb-3">{question.text}</h4>
        <div className="space-y-2 mb-4">
          {question.options.map((option, index) => (
            <button
              key={index}
              className={`w-full text-left p-3 rounded-lg border transition-colors \${
                selectedAnswer === index
                  ? showResult
                    ? index === question.correct
                      ? 'bg-green-600/20 border-green-500 text-green-300'
                      : 'bg-red-600/20 border-red-500 text-red-300'
                    : 'bg-blue-600/20 border-blue-500 text-blue-300'
                  : 'bg-gray-700/50 border-gray-600 text-gray-300 hover:bg-gray-700'
              }\`}
              onClick={() => setSelectedAnswer(index)}
            >
              {option}
            </button>
          ))}
        </div>
        <button
          className="bg-gradient-to-r from-purple-600 to-blue-600 text-white py-2 px-4 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-colors"
          onClick={() => setShowResult(!showResult)}
          disabled={selectedAnswer === null}
        >
          {showResult ? 'Hide Answer' : 'Check Answer'}
        </button>
        {showResult && (
          <div className="mt-3 p-3 bg-gray-900/50 rounded-lg">
            <p className="text-sm text-gray-300">{question.explanation}</p>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-8">
          Boolean Logic Study Guide
        </h1>
        
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700 mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-gray-300">Progress</span>
            <span className="text-purple-400">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all duration-300"
              style={{ width: `\${progress}%` }}
            />
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-4 sticky top-4">
              <h3 className="text-lg font-semibold text-white mb-4">Sections</h3>
              {sections.map(section => (
                <button
                  key={section.id}
                  className={`w-full text-left p-3 rounded-lg mb-2 flex items-center gap-3 transition-colors \${
                    currentSection === section.id ? 'bg-purple-600/20 text-purple-300 border border-purple-500/50' : 'text-gray-300 hover:bg-gray-700/50'
                  }\`}
                  onClick={() => setCurrentSection(section.id)}
                >
                  {completedSections.has(section.id) ? 
                    <CheckCircle className="w-4 h-4 text-green-400" /> : 
                    <Circle className="w-4 h-4 text-gray-500" />
                  }
                  <span className="text-sm">{section.title}</span>
                </button>
              ))}
            </div>
          </div>

          <div className="lg:col-span-3">
            {sections.map(section => (
              <div key={section.id} className={currentSection === section.id ? 'block' : 'hidden'}>
                <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
                  <div className="flex justify-between items-center mb-6">
                    <h2 className="text-2xl font-bold text-white">{section.title}</h2>
                    <button
                      className="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-2 rounded-lg hover:from-green-700 hover:to-emerald-700 transition-colors"
                      onClick={() => markComplete(section.id)}
                      disabled={completedSections.has(section.id)}
                    >
                      {completedSections.has(section.id) ? 'Completed ✓' : 'Mark Complete'}
                    </button>
                  </div>
                  
                  <div className="text-gray-300 leading-relaxed mb-4">
                    {section.content}
                  </div>
                  
                  {section.type === 'truth_table' && <TruthTable />}
                  {section.type === 'quiz' && <QuizSection />}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default BooleanLogicStudyGuide;
'''

@app.route('/')
def home():
    return jsonify({
        "message": "🎯 EduForge AI-Powered Artifact Generation System",
        "status": "Demo Ready!",
        "features": [
            "PDF Processing & Analysis",
            "AI-Generated Interactive Study Guides", 
            "Truth Tables & Quizzes",
            "Progress Tracking",
            "Claude-style Artifact Rendering"
        ]
    })

@app.route('/api/artifacts/pdf/<int:pdf_id>')
def get_pdf_artifacts(pdf_id):
    """Demo: Get artifacts for a PDF"""
    return jsonify({
        "success": True,
        "artifacts": [
            {
                "id": 1,
                "title": "Boolean Logic - Interactive Study Guide",
                "type": "study_guide",
                "created_at": "2025-01-21T19:40:00Z",
                "metadata": {
                    "chapter_count": 3,
                    "complexity": "intermediate",
                    "has_truth_tables": True,
                    "has_quizzes": True
                }
            },
            {
                "id": 2,
                "title": "Boolean Logic - Advanced Quiz",
                "type": "quiz", 
                "created_at": "2025-01-21T19:40:00Z",
                "metadata": {
                    "question_count": 10,
                    "difficulty": "intermediate"
                }
            }
        ]
    })

@app.route('/api/artifacts/lecture/<int:lecture_id>')
def get_lecture_artifacts(lecture_id):
    """Demo: Get artifacts for a specific lecture"""
    return jsonify([
        {
            'id': 1,
            'title': 'Boolean Logic Study Guide',
            'type': 'study_guide',
            'created_at': '2024-01-15T10:30:00Z',
            'lecture_id': lecture_id,
            'description': 'Interactive study guide covering Boolean logic fundamentals with truth tables and practice exercises.'
        },
        {
            'id': 2,
            'title': 'Logic Gates Quiz',
            'type': 'quiz',
            'created_at': '2024-01-15T11:00:00Z',
            'lecture_id': lecture_id,
            'description': 'Interactive quiz testing knowledge of AND, OR, NOT, and compound logic gates.'
        }
    ])



@app.route('/api/artifacts/<int:artifact_id>')
def get_artifact(artifact_id):
    """Demo: Get specific artifact details"""
    if artifact_id == 1:
        return jsonify({
            "success": True,
            "artifact": {
                "id": artifact_id,
                "title": "Boolean Logic - Interactive Study Guide",
                "type": "study_guide",
                "react_code": DEMO_STUDY_GUIDE,
                "metadata": {
                    "sections": 3,
                    "interactive_elements": ["truth_table", "quiz"],
                    "estimated_time": "15 minutes"
                },
                "created_at": "2025-01-21T19:40:00Z",
                "updated_at": "2025-01-21T19:40:00Z"
            }
        })
    elif artifact_id == 2:
        return jsonify({
            "success": True,
            "artifact": {
                "id": artifact_id,
                "title": "Boolean Logic - Quiz",
                "type": "quiz",
                "react_code": DEMO_QUIZ,
                "metadata": {
                    "questions": 5,
                    "difficulty": "beginner",
                    "estimated_time": "10 minutes"
                },
                "created_at": "2025-01-21T19:40:00Z",
                "updated_at": "2025-01-21T19:40:00Z"
            }
        })
    else:
        return jsonify({
            "success": False,
            "error": "Artifact not found"
        }), 404

@app.route('/api/lectures')
def get_lectures():
    """Demo: Get lectures list"""
    return jsonify({
        "success": True,
        "lectures": [
            {
                "id": 1,
                "title": "Boolean Logic Fundamentals",
                "filename": "boolean_logic.pdf",
                "created_at": "2025-01-21T19:40:00Z"
            }
        ]
    })

@app.route('/api/lectures/<int:lecture_id>')
def get_lecture(lecture_id):
    """Demo: Get specific lecture"""
    return jsonify({
        "id": lecture_id,
        "title": "Boolean Logic Fundamentals",
        "filename": "boolean_logic.pdf",
        "created_at": "2025-01-21T19:40:00Z"
    })

@app.route('/api/lectures/<int:lecture_id>/chapters')
def get_lecture_chapters(lecture_id):
    """Demo: Get lecture chapters"""
    return jsonify([
        {
            "id": 1,
            "title": "Introduction to Boolean Logic",
            "content": "Boolean logic is the foundation of digital systems..."
        }
    ])

@app.route('/api/lectures/<int:lecture_id>/exams')
def get_lecture_exams(lecture_id):
    """Demo: Get lecture exams"""
    return jsonify([
        {
            "id": 1,
            "title": "Boolean Logic Quiz",
            "created_at": "2025-01-21T19:40:00Z"
        }
    ])

@app.route('/api/artifacts/generate', methods=['POST'])
def generate_artifacts():
    """Demo: Generate new artifacts"""
    data = request.get_json()
    pdf_id = data.get('pdf_id', 1)
    
    return jsonify({
        "success": True,
        "message": "🎯 AI Processing Complete!",
        "job_id": 123,
        "artifacts_created": [
            {
                "type": "study_guide",
                "title": "Interactive Study Guide Generated"
            },
            {
                "type": "quiz", 
                "title": "Interactive Quiz Generated"
            }
        ],
        "analysis": {
            "word_count": 2500,
            "complexity_level": "intermediate",
            "has_mathematical_content": True,
            "has_logical_content": True,
            "chapter_count": 3
        }
    })

if __name__ == '__main__':
    print("🚀 Starting EduForge AI Artifact Demo Server...")
    print("🎯 Visit http://localhost:5001 to see the system status")
    print("✨ The AI-powered artifact generation system is ready!")
    app.run(host='0.0.0.0', port=5001, debug=True)
