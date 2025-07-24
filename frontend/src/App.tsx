import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import HomePage from './pages/Home';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import DashboardPage from './pages/Dashboard';
import LecturePage from './pages/LecturePage';
import ExamPage from './pages/ExamPage';
import ArtifactsPage from './pages/ArtifactsPage';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import { AuthProvider } from './context/AuthContext';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route 
              path="/dashboard" 
              element={
                <ProtectedRoute>
                  <DashboardPage />
                </ProtectedRoute>
              }
            />
            <Route 
              path="/lecture/:id"
              element={
                <ProtectedRoute>
                  <LecturePage />
                </ProtectedRoute>
              }
            />
            <Route 
              path="/exam/:examId"
              element={
                <ProtectedRoute>
                  <ExamPage />
                </ProtectedRoute>
              }
            />
            <Route 
              path="/artifacts/:lectureId"
              element={
                <ProtectedRoute>
                  <ArtifactsPage />
                </ProtectedRoute>
              }
            />
          </Route>
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;




