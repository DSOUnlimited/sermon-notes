import React from "react";
import ExportNotesPDF from "./components/ExportNotesPDF";

function App() {
  return (
    <div>
      <div id="notes-content">
        <h1>Test Notes</h1>
        <p>This is a test note. Add more content here to test multi-page export.</p>
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque euismod, nisi eu consectetur consectetur, nisl nisi consectetur nisi, eu consectetur nisl nisi euismod nisi.</p>
        <p>Page 2 content. Add more paragraphs to test multi-page PDF export.</p>
        <p>Page 3 content. Keep adding content to ensure the PDF spans multiple pages.</p>
      </div>
      <ExportNotesPDF notesHtmlId="notes-content" />
    </div>
  );
}

export default App;
