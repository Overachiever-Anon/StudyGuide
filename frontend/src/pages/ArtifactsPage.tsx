// frontend/src/pages/ArtifactsPage.tsx

import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { FileText, PlusCircle, ArrowLeft, RefreshCw, Trash2, Play } from 'lucide-react';
import ArtifactRenderer from '@/components/ArtifactRenderer';

interface Artifact {
  id: string;
  title: string;
  type: string;
  content: string;
  created_at: string;
}

const ArtifactsPage: React.FC = () => {
  const { lectureId } = useParams<{ lectureId: string }>();
  const navigate = useNavigate();
  
  const [artifacts, setArtifacts] = useState<Artifact[]>([]);
  const [selectedArtifact, setSelectedArtifact] = useState<Artifact | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [isFetchingContent, setIsFetchingContent] = useState(false);

  const fetchArtifacts = async (): Promise<Artifact[] | undefined> => {
    if (!lectureId) return;
    
    setIsLoading(true);
    setError(null);

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/artifacts/pdf/${lectureId}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Fehler beim Abrufen der Artefakte');
      }

      const data = await response.json();
      const artifacts = data.artifacts || [];
      setArtifacts(artifacts);
      return artifacts;

    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unbekannter Fehler');
      setArtifacts([]);
      return undefined;
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateArtifact = async () => {
    if (!lectureId) return;
    
    setIsGenerating(true);
    try {
      const response = await fetch(`/api/artifacts/generate/${lectureId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
          'Content-Type': 'application/json'
        }
      });

      if (!response.ok) {
        throw new Error('Failed to generate artifact');
      }

      await fetchArtifacts();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate artifact');
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDeleteArtifact = async (artifactId: string) => {
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

      setArtifacts(prev => prev.filter(a => a.id !== artifactId));
      if (selectedArtifact?.id === artifactId) {
        setSelectedArtifact(null);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete artifact');
    }
  };

  const handleSelectArtifact = async (artifact: Artifact) => {
    if (selectedArtifact?.id === artifact.id) return;

    setIsFetchingContent(true);
    setError(null);
    try {
      const response = await fetch(`/api/artifacts/${artifact.id}`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      if (!response.ok) {
        throw new Error('Failed to fetch artifact content');
      }
      const fullArtifact = await response.json();
      setSelectedArtifact(fullArtifact.artifact);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load artifact content');
      setSelectedArtifact(null); 
    } finally {
      setIsFetchingContent(false);
    }
  };

  useEffect(() => {
    if (lectureId) {
      fetchArtifacts().then((initialArtifacts) => {
        if (initialArtifacts && initialArtifacts.length > 0) {
          handleSelectArtifact(initialArtifacts[0]);
        }
      });
    }
  }, [lectureId]);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100">
      <header className="bg-slate-800 border-b border-slate-700 px-6 py-4">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div className="flex items-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-md"
            >
              <ArrowLeft className="w-5 h-5" />
            </button>
            <h1 className="text-xl font-semibold text-white">Artefakte</h1>
          </div>
          <button
            onClick={handleGenerateArtifact}
            disabled={isGenerating}
            className="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-md transition-colors"
          >
            {isGenerating ? (
              <RefreshCw className="w-4 h-4 animate-spin" />
            ) : (
              <PlusCircle className="w-4 h-4" />
            )}
            Neues Artefakt generieren
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto p-6">
        {error && (
          <div className="mb-4 p-4 bg-red-900/20 border border-red-700 rounded-md text-red-300">
            {error}
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-120px)]">
          <aside className="lg:col-span-1 bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
            <div className="p-4 border-b border-slate-700">
              <h2 className="text-lg font-semibold text-white">Artefakt-Liste</h2>
              <p className="text-sm text-slate-400 mt-1">
                {isLoading ? 'Lade...' : `${artifacts.length} Artefakte gefunden`}
              </p>
            </div>
            
            <div className="overflow-y-auto h-[calc(100%-80px)]">
              {isLoading ? (
                <div className="p-8 text-center">
                  <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-2 text-slate-400" />
                  <p className="text-slate-400">Lade Artefakte...</p>
                </div>
              ) : artifacts.length === 0 ? (
                <div className="p-8 text-center">
                  <FileText className="w-12 h-12 mx-auto mb-4 text-slate-500" />
                  <p className="text-slate-400 mb-4">Keine Artefakte gefunden</p>
                  <button
                    onClick={handleGenerateArtifact}
                    disabled={isGenerating}
                    className="px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white rounded-md"
                  >
                    Erstes Artefakt generieren
                  </button>
                </div>
              ) : (
                <div className="p-2 space-y-2">
                  {artifacts.map((artifact) => (
                    <div
                      key={artifact.id}
                      className={`p-3 rounded-md cursor-pointer transition-colors ${
                        selectedArtifact?.id === artifact.id
                          ? 'bg-purple-600/20 border border-purple-600'
                          : 'hover:bg-slate-700 border border-transparent'
                      }`}
                      onClick={() => handleSelectArtifact(artifact)}
                    >
                      <div className="flex items-start justify-between">
                        <div>
                          <h3 className="font-medium text-white">{artifact.title}</h3>
                          <p className="text-sm text-slate-400 capitalize">{artifact.type.replace(/_/g, ' ')}</p>
                          <p className="text-xs text-slate-500 mt-1">
                            {new Date(artifact.created_at).toLocaleDateString('de-DE')}
                          </p>
                        </div>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            handleDeleteArtifact(artifact.id);
                          }}
                          className="p-1 text-slate-400 hover:text-red-400"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </aside>

          <main className="lg:col-span-2 bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
            {isFetchingContent ? (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <RefreshCw className="w-12 h-12 mx-auto mb-4 text-slate-600 animate-spin" />
                  <h3 className="text-lg font-semibold text-slate-300">Lade Artefakt-Inhalt...</h3>
                </div>
              </div>
            ) : selectedArtifact ? (
              <ArtifactRenderer
                key={selectedArtifact.id}
                reactCode={selectedArtifact.content}
                title={selectedArtifact.title}
                type={selectedArtifact.type}
                onError={(message) => setError(message)}
              />
            ) : (
              <div className="flex items-center justify-center h-full">
                <div className="text-center">
                  <Play className="w-16 h-16 mx-auto mb-4 text-slate-600" />
                  <h3 className="text-lg font-semibold text-slate-300 mb-2">Kein Artefakt ausgewählt</h3>
                  <p className="text-slate-400">Wählen Sie ein Artefakt aus der Liste oder generieren Sie ein neues.</p>
                </div>
              </div>
            )}
          </main>
        </div>
      </main>
    </div>
  );
};

export default ArtifactsPage;
