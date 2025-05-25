import React, { useState } from 'react';
import { Editor } from '@tinymce/tinymce-react';
import axios from 'axios';

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
  'gen': 'Genesis',
  'ex': 'Exodus',
  'lev': 'Leviticus',
  'num': 'Numbers',
  'deut': 'Deuteronomy',
  'josh': 'Joshua',
  'judg': 'Judges',
  'rut': 'Ruth',
  '1sa': '1 Samuel',
  '2sa': '2 Samuel',
  '1ki': '1 Kings',
  '2ki': '2 Kings',
  '1ch': '1 Chronicles',
  '2ch': '2 Chronicles',
  'ezr': 'Ezra',
  'neh': 'Nehemiah',
  'est': 'Esther',
  'job': 'Job',
  'ps': 'Psalms',
  'prov': 'Proverbs',
  'eccl': 'Ecclesiastes',
  'song': 'Song of Solomon',
  'isa': 'Isaiah',
  'jer': 'Jeremiah',
  'lam': 'Lamentations',
  'eze': 'Ezekiel',
  'dan': 'Daniel',
  'hos': 'Hosea',
  'joel': 'Joel',
  'amos': 'Amos',
  'obad': 'Obadiah',
  'jon': 'Jonah',
  'mic': 'Micah',
  'nah': 'Nahum',
  'hab': 'Habakkuk',
  'zep': 'Zephaniah',
  'hag': 'Haggai',
  'zec': 'Zechariah',
  'mal': 'Malachi',
  'mt': 'Matthew',
  'mk': 'Mark',
  'lk': 'Luke',
  'jn': 'John',
  'acts': 'Acts',
  'rom': 'Romans',
  '1co': '1 Corinthians',
  '2co': '2 Corinthians',
  'gal': 'Galatians',
  'eph': 'Ephesians',
  'php': 'Philippians',
  'col': 'Colossians',
  '1th': '1 Thessalonians',
  '2th': '2 Thessalonians',
  '1ti': '1 Timothy',
  '2ti': '2 Timothy',
  'tit': 'Titus',
  'phm': 'Philemon',
  'heb': 'Hebrews',
  'jas': 'James',
  '1pe': '1 Peter',
  '2pe': '2 Peter',
  '1jn': '1 John',
  '2jn': '2 John',
  '3jn': '3 John',
  'jud': 'Jude',
  'rev': 'Revelation',
};

function getTodayDateString() {
  const today = new Date();
  return today.toISOString().split('T')[0];
}

function expandBookAbbreviation(ref: string): string {
  // Try to match the book part and expand it
  // e.g., "Jn 3:16" => "John 3:16"
  const match = ref.match(/^([1-3]?\s*\w+)\s+(\d{1,3}:\d{1,3}(?:-\d{1,3})?)/i);
  if (!match) return ref;
  let book = match[1].replace(/\s+/g, '').toLowerCase();
  let rest = match[2];
  // Handle 1/2/3 prefix (e.g., 1co, 2ti)
  let prefix = '';
  if (book.length > 2 && ['1','2','3'].includes(book[0])) {
    prefix = book[0] + ' ';
    book = book.substring(1);
  }
  const expanded = BOOK_ABBREVIATIONS[book] || match[1];
  // Capitalize each word in the book name
  const capitalized = (prefix + expanded)
    .split(' ')
    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
    .join(' ');
  return `${capitalized} ${rest}`.trim();
}

