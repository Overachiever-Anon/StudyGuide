import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, Sparkles, Trash2, Plus } from 'lucide-react';
import ArtifactRenderer from '../components/ArtifactRenderer';

interface Artifact {
  id: number;
  title: string;
  type: 'study_guide' | 'quiz' | 'visualization';
  created_at: string;
  metadata: any;
}

interface ArtifactDetail extends Artifact {
  react_code: string;
  updated_at: string;
}

const ArtifactsPage: React.FC = () => {
  const { lectureId } = useParams<{ lectureId: string }>();
  const navigate = useNavigate();
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);
  const [selectedArtifact, setSelectedArtifact] = useState<ArtifactDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (lectureId) {
      fetchArtifacts();
    }
  }, [lectureId]);

  const fetchArtifacts = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(`/api/artifacts/pdf/${lectureId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch artifacts');
      }

      const data = await response.json();
      setArtifacts(data.artifacts || []);
    } catch (err) {
      console.error('Error fetching artifacts:', err);
      setError('Failed to load artifacts. Please try again later.');
      setArtifacts([]);
    } finally {
      setIsLoading(false);
    }
  };

  const fetchArtifactDetail = async (artifactId: number) => {
    try {
      const response = await fetch(`/api/artifacts/${artifactId}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch artifact details');
      }

      const data = await response.json();
      setSelectedArtifact(data.artifact);
    } catch (err) {
      console.error('Error fetching artifact details:', err);
      setError('Failed to load artifact details. Please try again later.');
    }
  };

  const generateNewArtifacts = async () => {
    try {
      setIsGenerating(true);
      const response = await fetch('/api/artifacts/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify({
          pdf_id: lectureId,
          types: ['study_guide', 'quiz']
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate artifacts');
      }

      await response.json();
      
      // Refresh artifacts list
      await fetchArtifacts();
      
      // Show success message
      setError(null);
    } catch (err) {
      console.error('Error generating artifacts:', err);
      setError('Failed to generate artifacts. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const deleteArtifact = async (artifactId: number) => {
    if (!confirm('Are you sure you want to delete this artifact?')) return;

    try {
      const response = await fetch(`/api/artifacts/${artifactId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete artifact');
      }

      // Refresh artifacts list
      await fetchArtifacts();
      
      // Clear selected artifact if it was deleted
      if (selectedArtifact?.id === artifactId) {
        setSelectedArtifact(null);
      }
    } catch (err) {
      console.error('Error deleting artifact:', err);
      setError('Failed to delete artifact. Please try again.');
    }
  };

  const getArtifactIcon = (type: string) => {
    switch (type) {
      case 'study_guide':
        return '📚';
      case 'quiz':
        return '❓';
      case 'visualization':
        return '📊';
      default:
        return '✨';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900/20 to-blue-900/20">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate(-1)}
              className="p-2 text-gray-400 hover:text-white hover:bg-gray-700 rounded-lg transition-colors"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                Interactive Artifacts
              </h1>
              <p className="text-gray-400 mt-2">AI-generated study guides, quizzes, and interactive content</p>
            </div>
          </div>

          <button
            onClick={generateNewArtifacts}
            disabled={isGenerating}
            className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-3 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-colors flex items-center gap-2 disabled:opacity-50"
          >
            {isGenerating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent"></div>
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4" />
                Generate New Artifacts
              </>
            )}
          </button>
        </div>

        {error && (
          <div className="bg-red-600/20 border border-red-500/50 rounded-lg p-4 mb-6">
            <p className="text-red-300">{error}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Artifacts List */}
          <div className="lg:col-span-1">
            <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-6">
              <h2 className="text-xl font-bold text-white mb-4">Available Artifacts</h2>
              
              {isLoading ? (
                <div className="flex items-center justify-center py-8">
                  <div className="animate-spin rounded-full h-8 w-8 border-2 border-purple-500 border-t-transparent"></div>
                </div>
              ) : artifacts.length === 0 ? (
                <div className="text-center py-8">
                  <div className="text-4xl mb-4">✨</div>
                  <p className="text-gray-400 mb-4">No artifacts yet</p>
                  <button
                    onClick={generateNewArtifacts}
                    className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-4 py-2 rounded-lg hover:from-purple-700 hover:to-blue-700 transition-colors flex items-center gap-2 mx-auto"
                  >
                    <Plus className="w-4 h-4" />
                    Create First Artifact
                  </button>
                </div>
              ) : (
                <div className="space-y-3">
                  {artifacts.map((artifact) => (
                    <div
                      key={artifact.id}
                      className={`p-4 rounded-lg border transition-colors cursor-pointer ${
                        selectedArtifact?.id === artifact.id
                          ? 'bg-purple-600/20 border-purple-500/50'
                          : 'bg-gray-700/50 border-gray-600 hover:bg-gray-700'
                      }`}
                      onClick={() => fetchArtifactDetail(artifact.id)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center gap-2 mb-2">
                            <span className="text-lg">{getArtifactIcon(artifact.type)}</span>
                            <span className="text-white font-medium text-sm">{artifact.title}</span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="px-2 py-1 bg-gray-600 text-gray-300 text-xs rounded">
                              {artifact.type.replace('_', ' ')}
                            </span>
                            <span className="text-gray-400 text-xs">
                              {new Date(artifact.created_at).toLocaleDateString()}
                            </span>
                          </div>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            deleteArtifact(artifact.id);
                          }}
                          className="p-1 text-gray-400 hover:text-red-400 transition-colors"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Artifact Renderer */}
          <div className="lg:col-span-2">
            {selectedArtifact ? (
              <ArtifactRenderer
                reactCode={selectedArtifact.react_code}
                title={selectedArtifact.title}
                type={selectedArtifact.type}
                onError={(error) => setError(error)}
              />
            ) : (
              <div className="bg-gray-800/50 rounded-lg border border-gray-700 p-12 text-center">
                <div className="text-6xl mb-4">🎯</div>
                <h3 className="text-xl font-bold text-white mb-2">Select an Artifact</h3>
                <p className="text-gray-400">
                  Choose an artifact from the list to view its interactive content
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArtifactsPage;
