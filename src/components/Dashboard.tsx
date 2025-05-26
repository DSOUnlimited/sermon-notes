import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { collection, query, where, getDocs, doc, getDoc, updateDoc, serverTimestamp } from 'firebase/firestore';
import { auth, db } from '../firebase/config';
import { signOut } from 'firebase/auth';
import { useAuthState } from 'react-firebase-hooks/auth';
import jsPDF from 'jspdf';
import 'jspdf-autotable';

interface SermonData {
  id: string;
  title: string;
  date: string;
  preacher: string;
  scripture: string;
  notes: string;
  createdAt?: { seconds: number };
  deleted: boolean;
}

const Dashboard: React.FC = () => {
  const [user] = useAuthState(auth);
  const [sermons, setSermons] = useState<SermonData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return;
    const fetchSermons = async () => {
      setLoading(true);
      setError('');
      try {
        const q = query(
          collection(db, 'sermons'),
          where('uid', '==', user.uid)
        );
        const querySnapshot = await getDocs(q);
        let data: SermonData[] = querySnapshot.docs.map(doc => ({ id: doc.id, ...doc.data() } as SermonData));
        // Sort by createdAt if present, otherwise by title
        data = data.sort((a, b) => {
          if (a.createdAt && b.createdAt) {
            return (b.createdAt?.seconds || 0) - (a.createdAt?.seconds || 0);
          }
          return a.title.localeCompare(b.title);
        });
        setSermons(data);
      } catch (err) {
        setError('Failed to load sermons.');
      } finally {
        setLoading(false);
      }
    };
    fetchSermons();
  }, [user]);

  const handleLogout = async () => {
    await signOut(auth);
    navigate('/login');
  };

  const handleNewSermon = () => {
    navigate('/editor');
  };

  const handleEditSermon = (id: string) => {
    navigate(`/editor/${id}`);
  };

  const handleTestEnvironment = () => {
    navigate('/editor-test');
  };

  const handlePrint = async (sermonId: string) => {
    const docRef = doc(db, 'sermons', sermonId);
    const docSnap = await getDoc(docRef);
    if (!docSnap.exists()) return;
    const data = docSnap.data();
    const printWindow = window.open('', '_blank');
    if (!printWindow) return;
    printWindow.document.write(`
      <html><head><title>Print Sermon</title>
      <style>
        body { font-family: Arial, sans-serif; margin: 2em; }
        h1 { font-size: 2em; margin-bottom: 0.2em; }
        .meta { margin-bottom: 1em; color: #555; }
        .section { margin-bottom: 1.5em; }
        .label { font-weight: bold; }
        .notes { border: 1px solid #ccc; padding: 1em; border-radius: 6px; background: #fafafa; }
      </style>
      </head><body>
        <h1>${data.title || ''}</h1>
        <div class="meta">
          <span class="label">Date:</span> ${data.date || ''}<br/>
          <span class="label">Preacher:</span> ${data.preacher || ''}<br/>
          <span class="label">Scripture:</span> ${data.scripture || ''}
        </div>
        <div class="section notes">${data.notes || ''}</div>
        <script>window.onload = function() { window.print(); }<\/script>
      </body></html>
    `);
    printWindow.document.close();
  };

  const handleDownloadPDF = async (sermonId: string) => {
    const docRef = doc(db, 'sermons', sermonId);
    const docSnap = await getDoc(docRef);
    if (!docSnap.exists()) return;
    const data = docSnap.data();
    const docPdf = new jsPDF();
    docPdf.setFont('helvetica');
    docPdf.setFontSize(18);
    docPdf.text(data.title || '', 10, 20);
    docPdf.setFontSize(12);
    docPdf.text(`Date: ${data.date || ''}`, 10, 30);
    docPdf.text(`Preacher: ${data.preacher || ''}`, 10, 38);
    docPdf.text(`Scripture: ${data.scripture || ''}`, 10, 46);
    docPdf.setFontSize(12);
    docPdf.text('Notes:', 10, 58);
    docPdf.setFontSize(11);
    // Remove HTML tags from notes
    const notesText = (data.notes || '').replace(/<[^>]+>/g, '');
    const pageHeight = docPdf.internal.pageSize.getHeight();
    const margin = 10;
    let y = 66;
    const lineHeight = 7;
    const lines = docPdf.splitTextToSize(notesText, 190);
    lines.forEach((line: string) => {
      if (y + lineHeight > pageHeight - margin) {
        docPdf.addPage();
        y = margin + 10;
      }
      docPdf.text(line, 10, y);
      y += lineHeight;
    });
    docPdf.save(`${data.title || 'sermon'}.pdf`);
  };

  const handleDelete = async (sermonId: string) => {
    if (!window.confirm('Are you sure you want to delete this sermon? This action cannot be undone.')) return;
    try {
      await updateDoc(doc(db, 'sermons', sermonId), {
        deleted: true,
        deletedAt: serverTimestamp(),
      });
      setSermons(prev => prev.map(s => s.id === sermonId ? { ...s, deleted: true } : s));
    } catch (err) {
      alert('Failed to delete sermon. Please try again.');
    }
  };

  const handleRecover = async (sermonId: string) => {
    try {
      await updateDoc(doc(db, 'sermons', sermonId), { deleted: false });
      setSermons(prev => prev.map(s => s.id === sermonId ? { ...s, deleted: false } : s));
    } catch (err) {
      alert('Failed to recover sermon. Please try again.');
    }
  };

  if (!user) return <div>Loading...</div>;

  // Main (non-deleted) sermons
  const activeSermons = sermons.filter(s => !s.deleted);
  // Deleted sermons
  const deletedSermons = sermons.filter(s => s.deleted);

  return (
    <div className="container py-3 px-1 px-sm-3">
      <div className="d-flex flex-column flex-sm-row justify-content-between align-items-center mb-4 gap-2">
        <h1 className="display-6 mb-0 text-center w-100 w-sm-auto">Your Sermons</h1>
        <button className="btn btn-outline-danger w-100 w-sm-auto" onClick={handleLogout}>Logout</button>
      </div>
      <div className="d-flex flex-column flex-sm-row gap-2 mb-4">
        <button className="btn btn-primary w-100 w-sm-auto" onClick={handleNewSermon}>+ New Sermon</button>
        {import.meta.env.DEV && (
          <button className="btn btn-warning w-100 w-sm-auto" onClick={handleTestEnvironment}>
            Test Environment
          </button>
        )}
      </div>
      {loading ? (
        <div>Loading sermons...</div>
      ) : error ? (
        <div className="text-danger">{error}</div>
      ) : activeSermons.length === 0 ? (
        <div>No sermons found. Click "+ New Sermon" to get started!</div>
      ) : (
        <div className="row g-3">
          {activeSermons.map(sermon => (
            <div key={sermon.id} className="col-12 col-sm-6 col-md-4 col-lg-3">
              <div
                className="card h-100 shadow-sm sermon-tile p-2 p-sm-3"
                style={{ cursor: 'pointer' }}
                onClick={() => handleEditSermon(sermon.id)}
              >
                <div className="card-body d-flex flex-column justify-content-between p-2 p-sm-3">
                  <div>
                    <h5 className="card-title mb-2 text-break">{sermon.title}</h5>
                    <div className="card-subtitle mb-2 text-muted small text-break">{sermon.date} &mdash; {sermon.preacher}</div>
                  </div>
                  <div className="mt-2 text-truncate text-break" style={{ fontSize: '0.95em', color: '#555' }}>
                    {sermon.scripture}
                  </div>
                  <div className="mt-3 d-flex flex-column flex-sm-row gap-2">
                    <button className="btn btn-outline-secondary btn-sm w-100 w-sm-auto" onClick={e => { e.stopPropagation(); handlePrint(sermon.id); }}>Print</button>
                    <button className="btn btn-outline-secondary btn-sm w-100 w-sm-auto" onClick={e => { e.stopPropagation(); handleDownloadPDF(sermon.id); }}>Download PDF</button>
                    <button className="btn btn-outline-danger btn-sm w-100 w-sm-auto" onClick={e => { e.stopPropagation(); handleDelete(sermon.id); }}>Delete</button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Recently Deleted Section */}
      {deletedSermons.length > 0 && (
        <div className="mt-5">
          <h5>Recently Deleted</h5>
          <div className="mb-2 text-danger small">
            Deleted sermons will be permanently deleted after 7 days.
          </div>
          <div className="row g-3">
            {deletedSermons.map(sermon => (
              <div key={sermon.id} className="col-12 col-sm-6 col-md-4 col-lg-3">
                <div className="card h-100 shadow-sm bg-light p-2 p-sm-3">
                  <div className="card-body d-flex flex-column justify-content-between p-2 p-sm-3">
                    <div>
                      <h5 className="card-title mb-2 text-break">{sermon.title}</h5>
                      <div className="card-subtitle mb-2 text-muted small text-break">{sermon.date} &mdash; {sermon.preacher}</div>
                    </div>
                    <div className="mt-2 text-truncate text-break" style={{ fontSize: '0.95em', color: '#555' }}>
                      {sermon.scripture}
                    </div>
                    <div className="mt-3 d-flex flex-column flex-sm-row gap-2">
                      <button className="btn btn-outline-success btn-sm w-100 w-sm-auto" onClick={e => { e.stopPropagation(); handleRecover(sermon.id); }}>Recover</button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard; 