const SermonEditorTest: React.FC = () => {
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
  const [debugInfo, setDebugInfo] = useState<string>('');
  const [editorState, setEditorState] = useState<{
    isInitialized: boolean;
    lastAction: string;
    contentHistory: string[];
  }>({
    isInitialized: false,
    lastAction: '',
    contentHistory: []
  });

  const fetchVerse = async (reference: string) => {
    try {
      setDebugInfo((prev: string) => `${prev}\nFetching verse for: ${reference}`);
      const response = await axios.get(`https://bible-api.com/${encodeURIComponent(reference)}?translation=kjv`);
      setDebugInfo((prev: string) => `${prev}\nVerse fetched successfully: ${response.data.text.trim().substring(0, 50)}...`);
      return response.data.text.trim();
    } catch (e: unknown) {
      console.error('Error fetching verse:', e);
      const errorMessage = e instanceof Error ? e.message : 'Unknown error occurred';
      setDebugInfo((prev: string) => `${prev}\nError fetching verse: ${errorMessage}`);
      return null;
    }
  };

  // Debug: log scripture value on every render
  React.useEffect(() => {
    setDebugInfo(prev => `${prev}\n[RENDER] Current scripture value: "${sermonData.scripture}"`);
  }, [sermonData.scripture]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    console.log('[handleChange] name:', name, 'value:', value); // DEBUG
    setSermonData(prev => ({
      ...prev,
      [name]: value
    }));
    setEditorState(prev => ({
      ...prev,
      lastAction: `Field "${name}" updated to: ${value}`
    }));
    
    // Add debug info for scripture input
    if (name === 'scripture') {
      setDebugInfo(prev => `${prev}\n[handleChange] Scripture input changed to: "${value}"`);
      const matches = [...value.matchAll(SCRIPTURE_REGEX)];
      setDebugInfo(prev => `${prev}\n[handleChange] Regex matches found: ${matches.length}`);
      if (matches.length > 0) {
        setDebugInfo(prev => `${prev}\n[handleChange] Matches: ${matches.map(m => m[0]).join(', ')}`);
      }
    }
  };

  const handleEditorChange = (content: string) => {
    setSermonData(prev => ({ ...prev, notes: content }));
    setEditorState(prev => ({
      ...prev,
      lastAction: `Content updated (${content.length} characters)`,
      contentHistory: [...prev.contentHistory.slice(-4), content]
    }));
    setDebugInfo(prev => `${prev}\nContent length: ${content.length} characters`);
  };

  const handleEditorInit = (evt: any, editor: any) => {
    setEditorState(prev => ({
      ...prev,
      isInitialized: true,
      lastAction: 'Editor initialized'
    }));
    setDebugInfo(prev => `${prev}\nEditor initialized successfully`);
  };

  // Fetch verse when scripture reference changes
  React.useEffect(() => {
    const fetchScripture = async () => {
      const currentScripture = sermonData.scripture.trim();
      setDebugInfo(prev => `${prev}\nScripture effect triggered with: "${currentScripture}"`);
      
      if (!currentScripture) {
        setScriptureVerse('');
        setError('');
        setDebugInfo(prev => `${prev}\nNo scripture reference provided`);
        return;
      }

      setIsLoading(true);
      setError('');
      setDebugInfo(prev => `${prev}\nProcessing scripture reference: ${currentScripture}`);
      
      try {
        const refs = currentScripture.split(';').map(ref => ref.trim()).filter(Boolean);
        setDebugInfo(prev => `${prev}\nSplit references: ${refs.join(', ')}`);
        
        if (refs.length === 0) {
          setScriptureVerse('');
          setDebugInfo(prev => `${prev}\nNo valid references found after splitting`);
          return;
        }

        setDebugInfo(prev => `${prev}\nFound ${refs.length} references to process`);
        const verses: string[] = [];
        for (const ref of refs) {
          const matches = [...ref.matchAll(SCRIPTURE_REGEX)];
          setDebugInfo(prev => `${prev}\nProcessing reference: "${ref}"`);
          setDebugInfo(prev => `${prev}\nFound ${matches.length} matches for "${ref}"`);
          
          if (matches.length > 0) {
            for (const match of matches) {
              const fullRef = match[0];
              setDebugInfo(prev => `${prev}\nFetching verse for match: "${fullRef}"`);
              const verse = await fetchVerse(fullRef);
              if (verse) {
                verses.push(`<div style='margin-bottom:8px;'><span style='font-weight:bold;'>${fullRef}</span>: <span style='font-style:italic;font-weight:bold;font-size:90%;'>${verse}</span></div>`);
                setDebugInfo(prev => `${prev}\nSuccessfully added verse for "${fullRef}"`);
              } else {
                setError(`Could not fetch verse for ${fullRef}`);
                setDebugInfo(prev => `${prev}\nFailed to fetch verse for "${fullRef}"`);
              }
            }
          } else {
            setError(`Invalid scripture reference format: ${ref}`);
            setDebugInfo(prev => `${prev}\nInvalid reference format: "${ref}"`);
          }
        }
        setScriptureVerse(verses.join(''));
        setDebugInfo(prev => `${prev}\nFinished processing all references`);
      } catch (err: unknown) {
        console.error('Error fetching scripture:', err);
        const errorMessage = err instanceof Error ? err.message : 'Unknown error occurred';
        setError('Error fetching scripture verses. Please try again.');
        setDebugInfo(prev => `${prev}\nError in scripture processing: ${errorMessage}`);
      } finally {
        setIsLoading(false);
      }
    };
    fetchScripture();
  }, [sermonData.scripture]);

  return (
    <div className="container-fluid min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div className="w-100 px-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <div>
            <h1 className="display-4 mb-0 text-warning">Sermon Notes (Test Environment)</h1>
            <div className="text-muted">Development Mode - Changes here won't affect production</div>
          </div>
          <div className="badge bg-warning text-dark p-2">
            TEST ENVIRONMENT
          </div>
        </div>
        <div className="card p-4 shadow border-warning">
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
                  plugins: [
                    'advlist', 'autolink', 'lists', 'link', 'charmap', 'preview',
                    'searchreplace', 'visualblocks', 'code', 'fullscreen',
                    'insertdatetime', 'media', 'table', 'help', 'wordcount',
                    'fontsize'
                  ],
                  toolbar: [
                    'undo redo | fontfamily fontsize | bold italic underline | forecolor',
                    'alignleft aligncenter alignright | bullist numlist | removeformat'
                  ].join(' | '),
                  font_family_formats:
                    'Playfair Display=Playfair Display,serif;Roboto=Roboto,sans-serif;Montserrat=Montserrat,sans-serif;Lato=Lato,sans-serif;Poppins=Poppins,sans-serif;Merriweather=Merriweather,serif;Source Sans Pro=Source Sans Pro,sans-serif;Open Sans=Open Sans,sans-serif;PT Serif=PT Serif,serif;Ubuntu=Ubuntu,sans-serif;Caveat=Caveat,cursive;Bangers=Bangers,cursive;',
                  fontsize_formats: '8pt 10pt 12pt 14pt 16pt 18pt 24pt 36pt',
                  content_style:
                    "body { font-family:Helvetica,Arial,sans-serif; font-size:16px }" +
                    "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Roboto=wght@400;700&family=Montserrat=wght@400;700&family=Lato=wght@400;700&family=Poppins=wght@400;700&family=Merriweather=wght@400;700&family=Source+Sans+Pro=wght@400;700&family=Open+Sans=wght@400;700&family=PT+Serif=wght@400;700&family=Ubuntu=wght@400;700&family=Caveat=wght@400;700&family=Bangers&display=swap');"
                }}
                onEditorChange={handleEditorChange}
                onInit={handleEditorInit}
              />
            </div>
          </div>
          {/* Enhanced Debug Information Panel */}
          <div className="mt-3">
            <div className="card border-warning">
              <div className="card-header bg-warning text-dark">
                <h5 className="mb-0">Debug Information</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-6">
                    <h6>Editor State</h6>
                    <ul className="list-unstyled">
                      <li>Initialized: {editorState.isInitialized ? '✅' : '❌'}</li>
                      <li>Last Action: {editorState.lastAction}</li>
                      <li>Content Length: {sermonData.notes.length} characters</li>
                    </ul>
                  </div>
                  <div className="col-md-6">
                    <h6>Content History</h6>
                    <div className="small text-muted">
                      {editorState.contentHistory.map((content, index) => (
                        <div key={index} className="mb-1">
                          Version {index + 1}: {content.length} characters
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
                <hr />
                <h6>Raw Debug Info</h6>
                <pre className="mb-0 bg-light p-2 rounded" style={{ whiteSpace: 'pre-wrap', maxHeight: '200px', overflowY: 'auto' }}>
                  {debugInfo}
                </pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SermonEditorTest; 