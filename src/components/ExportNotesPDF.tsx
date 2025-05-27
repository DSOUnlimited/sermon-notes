import React from 'react';

interface ExportNotesPDFProps {
  notesHtmlId?: string;
}

const ExportNotesPDF: React.FC<ExportNotesPDFProps> = ({ notesHtmlId = "notes-content" }) => {
  const handleExport = async () => {
    if (typeof window === "undefined") return; // Only run in browser

    const element = document.getElementById(notesHtmlId);
    if (!element) return;

    // Dynamically import html2pdf.js only on the client
    const html2pdf = (await import('html2pdf.js')).default;

    // Clone the element to avoid modifying the DOM
    const clone = element.cloneNode(true) as HTMLElement;

    // Replace all &nbsp; and Unicode non-breaking spaces with a real space
    let html = clone.innerHTML.replace(/&nbsp;/gi, ' ').replace(/\u00A0/g, ' ');

    // Decode any other HTML entities
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = html;
    clone.innerHTML = tempDiv.textContent || tempDiv.innerText || '';

    html2pdf()
      .set({
        margin: 0.5,
        filename: 'sermon-notes.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'in', format: 'letter', orientation: 'portrait' }
      })
      .from(clone)
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