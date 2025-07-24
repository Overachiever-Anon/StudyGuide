import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { BookOpen, FileText, Clock, Sparkles, BrainCircuit } from 'lucide-react';

// --- Interface Definitions ---
interface Chapter {
  id: number;
  title: string;
  content: string;
}

interface Lecture {
  id: number;
  title: string;
  filename: string;
}

interface Exam {
  id: number;
  title: string;
  created_at: string;
}

interface Artifact {
  id: number;
  title: string;
  type: string;
  created_at: string;
}

// --- Component --- 
const LecturePage = () => {
  const { id } = useParams<{ id: string }>();
  const { token } = useAuth();

  // --- State Management ---
  const [lecture, setLecture] = useState<Lecture | null>(null);
  const [chapters, setChapters] = useState<Chapter[]>([]);
  const [exams, setExams] = useState<Exam[]>([]);
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);
  const [newExamTitle, setNewExamTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // --- Data Fetching Effect ---
  useEffect(() => {
    const fetchLectureDetails = async () => {
      if (!token || !id) {
        setLoading(false);
        setError("Invalid lecture ID or not logged in.");
        return;
      }

      setLoading(true);
      try {
        const responses = await Promise.all([
          fetch(`/api/lectures/${id}`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`/api/lectures/${id}/chapters`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`/api/lectures/${id}/exams`, { headers: { Authorization: `Bearer ${token}` } }),
          fetch(`/api/artifacts/pdf/${id}`, { headers: { Authorization: `Bearer ${token}` } })
        ]);

        const allOk = responses.every(res => res.ok);
        if (!allOk) {
          for (const res of responses) {
              if (!res.ok) {
                  console.error(`Request to ${res.url} failed with status ${res.status}`);
              }
          }
          throw new Error('One or more API requests failed. Check network tab for details.');
        }

        const [lectureData, chaptersData, examsData, artifactsResponse] = await Promise.all(responses.map(res => res.json()));
        
        setLecture(lectureData.lecture || lectureData);
        setChapters(chaptersData.chapters || []);
        setExams(examsData.exams || []);
        setArtifacts(artifactsResponse.artifacts || []);

      } catch (err: any) {
        console.error('Failed to fetch lecture details:', err);
        setError(err.message || 'Failed to load lecture data. Please try again later.');
        // Clear state on error
        setLecture(null);
        setChapters([]);
        setExams([]);
        setArtifacts([]);
      } finally {
        setLoading(false);
      }
    };

    fetchLectureDetails();
  }, [id, token]);

  // --- Event Handlers ---
  const handleCreateExam = async () => {
    if (!token || !newExamTitle.trim() || !id) return;

    try {
      const response = await fetch(`/api/lectures/${id}/exams`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ title: newExamTitle }),
      });

      if (response.ok) {
        const newExam = await response.json();
        setExams(prevExams => [newExam.exam, ...prevExams]);
        setNewExamTitle("");
      } else {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create exam.');
      }
    } catch (err: any) {
      console.error('Failed to create exam:', err);
      alert(`Error: ${err.message}`);
    }
  };

  // --- Render Logic ---
  if (loading) {
    return <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">Loading lecture details...</div>;
  }

  if (error) {
    return <div className="flex justify-center items-center min-h-screen bg-gray-900 text-red-500">Error: {error}</div>;
  }

  if (!lecture) {
    return <div className="flex justify-center items-center min-h-screen bg-gray-900 text-white">Lecture not found.</div>;
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <header className="mb-8">
        <h1 className="text-4xl font-bold mb-2">{lecture.title}</h1>
        <div className="flex items-center text-gray-400">
          <FileText className="mr-2 h-5 w-5" />
          <span>{lecture.filename}</span>
        </div>
      </header>

      <main className="grid md:grid-cols-3 gap-8">
        <div className="md:col-span-2 space-y-8">
          {/* AI Artifacts Card */}
          <Card className="bg-gray-800 border-purple-500/30">
            <CardHeader>
              <CardTitle className="flex items-center">
                <BrainCircuit className="mr-2 h-5 w-5 text-purple-400" />
                AI-Generated Artifacts
              </CardTitle>
            </CardHeader>
            <CardContent>
              {artifacts.length > 0 ? (
                <ul className="space-y-2">
                  {artifacts.map((artifact) => (
                    <li key={artifact.id} className="flex justify-between items-center p-3 bg-gray-700/50 rounded-md">
                      <div>
                        <p className="font-semibold">{artifact.title}</p>
                        <p className="text-xs text-gray-400">Type: {artifact.type.replace('_', ' ')}</p>
                      </div>
                      <Link to={`/artifacts/${id}`}>
                        <Button size="sm" className="bg-purple-600 hover:bg-purple-700">View Artifact</Button>
                      </Link>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 text-center py-4">No AI artifacts generated for this lecture yet.</p>
              )}
            </CardContent>
          </Card>

          {/* Lecture Content Card */}
          <Card className="bg-gray-800 border-purple-500/30">
            <CardHeader>
              <CardTitle className="flex items-center">
                <BookOpen className="mr-2 h-5 w-5 text-purple-400" />
                Lecture Content
              </CardTitle>
            </CardHeader>
            <CardContent>
              {chapters.length > 0 ? (
                <Accordion type="single" collapsible className="w-full">
                  {chapters.map((chapter) => (
                    <AccordionItem value={`item-${chapter.id}`} key={chapter.id} className="border-gray-700">
                      <AccordionTrigger className="hover:no-underline">{chapter.title}</AccordionTrigger>
                      <AccordionContent className="prose prose-invert max-w-none text-gray-300">
                        {chapter.content.split('\n').map((paragraph, index) => (
                          <p key={index}>{paragraph}</p>
                        ))}
                      </AccordionContent>
                    </AccordionItem>
                  ))}
                </Accordion>
              ) : (
                 <p className="text-gray-500 text-center py-4">No chapters found for this lecture.</p>
              )}
            </CardContent>
          </Card>
        </div>

        <div className="space-y-8">
          {/* Exams & Quizzes Card */}
          <Card className="bg-gray-800 border-purple-500/30">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Sparkles className="mr-2 h-5 w-5 text-purple-400" />
                Exams & Quizzes
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="mb-4 flex gap-2">
                <Input 
                  type="text" 
                  placeholder="New exam title..." 
                  value={newExamTitle}
                  onChange={(e) => setNewExamTitle(e.target.value)}
                  className="bg-gray-700 border-gray-600"
                />
                <Button onClick={handleCreateExam} className="bg-purple-600 hover:bg-purple-700">Create Exam</Button>
              </div>
              {exams.length > 0 ? (
                <ul className="space-y-2">
                  {exams.map((exam) => (
                    <li key={exam.id} className="flex justify-between items-center p-2 bg-gray-700/50 rounded-md">
                      <span>{exam.title}</span>
                      <div className="flex items-center gap-4">
                        <span className="text-xs text-gray-400 flex items-center">
                          <Clock className="mr-1 h-3 w-3" />
                          {new Date(exam.created_at).toLocaleDateString()}
                        </span>
                        <Link to={`/exam/${exam.id}`}>
                          <Button size="sm" className="bg-blue-600 hover:bg-blue-700">Take Exam</Button>
                        </Link>
                      </div>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500 text-center py-4">No exams found for this lecture.</p>
              )}
            </CardContent>
          </Card>
        </div>
      </main>
    </div>
  );
};

export default LecturePage;
