import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BookOpen, Brain, Sparkles } from "lucide-react";

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Simple test - if this shows dark background, Tailwind is working */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-6xl font-bold mb-8 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            Welcome to EduForge
          </h1>
          <p className="text-xl text-gray-300 mb-8">
            Transform your lecture slides into interactive, engaging learning experiences with the power of cutting-edge AI.
          </p>
          
          <div className="flex gap-4 justify-center mb-16">
            <Button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 text-lg">
              Get Started for Free
            </Button>
            <Button variant="outline" className="border-gray-600 text-gray-300 hover:bg-gray-800 px-8 py-3 text-lg">
              Watch Demo
            </Button>
          </div>

          {/* Feature cards with dark theme */}
          <div className="grid md:grid-cols-3 gap-8 mt-16">
            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6 text-center">
                <BookOpen className="w-12 h-12 text-blue-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">Smart PDF Processing</h3>
                <p className="text-gray-400">Upload your lecture slides and let our advanced AI extract key concepts, create structured learning materials, and generate comprehensive summaries.</p>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6 text-center">
                <Brain className="w-12 h-12 text-purple-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">AI-Generated Quizzes</h3>
                <p className="text-gray-400">Automatically generate personalized quizzes, assessments, and practice tests tailored to your learning style and comprehension level.</p>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardContent className="p-6 text-center">
                <Sparkles className="w-12 h-12 text-orange-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">3D Visualizations</h3>
                <p className="text-gray-400">Experience complex concepts through immersive 3D visualizations, interactive models, and cutting-edge augmented reality features.</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
