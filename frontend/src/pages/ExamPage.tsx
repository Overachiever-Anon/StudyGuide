import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { toast } from "sonner";
import { Label } from "@/components/ui/label";
import { Brain, Plus, FileText } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"

interface Question {
  id: number;
  question_text: string;
  options: string[];
  correct_answer: string;
}

interface Exam {
    id: number;
    title: string;
    pdf_id: number;
}

interface Chapter {
  id: number;
  title: string;
}

// Dummy data for testing when backend is not available
const getDummyExamData = (examId: string) => {
  const exams = {
    '1': { id: 1, title: 'ML Fundamentals Quiz', pdf_id: 1 },
    '2': { id: 2, title: 'Algorithm Comparison Test', pdf_id: 1 },
    '3': { id: 3, title: 'React Patterns Assessment', pdf_id: 2 },
    '4': { id: 4, title: 'Database Design Quiz', pdf_id: 3 }
  };

  const questions = {
    '1': [
      {
        id: 1,
        question_text: 'What is the main goal of supervised learning?',
        options: ['To find hidden patterns in unlabeled data', 'To learn from labeled training examples', 'To interact with an environment through trial and error', 'To reduce the dimensionality of data'],
        correct_answer: 'To learn from labeled training examples'
      },
      {
        id: 2,
        question_text: 'Which algorithm is best suited for classification tasks?',
        options: ['Linear Regression', 'K-Means Clustering', 'Decision Trees', 'PCA (Principal Component Analysis)'],
        correct_answer: 'Decision Trees'
      }
    ],
    '2': [
      {
        id: 4,
        question_text: 'Which algorithm typically provides the best accuracy for complex datasets?',
        options: ['Linear Regression', 'Random Forest', 'K-Means', 'Naive Bayes'],
        correct_answer: 'Random Forest'
      }
    ],
    '3': [
      {
        id: 6,
        question_text: 'What is the primary benefit of using Higher-Order Components (HOCs)?',
        options: ['They improve rendering performance', 'They enable code reuse and logic sharing', 'They reduce bundle size', 'They eliminate the need for state management'],
        correct_answer: 'They enable code reuse and logic sharing'
      }
    ],
    '4': []
  };

  const chapters = {
    '1': [{ id: 1, title: 'Chapter 1: What is Machine Learning?' }, { id: 2, title: 'Chapter 2: Types of Machine Learning' }],
    '2': [{ id: 4, title: 'Chapter 1: Component Composition' }],
    '3': [{ id: 6, title: 'Chapter 1: Database Fundamentals' }],
    '4': []
  };

  const exam = exams[examId as keyof typeof exams] || null;
  const examQuestions = questions[examId as keyof typeof questions] || [];
  const examChapters = exam ? chapters[exam.pdf_id.toString() as keyof typeof chapters] || [] : [];

  return { exam, questions: examQuestions, chapters: examChapters };
};

