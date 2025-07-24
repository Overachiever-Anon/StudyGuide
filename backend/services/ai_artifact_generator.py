import json
import re
import anthropic
from jinja2 import Template

class AIArtifactGenerator:
    """Generate interactive educational artifacts using AI"""

    def __init__(self, anthropic_api_key: str = None):
        self.anthropic_client = anthropic.Anthropic(api_key=anthropic_api_key) if anthropic_api_key else None
        self.system_prompt = """
        You are an expert in creating educational tools. Your task is to generate a single, self-contained React component file based on the provided text. Follow these rules precisely:

        1.  **Structure**: Create a single default export function component, e.g., `export default function MyComponent() { ... }`. The component name must be PascalCase and derived from the title.
        2.  **Dependencies**: Use only React hooks (`useState`, `useEffect`, etc.). Do NOT use any external libraries like lucide-react. All icons must be defined as inline SVG React components within the file.
        3.  **Styling**: Use only standard Tailwind CSS classes. Do not use custom CSS.
        4.  **Interactivity**: Use `onClick`, `onChange`, etc. Do NOT use `<form>` tags.
        5.  **State Management**: Use `useState` or `useReducer` for all state. Do not use `localStorage` or `sessionStorage`.
        6.  **Content**: The component should be a complete, runnable, and visually appealing educational tool based on the provided text.
        7.  **Output**: Return ONLY the raw React component code, inside a single ```jsx block. Do not include any explanation or extra text outside the code block.
        """

    def generate_study_guide(self, content: str, title: str) -> str:
        """Generate interactive React study guide component"""
        prompt = f"Create a comprehensive, interactive study guide from the following text. The guide should include sections, key terms, and summaries. The component name should be {self._sanitize_component_name(title)}StudyGuide. Text: {content}"
        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=4096,
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                ).content[0].text
                return self._extract_react_code(response)
            return self._generate_fallback_study_guide(title, content)
        except Exception as e:
            print(f"Error generating study guide: {e}")
            return self._generate_fallback_study_guide(title, content)

    def generate_quiz(self, content: str, title: str, num_questions: int = 5) -> str:
        """Generate interactive quiz component"""
        prompt = f"Create an interactive multiple-choice quiz with {num_questions} questions from the following text. Include questions, options, and a way to check answers. The component name should be {self._sanitize_component_name(title)}Quiz. Text: {content}"
        try:
            if self.anthropic_client:
                response = self.anthropic_client.messages.create(
                    model="claude-3-opus-20240229",
                    max_tokens=4096,
                    system=self.system_prompt,
                    messages=[{"role": "user", "content": prompt}]
                ).content[0].text
                return self._extract_react_code(response)
            return self._generate_fallback_quiz(title)
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._generate_fallback_quiz(title)

    def _generate_fallback_study_guide(self, title: str, content: str) -> str:
        """Generate a basic study guide component for demo using Jinja2"""
        component_name = self._sanitize_component_name(title)
        safe_content = json.dumps(content[:500].strip() + '...')
        template_str = """
import React, { useState } from 'react';

const CheckCircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="inline-block h-5 w-5 text-green-500"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
);

const CircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="inline-block h-5 w-5 text-gray-400"><circle cx="12" cy="12" r="10"/></svg>
);

export default function {{ component_name }}StudyGuide() {
  const [completedSections, setCompletedSections] = useState(new Set());
  const [currentSection, setCurrentSection] = useState('section_1');

  const sections = [
    {
      id: 'section_1',
      title: 'Introduction',
      content: {{ content }},
      type: 'text'
    },
    {
      id: 'section_2', 
      title: 'Interactive Quiz',
      content: 'Test your knowledge with this interactive quiz.',
      type: 'quiz'
    }
  ];

  const markComplete = (sectionId) => {
    setCompletedSections(prev => new Set([...prev, sectionId]));
  };

  const progress = (completedSections.size / sections.length) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20 text-gray-200 p-4 sm:p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent mb-8">
          {{ title }}
        </h1>
        <div className="bg-gray-800/50 rounded-lg p-4 border border-gray-700 mb-8">
          <div className="flex justify-between mb-2">
            <span className="text-gray-300">Progress</span>
            <span className="text-purple-400">{Math.round(progress)}%</span>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all duration-500"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          <div className="lg:col-span-1">
            <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-4">
              <h3 className="text-lg font-semibold text-white mb-4">Sections</h3>
              {sections.map(section => (
                <button
                  key={section.id}
                  className={`w-full text-left p-3 rounded-lg mb-2 flex items-center transition-colors ${
                    currentSection === section.id ? 'bg-purple-600/30 text-purple-300' : 'text-gray-300 hover:bg-gray-700/50'
                  }`}
                  onClick={() => setCurrentSection(section.id)}
                >
                  {completedSections.has(section.id) ? <CheckCircleIcon /> : <CircleIcon />}
                  <span className="ml-2">{section.title}</span>
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
                    {!completedSections.has(section.id) && (
                      <button
                        className="bg-gradient-to-r from-green-600 to-emerald-600 text-white px-4 py-2 rounded-lg hover:opacity-90 transition-opacity"
                        onClick={() => markComplete(section.id)}
                      >
                        Mark as Completed
                      </button>
                    )}
                  </div>
                  <div className="prose prose-invert max-w-none text-gray-300 leading-relaxed">
                    <p>{section.content}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
"""
        template = Template(template_str)
        return template.render(component_name=component_name, title=title, content=safe_content)

    def _generate_fallback_quiz(self, title: str) -> str:
        """Generate a basic quiz component for demo using Jinja2"""
        component_name = self._sanitize_component_name(title)
        template_str = """
import React, { useState } from 'react';

const CircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="inline-block h-5 w-5 text-gray-400"><circle cx="12" cy="12" r="10"/></svg>
);

const CheckCircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="inline-block h-5 w-5 text-green-500"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
);

export default function {{ component_name }}Quiz() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [isCorrect, setIsCorrect] = useState(null);
  const [score, setScore] = useState(0);
  const [showResults, setShowResults] = useState(false);

  const questions = [
    {
      question: "What is a primary key in a relational database?",
      options: [
        "A key used for encryption.",
        "A unique identifier for a record in a table.",
        "A key that links two tables together.",
        "A key that is not unique."
      ],
      correct: 1,
      explanation: "A primary key is a column (or a set of columns) in a table that uniquely identifies each row. It must contain unique values and cannot have NULL values."
    },
    {
      question: "Which of the following is a characteristic of a functional programming language?",
      options: [
        "Mutable state",
        "For-loops",
        "Immutability and pure functions",
        "Object-oriented inheritance"
      ],
      correct: 2,
      explanation: "Functional programming emphasizes immutability (data cannot be changed after creation) and pure functions (functions that return the same output for the same input and have no side effects)."
    }
  ];

  const handleAnswer = (optionIndex) => {
    if (isCorrect !== null) return;
    setSelectedAnswer(optionIndex);
    const correct = optionIndex === questions[currentQuestion].correct;
    setIsCorrect(correct);
    if (correct) {
      setScore(score + 1);
    }
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setIsCorrect(null);
    } else {
      setShowResults(true);
    }
  };

  const restartQuiz = () => {
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setIsCorrect(null);
    setScore(0);
    setShowResults(false);
  };

  if (showResults) {
    return (
      <div className="p-8 bg-gray-800 text-white rounded-lg max-w-2xl mx-auto text-center">
        <h2 className="text-3xl font-bold mb-4">Quiz Results</h2>
        <p className="text-xl mb-6">You scored {score} out of {questions.length}</p>
        <button 
          onClick={restartQuiz}
          className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transition-colors"
        >
          Restart Quiz
        </button>
      </div>
    );
  }

  const q = questions[currentQuestion];

  return (
    <div className="p-4 sm:p-8 bg-gray-800 text-white rounded-lg max-w-2xl mx-auto">
      <h2 className="text-2xl sm:text-3xl font-bold mb-2 text-purple-300">{{ title }} Quiz</h2>
      <p className="text-gray-400 mb-6">Question {currentQuestion + 1} of {questions.length}</p>
      
      <div className="bg-gray-900 p-6 rounded-lg">
        <p className="text-lg sm:text-xl mb-6 min-h-[60px]">{q.question}</p>
        <div className="space-y-3">
          {q.options.map((option, index) => {
            const isSelected = selectedAnswer === index;
            let buttonClass = 'w-full text-left p-4 rounded-lg transition-all duration-200 border-2 border-transparent ';
            if (isSelected) {
              buttonClass += isCorrect ? 'bg-green-500/20 border-green-500' : 'bg-red-500/20 border-red-500';
            } else {
              buttonClass += 'bg-gray-700 hover:bg-gray-600';
            }
            if (selectedAnswer !== null && index === q.correct) {
                buttonClass = 'w-full text-left p-4 rounded-lg transition-all duration-200 border-2 bg-green-500/20 border-green-500';
            }

            return (
              <button key={index} onClick={() => handleAnswer(index)} className={buttonClass} disabled={selectedAnswer !== null}>
                {option}
              </button>
            );
          })}
        </div>

        {selectedAnswer !== null && (
          <div className="mt-6 p-4 rounded-lg bg-gray-700/50">
            <p className="font-bold text-lg mb-2">{isCorrect ? 'Correct!' : 'Incorrect'}</p>
            <p className="text-gray-300">{q.explanation}</p>
          </div>
        )}

        <div className="mt-8 text-right">
          <button 
            onClick={handleNext}
            className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-6 rounded-lg transition-colors disabled:opacity-50"
            disabled={selectedAnswer === null}
          >
            {currentQuestion < questions.length - 1 ? 'Next' : 'Finish'}
          </button>
        </div>
      </div>
    </div>
  );
}
"""
        template = Template(template_str)
        return template.render(component_name=component_name, title=title)

    def _sanitize_component_name(self, title: str) -> str:
        """Sanitize title to be a valid component name"""
        return re.sub(r'[^a-zA-Z0-9]', '', title.title())

    def _extract_react_code(self, response_text: str) -> str:
        """Extracts React code from a markdown block and ensures it has a proper function definition."""
        code = response_text
        match = re.search(r'```jsx\n(.*)```', response_text, re.DOTALL)
        if match:
            code = match.group(1).strip()

        # AI can sometimes generate "export default MyComponent()" instead of "export default function MyComponent()"
        # This regex finds a line starting with "export default" followed by a PascalCase component name and parentheses,
        # and inserts the "function" keyword.
        # It specifically avoids matching if 'function' or 'const' is already there.
        if re.search(r'^export default [A-Z]', code, re.MULTILINE) and not re.search(r'^export default (function|const)', code, re.MULTILINE):
             code = re.sub(r'^(export default )([A-Z]\w*\s*\(.*)', r'\1function \2', code, 1, re.MULTILINE)

        return code