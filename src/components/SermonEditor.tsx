import React, { useState, useEffect } from 'react';
import { Editor } from '@tinymce/tinymce-react';
import axios from 'axios';
import { auth, db } from '../firebase/config';
import { signOut } from 'firebase/auth';
import { useNavigate, useParams } from 'react-router-dom';
import { collection, addDoc, serverTimestamp, doc, getDoc, updateDoc } from 'firebase/firestore';
import { useAuthState } from 'react-firebase-hooks/auth';

interface SermonData {
  title: string;
  date: string;
  preacher: string;
  scripture: string;
  notes: string;
}

const SCRIPTURE_REGEX = /([1-3]?\s?[A-Za-z]+)\s(\d{1,3}):(\d{1,3})(?:-(\d{1,3}))?/g;

// KJV Book Abbreviations mapping
const BOOK_ABBREVIATIONS: Record<string, string> = {
  'gen': 'Genesis', 'ex': 'Exodus', 'lev': 'Leviticus', 'num': 'Numbers', 'deut': 'Deuteronomy',
  'josh': 'Joshua', 'judg': 'Judges', 'rut': 'Ruth', '1sa': '1 Samuel', '2sa': '2 Samuel',
  '1ki': '1 Kings', '2ki': '2 Kings', '1ch': '1 Chronicles', '2ch': '2 Chronicles', 'ezr': 'Ezra',
  'neh': 'Nehemiah', 'est': 'Esther', 'job': 'Job', 'ps': 'Psalms', 'prov': 'Proverbs',
  'eccl': 'Ecclesiastes', 'song': 'Song of Solomon', 'isa': 'Isaiah', 'jer': 'Jeremiah',
  'lam': 'Lamentations', 'eze': 'Ezekiel', 'dan': 'Daniel', 'hos': 'Hosea', 'joel': 'Joel',
  'amos': 'Amos', 'obad': 'Obadiah', 'jon': 'Jonah', 'mic': 'Micah', 'nah': 'Nahum',
  'hab': 'Habakkuk', 'zep': 'Zephaniah', 'hag': 'Haggai', 'zec': 'Zechariah', 'mal': 'Malachi',
  'mt': 'Matthew', 'mk': 'Mark', 'lk': 'Luke', 'jn': 'John', 'acts': 'Acts', 'rom': 'Romans',
  '1co': '1 Corinthians', '2co': '2 Corinthians', 'gal': 'Galatians', 'eph': 'Ephesians',
  'php': 'Philippians', 'col': 'Colossians', '1th': '1 Thessalonians', '2th': '2 Thessalonians',
  '1ti': '1 Timothy', '2ti': '2 Timothy', 'tit': 'Titus', 'phm': 'Philemon', 'heb': 'Hebrews',
  'jas': 'James', '1pe': '1 Peter', '2pe': '2 Peter', '1jn': '1 John', '2jn': '2 John',
  '3jn': '3 John', 'jud': 'Jude', 'rev': 'Revelation',
};

function expandBookAbbreviation(ref: string): string {
  const match = ref.match(/^([1-3]?\s*\w+)\s+(\d{1,3}:\d{1,3}(?:-\d{1,3})?)/i);
  if (!match) return ref;
  let book = match[1].replace(/\s+/g, '').toLowerCase();
  let rest = match[2];
  let prefix = '';
  if (book.length > 2 && ['1','2','3'].includes(book[0])) {
    prefix = book[0] + ' ';
    book = book.substring(1);
  }
  const expanded = BOOK_ABBREVIATIONS[book] || match[1];
  const capitalized = (prefix + expanded)
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
  return `${capitalized} ${rest}`.trim();
}

const fetchVerse = async (reference: string) => {
  try {
    const response = await axios.get(`https://bible-api.com/${encodeURIComponent(reference)}?translation=kjv`);
    return response.data.text.trim();
  } catch (e) {
    console.error('Error fetching verse:', e);
    return null;
  }
};

function getTodayDateString() {
  const today = new Date();
  return today.toISOString().split('T')[0];
}