const ExamPage = () => {
  const { examId } = useParams<{ examId: string }>();
  const { token } = useAuth();
  const [exam, setExam] = useState<Exam | null>(null);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [newQuestion, setNewQuestion] = useState({ question_text: '', options: ['', '', '', ''], correct_answer: '' });
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [selectedChapter, setSelectedChapter] = useState<string>("");
  const [isGenerating, setIsGenerating] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchExamDetails = async () => {
      if (!token || !examId) return;
      
      try {
        // Try to fetch from API first
        const [examResponse, questionsResponse] = await Promise.all([
          fetch(`http://localhost:5001/api/exams/${examId}`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
          fetch(`http://localhost:5001/api/exams/${examId}/questions`, {
            headers: { Authorization: `Bearer ${token}` },
          }),
        ]);

        if (examResponse.ok && questionsResponse.ok) {
          // If API is available, use real data
          const examData = await examResponse.json();
          const questionsData = await questionsResponse.json();

          setExam(examData);
          setQuestions(questionsData);

          if (examData.pdf_id) {
            const chaptersResponse = await fetch(`http://localhost:5001/api/lectures/${examData.pdf_id}/chapters`, {
              headers: { Authorization: `Bearer ${token}` },
            });
            if (chaptersResponse.ok) {
              const chaptersData = await chaptersResponse.json();
              setChapters(chaptersData);
            }
          }
        } else {
          throw new Error('API not available');
        }
      } catch (err) {
        // Fallback to dummy data if API fails
        console.log('API not available, using dummy data for exam:', examId);
        const dummyData = getDummyExamData(examId);
        
        if (dummyData.exam) {
          setExam(dummyData.exam);
          setQuestions(dummyData.questions);
          setChapters(dummyData.chapters);
        } else {
          setError('Exam not found');
        }
      } finally {
        setLoading(false);
      }
    };
    fetchExamDetails();
  }, [examId, token]);

  const handleGenerateQuestions = async () => {
    if (!selectedChapter || !examId || !token) {
      toast.warning("Please select a chapter to generate questions from.");
      return;
    }
    setIsGenerating(true);
    try {
      const response = await fetch(`http://localhost:5001/api/chapters/${selectedChapter}/generate-questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ exam_id: examId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to generate questions.');
      }

      // Re-fetch questions to update the list
      const questionsResponse = await fetch(`http://localhost:5001/api/exams/${examId}/questions`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!questionsResponse.ok) throw new Error('Failed to fetch updated questions.');
      const updatedQuestions = await questionsResponse.json();
      setQuestions(updatedQuestions);
      toast.success('Questions generated successfully!');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'An unknown error occurred during generation.';
      setError(message);
      toast.error(message);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleAddQuestion = async () => {
    if (!token || !newQuestion.question_text.trim() || newQuestion.options.some(o => !o.trim()) || !newQuestion.correct_answer.trim()) {
      toast.warning('Please fill out all fields for the new question.');
      return;
    }

    try {
      const response = await fetch(`http://localhost:5001/api/exams/${examId}/questions`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(newQuestion),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to add question.');
      }

      const addedQuestion = await response.json();
      setQuestions([...questions, addedQuestion.question]);
      setNewQuestion({ question_text: '', options: ['', '', '', ''], correct_answer: '' }); // Reset form
      toast.success('Question added successfully!');
    } catch (err) {
      const message = err instanceof Error ? err.message : 'An unknown error occurred while adding the question.';
      setError(message);
      toast.error(message);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center space-y-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="text-gray-400">Loading exam details...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-950 flex items-center justify-center">
        <div className="text-center space-y-4">
          <FileText className="w-16 h-16 text-gray-600 mx-auto" />
          <div className="space-y-2">
            <h2 className="text-xl font-semibold text-gray-300">Exam Not Found</h2>
            <p className="text-gray-500">{error}</p>
            <Link to="/dashboard">
              <Button className="mt-4">Back to Dashboard</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-950">
      <div className="container mx-auto p-6 space-y-8">
        {/* Header */}
        <div className="space-y-4">
          <Link to="/dashboard" className="inline-flex items-center text-blue-400 hover:text-blue-300 transition-colors">
            ← Back to Dashboard
          </Link>
          <div className="flex justify-between items-center">
            <div className="space-y-2">
              <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-orange-400 bg-clip-text text-transparent">
                {exam?.title || 'Exam'}
              </h1>
              <p className="text-gray-400">Manage and create questions for this exam</p>
            </div>
            <Dialog>
              <DialogTrigger asChild>
                <Button className="bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-400 hover:to-pink-400 text-white">
                  <Brain className="w-4 h-4 mr-2" />
                  Generate with AI
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-gray-900 border-gray-800">
                <DialogHeader>
                  <DialogTitle className="text-gray-100">Generate Questions with AI</DialogTitle>
                  <DialogDescription className="text-gray-400">
                    Select a chapter to automatically generate questions for this exam.
                  </DialogDescription>
                </DialogHeader>
                <div className="space-y-4 py-4">
                  <Select onValueChange={setSelectedChapter} value={selectedChapter}>
                    <SelectTrigger className="bg-gray-800 border-gray-700 text-gray-200">
                      <SelectValue placeholder="Select a chapter" />
                    </SelectTrigger>
                    <SelectContent className="bg-gray-800 border-gray-700">
                      {chapters.map((chapter) => (
                        <SelectItem key={chapter.id} value={String(chapter.id)} className="text-gray-200 focus:bg-gray-700">
                          {chapter.title}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                  <Button 
                    onClick={handleGenerateQuestions} 
                    disabled={isGenerating || !selectedChapter}
                    className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-400 hover:to-pink-400 text-white"
                  >
                    {isGenerating ? 'Generating...' : 'Generate Questions'}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>
        
        {/* Add New Question */}
        <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-gray-100">
              <Plus className="w-5 h-5 text-green-400" />
              Add New Question
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
          <div>
            <Label htmlFor="question-text">Question</Label>
            <Input id="question-text" placeholder="What is...?" value={newQuestion.question_text} onChange={(e) => setNewQuestion({...newQuestion, question_text: e.target.value})} />
          </div>
          <div>
            <Label>Options</Label>
            <div className="grid grid-cols-2 gap-4">
              <Input placeholder="Option A" value={newQuestion.options[0]} onChange={(e) => {
                const newOptions = [...newQuestion.options];
                newOptions[0] = e.target.value;
                setNewQuestion({...newQuestion, options: newOptions});
              }} />
              <Input placeholder="Option B" value={newQuestion.options[1]} onChange={(e) => {
                const newOptions = [...newQuestion.options];
                newOptions[1] = e.target.value;
                setNewQuestion({...newQuestion, options: newOptions});
              }} />
              <Input placeholder="Option C" value={newQuestion.options[2]} onChange={(e) => {
                const newOptions = [...newQuestion.options];
                newOptions[2] = e.target.value;
                setNewQuestion({...newQuestion, options: newOptions});
              }} />
              <Input placeholder="Option D" value={newQuestion.options[3]} onChange={(e) => {
                const newOptions = [...newQuestion.options];
                newOptions[3] = e.target.value;
                setNewQuestion({...newQuestion, options: newOptions});
              }} />
            </div>
          </div>
          <div>
            <Label htmlFor="correct-answer">Correct Answer</Label>
            <Input id="correct-answer" placeholder="Option A" value={newQuestion.correct_answer} onChange={(e) => setNewQuestion({...newQuestion, correct_answer: e.target.value})} />
          </div>
          <Button onClick={handleAddQuestion}>Add Question</Button>
        </CardContent>
      </Card>

        {/* Question List */}
        <Card className="bg-gray-900/50 border-gray-800 backdrop-blur-sm">
          <CardHeader>
            <CardTitle className="text-gray-100">Question List ({questions.length})</CardTitle>
          </CardHeader>
          <CardContent>
            {questions.length > 0 ? (
              <div className="space-y-4">
                {questions.map((q) => (
                  <div key={q.id} className="p-4 bg-gray-800/50 border border-gray-700 rounded-lg">
                    <p className="font-semibold text-gray-200 mb-3">{q.question_text}</p>
                    <ul className="space-y-1">
                      {q.options.map((opt, index) => (
                        <li key={index} className={`flex items-center gap-2 ${opt === q.correct_answer ? 'text-green-400' : 'text-gray-300'}`}>
                          {opt === q.correct_answer && <span className="text-green-400">✓</span>}
                          <span>{String.fromCharCode(65 + index)}. {opt}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-400 text-center py-8">No questions yet. Add your first question above or generate with AI!</p>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ExamPage;
