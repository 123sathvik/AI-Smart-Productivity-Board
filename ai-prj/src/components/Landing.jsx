// src/App.jsx
import React,{ useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Landing() {
  const [showSearch, setShowSearch] = useState(false);
  const navigate = useNavigate();

  

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-r from-purple-600 via-purple-500 to-blue-400 text-white">
      {/* Navbar */}
      <nav className="flex justify-between items-center px-8 py-4 bg-black bg-opacity-30">
        <h1 className="text-xl font-bold">Smart BOAE</h1>
        <div className="flex items-center space-x-6">
          <a href="#features" className="hover:text-gray-300">Features</a>
          <a href="#pricing" className="hover:text-gray-300">Pricing</a>
          <a href="#about" className="hover:text-gray-300">About</a>
          <a href="#contact" className="hover:text-gray-300">Contact</a>

          {/* Search */}
          {showSearch ? (
            <input
              type="text"
              placeholder="Search..."
              className="px-2 py-1 rounded-md text-white"
              autoFocus
              onBlur={() => setShowSearch(false)}
            />
          ) : (
            <button onClick={() => setShowSearch(true)}>🔍</button>
          )}

          <button onClick={()=>navigate("/board")}
          className="px-4 py-2 bg-purple-600 rounded-md hover:bg-purple-700">
            Get Started
          </button>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="flex flex-col items-center justify-center flex-1 text-center px-6 py-24">
        <h2 className="text-6xl font-extrabold mb-6 drop-shadow-lg">
          Build Something Amazing
        </h2>
        <p className="text-lg max-w-2xl mb-8 text-gray-200">
          Transform your ideas into reality with our cutting-edge platform.
          Join thousands of creators who are already building the future.
        </p>
        <div className="space-x-4">
          <button className="px-6 py-3 bg-purple-600 text-white rounded-lg shadow-md hover:bg-purple-700">
            Get Started →
          </button>
          <button className="px-6 py-3 bg-black bg-opacity-60 text-white rounded-lg shadow-md hover:bg-black">
            ▶ Demo
          </button>
        </div>
      </header>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-8 bg-gradient-to-r from-purple-700 to-blue-500">
        <h3 className="text-4xl font-bold text-center mb-12">Get in Touch</h3>
        <div className="grid md:grid-cols-2 gap-10 max-w-6xl mx-auto">
          {/* Contact Info */}
          <div className="p-8 bg-black bg-opacity-30 rounded-xl shadow-lg">
            <h4 className="text-xl font-semibold mb-4">Contact Information</h4>
            <p className="mb-2"><strong>Email:</strong> hello@company.com</p>
            <p className="mb-2"><strong>Phone:</strong> +1 (555) 123-4567</p>
            <p><strong>Address:</strong> 123 Business St, Suite 100, San Francisco, CA</p>
          </div>

          {/* Contact Form */}
          <div className="p-8 bg-black bg-opacity-30 rounded-xl shadow-lg">
            <h4 className="text-xl font-semibold mb-4">Send us a Message</h4>
            <form className="space-y-4">
              <div className="flex space-x-4">
                <input type="text" placeholder="First Name" className="w-1/2 p-2 rounded-md text-black" />
                <input type="text" placeholder="Last Name" className="w-1/2 p-2 rounded-md text-black" />
              </div>
              <input type="email" placeholder="Email" className="w-full p-2 rounded-md text-black" />
              <input type="text" placeholder="Subject" className="w-full p-2 rounded-md text-black" />
              <textarea placeholder="Message" className="w-full p-2 rounded-md text-black" rows="4"></textarea>
              <button className="w-full px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700">
                Send Message
              </button>
            </form>
          </div>
        </div>
      </section>
           
      {/* Footer */}
      <footer className="bg-black bg-opacity-40 text-center py-6 mt-8">
        <p>© 2025 Smart BOAE. All rights reserved.</p>
      </footer>
    </div>
  

  );
}
