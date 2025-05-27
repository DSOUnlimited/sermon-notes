import React from 'react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col">
      {/* Hero Section */}
      <header className="flex-1 flex flex-col justify-center items-center text-center px-4 py-16">
        <h1 className="text-5xl md:text-6xl font-extrabold text-indigo-700 mb-4 drop-shadow-lg">
          SermonNotes
        </h1>
        <p className="text-xl md:text-2xl text-gray-700 mb-8 max-w-2xl">
          Take, organize, and sync your sermon notes across all your devices. Simple. Secure. Powerful.
        </p>
        <a
          href="/login"
          className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3 rounded-lg shadow-lg transition"
        >
          Get Started
        </a>
      </header>

      {/* Features Section */}
      <section className="py-12 bg-white shadow-inner">
        <div className="max-w-5xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-center text-indigo-700 mb-10">Features</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-indigo-50 p-6 rounded-lg shadow text-center">
              <div className="text-4xl mb-4">📝</div>
              <h3 className="font-semibold text-lg mb-2">Rich Note Taking</h3>
              <p className="text-gray-600">Write, edit, and format your sermon notes with ease. Attach files and images for deeper study.</p>
            </div>
            <div className="bg-indigo-50 p-6 rounded-lg shadow text-center">
              <div className="text-4xl mb-4">🔄</div>
              <h3 className="font-semibold text-lg mb-2">Sync Across Devices</h3>
              <p className="text-gray-600">Access your notes from web or mobile. Everything stays in sync, always.</p>
            </div>
            <div className="bg-indigo-50 p-6 rounded-lg shadow text-center">
              <div className="text-4xl mb-4">🔒</div>
              <h3 className="font-semibold text-lg mb-2">Secure & Private</h3>
              <p className="text-gray-600">Your notes are safe and private. Only you can access your content.</p>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <footer className="py-10 text-center">
        <h3 className="text-2xl font-bold text-indigo-700 mb-4">Ready to get started?</h3>
        <a
          href="/login"
          className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-8 py-3 rounded-lg shadow-lg transition"
        >
          Create Your Free Account
        </a>
        <p className="mt-6 text-gray-500 text-sm">&copy; {new Date().getFullYear()} SermonNotes. All rights reserved.</p>
      </footer>
    </div>
  );
} 