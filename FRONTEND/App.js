import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import PromptEditor from './components/PromptEditor';
import VersionHistory from './components/VersionHistory';
import PromptEvaluation from './components/PromptEvaluation';
import Navbar from './components/Navbar';

const App = () => {
  return (
    <Router>
      <Navbar />
      <div id="root">
        <h1>Welcome to PromptCraft</h1>
        <p>Your go-to toolkit for optimizing and version-controlling prompts for code generation, debugging, and technical documentation.</p>
        <button className="btn">Get Started</button>

        {/* Key Features Section */}
        <section className="section">
          <h2>Key Features</h2>
          <div className="feature-cards-container">
            <div className="feature-card">
              <h3>Version Control</h3>
              <p>Efficiently manage and version control your prompts to keep track of changes over time.</p>
            </div>
            <div className="feature-card">
              <h3>Optimized Prompts</h3>
              <p>Enhance your prompts for improved responses from AI models like GPT-3 and others.</p>
            </div>
            <div className="feature-card">
              <h3>Cross-Platform Support</h3>
              <p>Use our toolkit across platforms to easily integrate and enhance your development workflows.</p>
            </div>
          </div>
        </section>

        <Switch>
          <Route path="/editor" component={PromptEditor} />
          <Route path="/history" component={VersionHistory} />
          <Route path="/evaluate" component={PromptEvaluation} />
        </Switch>
      </div>
    </Router>
  );
};
export default App;