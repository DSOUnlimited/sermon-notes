import React from 'react';
import html2pdf from 'html2pdf.js';

interface ExportNotesPDFProps {
  notesHtmlId?: string;
}

const ExportNotesPDF: React.FC<ExportNotesPDFProps> = ({ notesHtmlId = "notes-content" }) => {
  const handleExport = () => {
    const element = document.getElementById(notesHtmlId);
    if (!element) return;
    html2pdf()
      .set({
        margin: 0.5,
        filename: 'sermon-notes.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      })
      .from(element)
      .save();
  };

  return (
    <button
      onClick={handleExport}
      className="bg-indigo-600 hover:bg-indigo-700 text-white font-semibold px-4 py-2 rounded"
    >
      Download Notes as PDF
    </button>
  );
};

export default ExportNotesPDF; 