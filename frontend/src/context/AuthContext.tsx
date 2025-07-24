import { createContext, useState, useContext, ReactNode, useEffect } from 'react';

interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  login: (token: string) => void;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    console.log('AuthProvider: Initializing, checking localStorage...');
    try {
      const storedToken = localStorage.getItem('token');
      console.log('AuthProvider: Raw stored token:', storedToken);
      
      // Validate token - must be a non-empty string and not 'null' or 'undefined'
      if (storedToken && storedToken !== 'null' && storedToken !== 'undefined' && storedToken.trim().length > 0) {
        console.log('AuthProvider: Valid token found, setting:', storedToken.substring(0, 10) + '...');
        setToken(storedToken);
      } else {
        console.log('AuthProvider: Invalid token found, clearing localStorage');
        localStorage.removeItem('token');
        setToken(null);
      }
    } finally {
      setLoading(false);
      console.log('AuthProvider: Loading complete');
    }
  }, []);

  const login = (newToken: string) => {
    console.log('AuthProvider: Login called with token:', newToken ? (newToken.substring(0, 10) + '...') : 'UNDEFINED/NULL');
    if (newToken && newToken.trim().length > 0) {
      localStorage.setItem('token', newToken);
      setToken(newToken);
      console.log('AuthProvider: Login successful, token set');
    } else {
      console.error('AuthProvider: Login failed - invalid token received');
    }
  };

  const logout = () => {
    console.log('AuthProvider: Logout called');
    localStorage.removeItem('token');
    setToken(null);
  };

  const isAuthenticated = !!token;
  console.log('AuthProvider: Current state - token:', token ? 'EXISTS' : 'NULL', 'isAuthenticated:', isAuthenticated, 'loading:', loading);

  return (
    <AuthContext.Provider value={{ isAuthenticated, token, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
