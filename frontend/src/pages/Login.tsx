import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { LogIn, Mail, Lock, Sparkles } from 'lucide-react';

// Dummy user data for testing
const DUMMY_USERS = [
  { email: 'demo@eduforge.ai', password: 'demo123', name: 'Demo User' },
  { email: 'student@university.edu', password: 'student123', name: 'Alex Student' },
  { email: 'professor@university.edu', password: 'prof123', name: 'Dr. Sarah Wilson' },
];

const LoginPage = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 800));
    
    try {
      // Check dummy users first
      const dummyUser = DUMMY_USERS.find(user => user.email === email && user.password === password);
      
      if (dummyUser) {
        // Simulate successful login with dummy data
        const mockToken = `dummy_token_${Date.now()}`;
        login(mockToken);
        navigate('/dashboard');
        setIsLoading(false);
        return;
      }

      // Try real API if dummy login fails
      const response = await fetch('http://localhost:5001/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        login(data.access_token);
        navigate('/dashboard');
      } else {
        alert(data.message || 'Login failed');
      }
    } catch (error) {
      console.error('API not available, using dummy data only:', error);
      alert('Invalid credentials. Try demo@eduforge.ai / demo123');
    }
    
    setIsLoading(false);
  };

  const fillDemoCredentials = () => {
    setEmail('demo@eduforge.ai');
    setPassword('demo123');
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-gray-900 to-purple-900/20" />
      <div className="absolute top-1/4 left-1/4 w-64 h-64 bg-blue-500/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{animationDelay: '2s'}} />
      
      <div className="relative z-10 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-500/10 to-purple-500/10 border border-blue-500/20 text-blue-300 px-4 py-2 rounded-full text-sm font-medium mb-4">
            <Sparkles className="w-4 h-4" />
            Welcome to EduForge
          </div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent mb-2">
            Sign In
          </h1>
          <p className="text-gray-400">Access your AI-powered learning platform</p>
        </div>

        <Card className="bg-gray-800/50 border-gray-700/50 backdrop-blur-sm shadow-2xl">
          <CardHeader className="text-center">
            <CardTitle className="text-xl text-white flex items-center justify-center gap-2">
              <LogIn className="w-5 h-5 text-blue-400" />
              Login to Your Account
            </CardTitle>
            <CardDescription className="text-gray-400">
              Enter your credentials to access your dashboard
            </CardDescription>
          </CardHeader>
          
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email" className="text-gray-300 flex items-center gap-2">
                  <Mail className="w-4 h-4" />
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="your@email.com"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="bg-gray-700/50 border-gray-600 text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500/20"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password" className="text-gray-300 flex items-center gap-2">
                  <Lock className="w-4 h-4" />
                  Password
                </Label>
                <Input 
                  id="password" 
                  type="password" 
                  placeholder="••••••••"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="bg-gray-700/50 border-gray-600 text-white placeholder:text-gray-400 focus:border-blue-500 focus:ring-blue-500/20"
                />
              </div>

              {/* Demo credentials helper */}
              <div className="bg-blue-900/20 border border-blue-500/30 rounded-lg p-3">
                <p className="text-sm text-blue-300 mb-2 font-medium">🚀 Quick Demo Access:</p>
                <Button 
                  type="button" 
                  variant="outline" 
                  size="sm" 
                  onClick={fillDemoCredentials}
                  className="text-xs bg-blue-500/10 border-blue-500/30 text-blue-300 hover:bg-blue-500/20"
                >
                  Use Demo Credentials
                </Button>
                <p className="text-xs text-gray-400 mt-1">demo@eduforge.ai / demo123</p>
              </div>
            </CardContent>
            
            <CardFooter className="flex flex-col space-y-4">
              <Button 
                type="submit" 
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-medium py-2.5 transition-all duration-200 transform hover:scale-[1.02]"
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="flex items-center gap-2">
                    <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Signing in...
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <LogIn className="w-4 h-4" />
                    Sign In
                  </div>
                )}
              </Button>
              
              <div className="text-center text-sm text-gray-400">
                Don't have an account?{" "}
                <Link to="/register" className="text-blue-400 hover:text-blue-300 underline font-medium">
                  Create Account
                </Link>
              </div>
            </CardFooter>
          </form>
        </Card>
        
        {/* Additional demo info */}
        <div className="mt-6 text-center">
          <div className="bg-gray-800/30 border border-gray-700/50 rounded-lg p-4">
            <h3 className="text-sm font-medium text-gray-300 mb-2">Demo Accounts Available:</h3>
            <div className="space-y-1 text-xs text-gray-400">
              <div>👨‍🎓 Student: student@university.edu / student123</div>
              <div>👩‍🏫 Professor: professor@university.edu / prof123</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
