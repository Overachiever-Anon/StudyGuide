import { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "../components/ui/badge";
import { Upload, BrainCircuit, BookCopy, CheckCircle, Clock } from 'lucide-react';

interface Lecture {
  id: number;
  title: string;
  filename: string;
  created_at: string;
  size: string;
  status?: 'processing' | 'completed' | 'failed';
}

const dummyLectures: Lecture[] = [];

const DashboardPage = () => {
  const { token } = useAuth();
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");
  const [lectures, setLectures] = useState<Lecture[]>(dummyLectures);

  const fetchLectures = async () => {
    console.log('fetchLectures called with token:', token);
    if (!token) {
      console.log('No token available, skipping fetch');
      return;
    }
    try {
      const response = await fetch('/api/lectures', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const liveLectures: Lecture[] = await response.json();
      setLectures(liveLectures);
    } catch (error) {
      console.error("Failed to fetch lectures:", error);
      setLectures([]); // Clear lectures on error to avoid showing stale data
    }
  };

  useEffect(() => {
    fetchLectures();
  }, [token]);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
      setMessage("");
    }
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a file first.");
      return;
    }
    if (!token) {
      setMessage("Authentication error. Please log in again.");
      return;
    }

    setUploading(true);
    setMessage("Uploading and processing...");

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        setMessage("✅ File uploaded and processed successfully!");
        setFile(null);
        fetchLectures(); // Refetch lectures to show the new one
      } else {
        setMessage(data.message || "Upload failed.");
      }
    } catch (error) {
      console.error("Upload error:", error);
      setMessage("An error occurred during upload.");
    } finally {
      setUploading(false);
    }
  };

  const handleViewLecture = (id: number) => {
    navigate(`/lecture/${id}`);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white p-8">
      <header className="flex justify-between items-center mb-8">
        <div className="flex items-center space-x-3">
          <BrainCircuit className="h-8 w-8 text-purple-400" />
          <h1 className="text-3xl font-bold">AI Learning Dashboard</h1>
        </div>
        <p className="text-purple-300">Transform your PDFs into interactive learning experiences</p>
      </header>

      <main>
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4 mb-8">
          <Card className="bg-gray-800 border-purple-500/30">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium text-gray-300">Total Lectures</CardTitle>
              <BookCopy className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{lectures.length}</div>
              <p className="text-xs text-gray-500">lectures available</p>
            </CardContent>
          </Card>
        </div>

        <Card className="bg-gray-800 border-purple-500/30 mb-8">
          <CardHeader>
            <CardTitle className="flex items-center"><Upload className="mr-2"/> Upload New Lecture PDF</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col space-y-4">
              <div className="flex items-center space-x-4">
                <Input id="pdf-upload" type="file" accept=".pdf" onChange={handleFileChange} className="flex-grow bg-gray-700 border-gray-600 file:text-white" />
                <Button onClick={handleUpload} disabled={!file || uploading} className="bg-purple-600 hover:bg-purple-700">
                  {uploading ? 'Processing...' : 'Upload & Process'}
                </Button>
              </div>
              {message && <p className={`text-sm ${message.startsWith('✅') ? 'text-green-400' : 'text-red-400'}`}>{message}</p>}
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-purple-500/30">
          <CardHeader>
            <CardTitle className="text-white">My Lecture Library</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow className="border-gray-700">
                  <TableHead className="text-white">Title</TableHead>
                  <TableHead className="text-white">File</TableHead>
                  <TableHead className="text-white">Size</TableHead>
                  <TableHead className="text-white">Status</TableHead>
                  <TableHead className="text-white">Created</TableHead>
                  <TableHead className="text-white">Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {lectures.length > 0 ? lectures.map((lecture: Lecture) => (
                  <TableRow key={lecture.id} className="border-gray-700">
                    <TableCell>{lecture.title}</TableCell>
                    <TableCell className="text-gray-400">{lecture.filename}</TableCell>
                    <TableCell>{lecture.size || 'N/A'}</TableCell>
                    <TableCell>
                      <Badge variant={lecture.status === 'completed' ? 'default' : 'secondary'} className={lecture.status === 'completed' ? 'bg-green-600' : 'bg-yellow-600'}>
                        {lecture.status === 'completed' ? <CheckCircle className="mr-1 h-3 w-3" /> : <Clock className="mr-1 h-3 w-3" />}
                        {lecture.status || 'Processing'}
                      </Badge>
                    </TableCell>
                    <TableCell>{new Date(lecture.created_at).toLocaleDateString()}</TableCell>
                    <TableCell className="space-x-2">
                      <Button size="sm" onClick={() => handleViewLecture(lecture.id)} className="bg-blue-600 hover:bg-blue-700">View</Button>
                    </TableCell>
                  </TableRow>
                )) : (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center text-gray-500 py-8">No lectures found. Upload a PDF to get started.</TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </main>
    </div>
  );
};

export default DashboardPage;