const SermonEditor: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const [user] = useAuthState(auth);
  const [sermonData, setSermonData] = useState<SermonData>({
    title: '',
    date: getTodayDateString(),
    preacher: '',
    scripture: '',
    notes: ''
  });
  const [scriptureVerse, setScriptureVerse] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');
  const [initializing, setInitializing] = useState<boolean>(!!id);

  // Load sermon if editing
  useEffect(() => {
    const fetchSermon = async () => {
      if (id) {
        setInitializing(true);
        try {
          const docRef = doc(db, 'sermons', id);
          const docSnap = await getDoc(docRef);
          if (docSnap.exists()) {
            const data = docSnap.data();
            setSermonData({
              title: data.title || '',
              date: data.date || '',
              preacher: data.preacher || '',
              scripture: data.scripture || '',
              notes: data.notes || ''
            });
          } else {
            setError('Sermon not found.');
          }
        } catch (err) {
          setError('Failed to load sermon.');
        } finally {
          setInitializing(false);
        }
      }
    };
    fetchSermon();
  }, [id]);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      navigate('/login');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  // Fetch verse when scripture reference changes
  useEffect(() => {
    const fetchScripture = async () => {
      if (!sermonData.scripture.trim()) {
        setScriptureVerse('');
        setError('');
        return;
      }

      setIsLoading(true);
      setError('');
      
      try {
        const refs = sermonData.scripture.split(';').map(ref => ref.trim()).filter(Boolean);
        if (refs.length === 0) {
          setScriptureVerse('');
          return;
        }

        const verses: string[] = [];
        for (const ref of refs) {
          const matches = [...ref.matchAll(SCRIPTURE_REGEX)];
          if (matches.length > 0) {
            for (const match of matches) {
              const fullRef = match[0];
              const verse = await fetchVerse(fullRef);
              if (verse) {
                verses.push(`<div style='margin-bottom:8px;'><span style='font-weight:bold;'>${fullRef}</span>: <span style='font-style:italic;font-weight:bold;font-size:90%;'>${verse}</span></div>`);
              } else {
                setError(`Could not fetch verse for ${fullRef}`);
              }
            }
          } else {
            setError(`Invalid scripture reference format: ${ref}`);
          }
        }
        setScriptureVerse(verses.join(''));
      } catch (err) {
        console.error('Error fetching scripture:', err);
        setError('Error fetching scripture verses. Please try again.');
      } finally {
        setIsLoading(false);
      }
    };
    fetchScripture();
  }, [sermonData.scripture]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setSermonData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleEditorChange = (content: string) => {
    setSermonData(prev => ({ ...prev, notes: content }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) {
      setError('You must be logged in to save notes.');
      return;
    }
    setIsLoading(true);
    setError('');
    try {
      if (id) {
        // Update existing sermon
        const docRef = doc(db, 'sermons', id);
        await updateDoc(docRef, {
          ...sermonData,
          uid: user.uid,
        });
      } else {
        // Create new sermon
        await addDoc(collection(db, 'sermons'), {
          ...sermonData,
          uid: user.uid,
          createdAt: serverTimestamp(),
        });
      }
      setIsLoading(false);
      navigate('/dashboard');
    } catch (err) {
      setIsLoading(false);
      setError('Failed to save sermon. Please try again.');
      console.error(err);
    }
  };

  // Detect mobile device
  const isMobile = typeof window !== 'undefined' && window.innerWidth <= 600;

  if (initializing) {
    return <div className="container py-5 text-center">Loading sermon...</div>;
  }

  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div className="w-100 px-4">
        <div className="d-flex justify-content-between align-items-center mb-4 position-relative">
          <div className="position-absolute" style={{ right: 0, display: 'flex', gap: '0.5rem' }}>
            <button 
              onClick={() => navigate('/dashboard')}
              className="btn btn-outline-primary me-2"
            >
              Dashboard
            </button>
            <button 
              onClick={handleLogout}
              className="btn btn-outline-danger"
            >
              Logout
            </button>
          </div>
          <div className="w-100 text-center">
            <h1 className="display-4 mb-0">Sermon Notes</h1>
          </div>
        </div>
        <form className="card p-4 shadow" onSubmit={handleSubmit}>
          <div className="row mb-3">
            <div className="col-md-6 mb-3 mb-md-0">
              <label htmlFor="title" className="form-label fs-5">Sermon Title</label>
              <input
                type="text"
                name="title"
                id="title"
                value={sermonData.title}
                onChange={handleChange}
                className="form-control form-control-lg"
                placeholder="Enter the sermon title"
                required
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="date" className="form-label fs-5">Date</label>
              <input
                type="date"
                name="date"
                id="date"
                value={sermonData.date}
                onChange={handleChange}
                className="form-control form-control-lg"
                required
              />
            </div>
          </div>
          <div className="row mb-3">
            <div className="col-md-6 mb-3 mb-md-0">
              <label htmlFor="preacher" className="form-label fs-5">Preacher</label>
              <input
                type="text"
                name="preacher"
                id="preacher"
                value={sermonData.preacher}
                onChange={handleChange}
                className="form-control form-control-lg"
                placeholder="Enter preacher's name"
                required
              />
            </div>
            <div className="col-md-6">
              <label htmlFor="scripture" className="form-label fs-5">Scripture Reference</label>
              <input
                type="text"
                name="scripture"
                id="scripture"
                value={sermonData.scripture}
                onChange={handleChange}
                className="form-control form-control-lg"
                placeholder="e.g., John 3:16 or John 3:16-18"
                required
              />
              {isLoading && (
                <div className="mt-2 text-muted">
                  <small>Loading verses...</small>
                </div>
              )}
              {error && (
                <div className="mt-2 text-danger">
                  <small>{error}</small>
                </div>
              )}
              {scriptureVerse && (
                <div 
                  className="mt-3 p-3 bg-light rounded"
                  dangerouslySetInnerHTML={{ __html: scriptureVerse }}
                />
              )}
            </div>
          </div>
          <div className="mb-3">
            <label className="form-label fs-5">Notes</label>
            <div className="border rounded bg-white editor-container w-full max-w-full">
              <Editor
                apiKey="dl0pifrwkq8bux7u2niz7gzyvioedfl1by2jhtacmuttvq1b"
                value={sermonData.notes}
                init={{
                  height: 400,
                  menubar: false,
                  plugins: isMobile
                    ? ['lists']
                    : [
                        'advlist', 'autolink', 'lists', 'link', 'charmap', 'preview',
                        'searchreplace', 'visualblocks', 'code', 'fullscreen',
                        'insertdatetime', 'media', 'table', 'help', 'wordcount',
                        'fontsize'
                      ],
                  toolbar: isMobile
                    ? 'bullist numlist'
                    : [
                        'undo redo | styles | fontfamily fontsize | bold italic underline | forecolor',
                        'alignleft aligncenter alignright | bullist numlist | removeformat'
                      ].join(' | '),
                  font_family_formats:
                    'Playfair Display=Playfair Display,serif;Roboto=Roboto,sans-serif;Montserrat=Montserrat,sans-serif;Lato=Lato,sans-serif;Poppins=Poppins,sans-serif;Merriweather=Merriweather,serif;Source Sans Pro=Source Sans Pro,sans-serif;Open Sans=Open Sans,sans-serif;PT Serif=PT Serif,serif;Ubuntu=Ubuntu,sans-serif;Caveat=Caveat,cursive;Bangers=Bangers,cursive;',
                  fontsize_formats: '8pt 10pt 12pt 14pt 16pt 18pt 24pt 36pt',
                  content_style:
                    "body { font-family:Helvetica,Arial,sans-serif; font-size:16px }" +
                    "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto=wght@400;700&family=Montserrat=wght@400;700&family=Lato=wght@400;700&family=Poppins=wght@400;700&family=Merriweather=wght@400;700&family=Source+Sans+Pro=wght@400;700&family=Open+Sans=wght@400;700&family=PT+Serif=wght@400;700&family=Ubuntu=wght@400;700&family=Caveat=wght@400;700&family=Bangers&display=swap');",
                  setup: (editor: any) => {
                    editor.on('keydown', async (e: KeyboardEvent) => {
                      if (e.key === ' ') {
                        const rng = editor.selection.getRng();
                        const node = rng.startContainer;
                        let textBefore = '';
                        if (node.nodeType === 3) {
                          textBefore = node.textContent?.substring(0, rng.startOffset) || '';
                        } else if (node.nodeType === 1 && rng.startOffset > 0) {
                          const child = node.childNodes[rng.startOffset - 1];
                          if (child && child.nodeType === 3) {
                            textBefore = child.textContent || '';
                          }
                        }
                        const matches = [...textBefore.matchAll(SCRIPTURE_REGEX)];
                        if (matches.length > 0) {
                          const lastMatch = matches[matches.length - 1];
                          const ref = lastMatch[0];
                          const expandedRef = expandBookAbbreviation(ref);
                          editor.setProgressState(true);
                          const verse = await fetchVerse(expandedRef);
                          editor.setProgressState(false);
                          if (verse) {
                            if (node.nodeType === 3) {
                              const matchIndex = lastMatch.index ?? 0;
                              const refText = `${expandedRef}: `;
                              const verseHtml = `<span style=\"font-weight:bold;font-style:italic;font-size:90%;\">${verse}</span> `;
                              const range = editor.dom.createRng();
                              range.setStart(node, matchIndex);
                              range.setEnd(node, matchIndex + ref.length);
                              editor.selection.setRng(range);
                              editor.insertContent(refText + verseHtml);
                              editor.execCommand('RemoveFormat');
                              editor.save();
                              editor.setDirty(true);
                            }
                          }
                        }
                      }
                    });
                  }
                }}
                onEditorChange={handleEditorChange}
              />
            </div>
          </div>
          <div className="text-end">
            <button type="submit" className="btn btn-primary btn-lg">
              Save Notes
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default SermonEditor; 