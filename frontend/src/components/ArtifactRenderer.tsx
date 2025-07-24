import React, { useState, useEffect, useRef, FC } from 'react';

// --- Icons ---
const Play: FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>);
const RefreshCw: FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><path d="M3 2v6h6"></path><path d="M21 12A9 9 0 0 0 6 5.3L3 8"></path><path d="M21 22v-6h-6"></path><path d="M3 12a9 9 0 0 0 15 6.7l3-2.7"></path></svg>);
const Code: FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><polyline points="16 18 22 12 16 6"></polyline><polyline points="8 6 2 12 8 18"></polyline></svg>);
const Maximize2: FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>);
const Minimize2: FC<React.SVGProps<SVGSVGElement>> = (props) => (<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" {...props}><polyline points="4 14 10 14 10 20"></polyline><polyline points="20 10 14 10 14 4"></polyline><line x1="14" y1="10" x2="21" y2="3"></line><line x1="10" y1="14" x2="3" y2="21"></line></svg>);

interface ArtifactRendererProps {
  reactCode: string;
  title?: string;
  type?: string;
  onError?: (message: string) => void;
}

const createSandboxedHTML = (code: string): [string, string | null] => {
  let cleanedCode = code.replace(/import\s+.*\s+from\s+['"].*['"];?/g, '');
  let componentName: string | null = null;

  const exportDefaultMatch = cleanedCode.match(/export\s+default\s+(?:function\s+|class\s+)?([A-Z]\w*)/);
  if (exportDefaultMatch && exportDefaultMatch[1]) {
    componentName = exportDefaultMatch[1];
  } else {
    const allComponents = [...cleanedCode.matchAll(/(?:const|function)\s+([A-Z]\w*)/g)];
    if (allComponents.length > 0) {
      componentName = allComponents[allComponents.length - 1][1];
    }
  }

  if (!componentName) {
    return ['', 'Konnte keine React-Hauptkomponente finden.'];
  }

  cleanedCode = cleanedCode.replace(/export\s+default/g, '').replace(/export\s/g, '');

  const fullComponentCode = `
    const { useState, useEffect, useReducer, useCallback, useMemo, useRef, useContext } = React;
    ${cleanedCode}
    const ComponentToRender = ${componentName};
    const container = document.getElementById('root');
    const root = ReactDOM.createRoot(container);
    root.render(React.createElement(ComponentToRender));
  `;

  const script = `
    try {
      const transformedCode = Babel.transform(${JSON.stringify(fullComponentCode)}, { presets: ['react'] }).code;
      const scriptEl = document.createElement('script');
      scriptEl.textContent = transformedCode;
      document.body.appendChild(scriptEl);
      window.parent.postMessage({ type: 'iframeSuccess' }, '*');
    } catch (e) {
      window.parent.postMessage({ type: 'iframeError', error: { message: e.message, stack: e.stack } }, '*');
    }
  `;

  return [`
    <html>
      <head>
        <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
        <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
        <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>body { margin: 0; background-color: transparent; color: #e2e8f0; font-family: sans-serif; }</style>
        <script>
          // Globale Error-Handler, die JEDEN Fehler fangen
          window.addEventListener('error', e => {
            const error = e.error || {};
            window.parent.postMessage({ type: 'iframeError', error: { message: error.message || 'Script error', stack: error.stack } }, '*'); 
          });
          window.addEventListener('unhandledrejection', e => { 
            const reason = e.reason || {};
            window.parent.postMessage({ type: 'iframeError', error: { message: reason.message || 'Unhandled rejection', stack: reason.stack } }, '*');
          });
        </script>
      </head>
      <body>
        <div id="root"></div>
        <script>
          // Pass the code to be transformed into a global variable
          window.fullComponentCode = ${JSON.stringify(fullComponentCode)};
        </script>
        <script>${script}</script>
      </body>
    </html>
  `, null];
};

const ArtifactRenderer: FC<ArtifactRendererProps> = ({ reactCode, title = 'Artifact', type = 'Interactive', onError }) => {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const [srcDoc, setSrcDoc] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCode, setShowCode] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [key, setKey] = useState(0); // State to force iframe re-creation

  useEffect(() => {
    setIsLoading(true);
    setError(null);
    const [htmlContent, errorMessage] = createSandboxedHTML(reactCode);
    if (errorMessage) {
      setError(errorMessage);
      if (onError) onError(errorMessage);
      setIsLoading(false);
    } else {
      setSrcDoc(htmlContent);
    }
  }, [reactCode, key]); // Re-run when key changes

  useEffect(() => {
    const handleIframeMessage = (event: MessageEvent) => {
      // Sicherheitscheck: Stellen Sie sicher, dass die Nachricht vom iframe stammt, den wir erwarten.
      if (!iframeRef.current || event.source !== iframeRef.current.contentWindow) return;
      
      const { type, error: errorData } = event.data;
      if (type === 'iframeSuccess') {
        setIsLoading(false);
        setError(null);
      } else if (type === 'iframeError') {
        const message = errorData?.message || 'Ein unbekannter Fehler ist im Artefakt aufgetreten.';
        setError(message);
        if (onError) onError(message);
        setIsLoading(false);
      }
    };

    window.addEventListener('message', handleIframeMessage);
    return () => window.removeEventListener('message', handleIframeMessage);
  }, [onError]);

  const refreshComponent = () => {
    // Ändern Sie den Key, um eine vollständige Neuerstellung zu erzwingen
    setKey(prevKey => prevKey + 1);
  };

  return (
    <div className={`bg-slate-800/50 rounded-lg border border-slate-700 overflow-hidden transition-all duration-300 flex flex-col h-full ${isFullscreen ? 'fixed inset-2 z-50 bg-slate-900' : 'relative'}`}>
      <div className="bg-slate-900/70 border-b border-slate-700 px-4 py-2 flex items-center justify-between flex-shrink-0">
        <div className="flex items-center gap-3">
          <Play className="w-5 h-5 text-emerald-400" />
          <span className="text-white font-semibold">{title}</span>
          <span className="px-2 py-0.5 bg-purple-500/20 text-purple-300 text-xs font-medium rounded-full border border-purple-500/30 capitalize">
            {type.replace(/_/g, ' ')}
          </span>
        </div>
        <div className="flex items-center gap-1">
          <button onClick={refreshComponent} title="Refresh" className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-md"><RefreshCw className="w-4 h-4" /></button>
          <button onClick={() => setShowCode(!showCode)} title="View Code" className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-md"><Code className="w-4 h-4" /></button>
          <button onClick={() => setIsFullscreen(!isFullscreen)} title={isFullscreen ? 'Exit Fullscreen' : 'Fullscreen'} className="p-2 text-slate-400 hover:text-white hover:bg-slate-700 rounded-md">
            {isFullscreen ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
          </button>
        </div>
      </div>

      {showCode && (
        <div className="bg-slate-900 p-4 border-b border-slate-700 flex-shrink-0 overflow-auto">
          <h4 className="text-white font-semibold mb-2">Quellcode</h4>
          <pre className="bg-slate-950 rounded-md p-3 overflow-auto max-h-80 text-sm text-slate-300"><code>{reactCode}</code></pre>
        </div>
      )}

      <div className="relative w-full flex-grow bg-slate-900">
        {isLoading && (
          <div className="absolute inset-0 bg-slate-800/80 flex items-center justify-center z-10 p-4">
            <div className="flex items-center gap-2 text-slate-300"><div className="animate-spin rounded-full h-5 w-5 border-b-2 border-purple-400"></div>Lade interaktive Komponente...</div>
          </div>
        )}
        {error && (
           <div className="absolute inset-0 bg-slate-800/80 flex items-center justify-center z-10 p-4">
              <div className="text-center text-red-400">
                <h3 className="font-bold mb-1">Render-Fehler</h3>
                <p className="text-sm text-slate-400">{error}</p>
              </div>
            </div>
        )}
        <iframe
          key={key} // Wichtig: Erzwingt die Neuerstellung des iframes beim Refresh
          ref={iframeRef}
          className={`w-full h-full border-0 ${isLoading || error ? 'opacity-0' : 'opacity-100'} transition-opacity`}
          sandbox="allow-scripts allow-same-origin" // allow-same-origin ist für die message-Kommunikation notwendig
          title={`Interactive Artifact: ${title}`}
          srcDoc={srcDoc}
        />
      </div>
    </div>
  );
};

export default ArtifactRenderer;
