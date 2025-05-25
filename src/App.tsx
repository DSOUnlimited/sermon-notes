import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from './firebase/config';
import SermonEditor from './components/SermonEditor';
import SermonEditorTest from './components/SermonEditorTest';
import Login from './components/Login';
import Dashboard from './components/Dashboard';

function App() {
  const [user, loading] = useAuthState(auth);
  const isDevelopment = import.meta.env.DEV;

  if (loading) {
    return (
      <div className="min-h-screen d-flex align-items-center justify-content-center">
        <div className="spinner-border text-primary" role="status">
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Routes>
          <Route 
            path="/" 
            element={user ? <Navigate to="/dashboard" /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/login" 
            element={!user ? <Login /> : <Navigate to="/dashboard" />} 
          />
          <Route 
            path="/dashboard" 
            element={user ? <Dashboard /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/editor" 
            element={user ? <SermonEditor /> : <Navigate to="/login" />} 
          />
          <Route 
            path="/editor/:id" 
            element={user ? <SermonEditor /> : <Navigate to="/login" />} 
          />
          {isDevelopment && (
            <Route 
              path="/editor-test" 
              element={user ? <SermonEditorTest /> : <Navigate to="/login" />} 
            />
          )}
        </Routes>
      </div>
    </Router>
  );
}

export default App;
