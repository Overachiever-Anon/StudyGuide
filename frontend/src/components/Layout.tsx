import { Link, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Toaster } from "@/components/ui/sonner";
import { Button } from "@/components/ui/button";
import { Sparkles, Menu, X } from "lucide-react";
import { useState } from "react";

const Layout = () => {
  const { isAuthenticated, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-neutral-900 via-neutral-800 to-neutral-900">
      <header className="bg-neutral-900/80 backdrop-blur-md border-b border-neutral-700/50 sticky top-0 z-50">
        <nav className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex-shrink-0">
              <Link to="/" className="flex items-center gap-2 text-2xl font-display font-bold bg-gradient-to-r from-primary-400 via-secondary-400 to-accent-400 bg-clip-text text-transparent hover:scale-105 transition-transform">
                <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg flex items-center justify-center shadow-glow">
                  <Sparkles className="w-5 h-5 text-white" />
                </div>
                EduForge
              </Link>
            </div>
            
            {/* Desktop Navigation */}
            <div className="hidden md:block">
              <div className="ml-10 flex items-center space-x-2">
                {isAuthenticated ? (
                  <>
                    <Link to="/dashboard">
                      <Button variant="ghost" size="sm" className="text-neutral-300 hover:text-white hover:bg-neutral-800">
                        Dashboard
                      </Button>
                    </Link>
                    <Button variant="outline" size="sm" onClick={logout} className="border-neutral-600 text-neutral-300 hover:text-white hover:bg-neutral-800 hover:border-neutral-500">
                      Logout
                    </Button>
                  </>
                ) : (
                  <>
                    <Link to="/login">
                      <Button variant="ghost" size="sm" className="text-neutral-300 hover:text-white hover:bg-neutral-800">
                        Login
                      </Button>
                    </Link>
                    <Link to="/register">
                      <Button size="sm" className="bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-400 hover:to-secondary-400 text-white shadow-glow hover:shadow-glow-purple">
                        Get Started
                      </Button>
                    </Link>
                  </>
                )}
              </div>
            </div>

            {/* Mobile menu button */}
            <div className="md:hidden">
              <Button
                variant="ghost"
                size="icon-sm"
                onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
                className="text-neutral-300 hover:text-white hover:bg-neutral-800"
              >
                {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
              </Button>
            </div>
          </div>

          {/* Mobile Navigation */}
          {mobileMenuOpen && (
            <div className="md:hidden border-t border-neutral-700/50 bg-neutral-900/95 backdrop-blur-md">
              <div className="px-2 pt-2 pb-3 space-y-1">
                {isAuthenticated ? (
                  <>
                    <Link to="/dashboard" className="block">
                      <Button variant="ghost" size="sm" className="w-full justify-start text-neutral-300 hover:text-white hover:bg-neutral-800">
                        Dashboard
                      </Button>
                    </Link>
                    <Button variant="outline" size="sm" className="w-full border-neutral-600 text-neutral-300 hover:text-white hover:bg-neutral-800 hover:border-neutral-500" onClick={logout}>
                      Logout
                    </Button>
                  </>
                ) : (
                  <>
                    <Link to="/login" className="block">
                      <Button variant="ghost" size="sm" className="w-full justify-start text-neutral-300 hover:text-white hover:bg-neutral-800">
                        Login
                      </Button>
                    </Link>
                    <Link to="/register" className="block">
                      <Button size="sm" className="w-full bg-gradient-to-r from-primary-500 to-secondary-500 hover:from-primary-400 hover:to-secondary-400 text-white shadow-glow">
                        Get Started
                      </Button>
                    </Link>
                  </>
                )}
              </div>
            </div>
          )}
        </nav>
      </header>
      <main className="flex-grow">
        <Outlet />
      </main>
      <Toaster />
    </div>
  );
};

export default Layout;
