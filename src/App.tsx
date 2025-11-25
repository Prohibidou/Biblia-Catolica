import { useEffect, useState, useRef } from 'react';
import './App.css';
import { BibleService } from './services/BibleService';
import type { Verse } from './models/Verse';
import { BIBLE_BOOKS } from './constants/BibleBooks';
import { CommentsSection } from './components/CommentsSection';
import { makeReferencesClickable, attachReferenceHandlers, type BibleReference } from './utils/bibleReferences';

// Singleton instance
const bibleService = new BibleService();

function App() {
  const [versions] = useState(bibleService.getAvailableVersions());
  const [selectedVersion, setSelectedVersion] = useState(versions[0].id);

  // Navigation State
  const [selectedBook, setSelectedBook] = useState('GEN');
  const [selectedChapter, setSelectedChapter] = useState(1);
  const [selectedVerse, setSelectedVerse] = useState<number | null>(null);

  const [verses, setVerses] = useState<Verse[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Ref for attaching reference click handlers
  const versesContainerRef = useRef<HTMLDivElement>(null);

  // Initial Load
  useEffect(() => {
    bibleService.initialize();
    loadContent(selectedVersion, selectedBook, selectedChapter);
  }, []);

  // Attach click handlers to Bible reference links after verses render
  useEffect(() => {
    if (versesContainerRef.current) {
      attachReferenceHandlers(versesContainerRef.current, handleReferenceClick);
    }
  }, [verses]); // Re-attach whenever verses change

  // When Version/Book/Chapter changes, reload content
  const loadContent = async (vId: string, bId: string, ch: number) => {
    setLoading(true);
    setError(null);
    try {
      await bibleService.loadVersion(vId);
      const content = await bibleService.getChapter(bId, ch);
      setVerses(content);

      // If specific verse selected, scroll to it
      if (selectedVerse) {
        setTimeout(() => {
          const el = document.getElementById(`verse-${selectedVerse}`);
          if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
      }
    } catch (err: any) {
      console.error(err);
      setError(`Error loading content: ${err.message}`);
      setVerses([]);
    } finally {
      setLoading(false);
    }
  };

  const handleVersionChange = (newVersion: string) => {
    setSelectedVersion(newVersion);
    setSelectedVerse(null);
    loadContent(newVersion, selectedBook, selectedChapter);
  };

  const handleBookChange = (newBook: string) => {
    setSelectedBook(newBook);
    setSelectedChapter(1);
    setSelectedVerse(null);
    loadContent(selectedVersion, newBook, 1);
  };

  const handleChapterChange = (newChapter: number) => {
    setSelectedChapter(newChapter);
    setSelectedVerse(null);
    loadContent(selectedVersion, selectedBook, newChapter);
  };

  const handleVerseSelect = (verseNum: number) => {
    setSelectedVerse(verseNum);
    const el = document.getElementById(`verse-${verseNum}`);
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
  };

  const handleReferenceClick = (ref: BibleReference) => {
    // Navigate to the referenced book and chapter
    setSelectedBook(ref.book);
    setSelectedChapter(ref.chapter);

    // If specific verse is mentioned, scroll to it after content loads
    if (ref.verseStart) {
      setSelectedVerse(ref.verseStart);
    } else {
      setSelectedVerse(null);
    }

    // Load the new content
    loadContent(selectedVersion, ref.book, ref.chapter);
  };

  // Get current book metadata to know how many chapters it has
  const currentBookMeta = BIBLE_BOOKS.find(b => b.id === selectedBook);
  const totalChapters = currentBookMeta ? currentBookMeta.chapters : 1;

  // Extract comments from verses (only for Navarra and Straubinger)
  const hasComments = selectedVersion === 'navarra' || selectedVersion === 'straubinger';
  const chapterComments = hasComments
    ? verses.filter(v => v.comment).map(v => `${v.verse}. ${v.comment}`)
    : [];

  return (
    <div className="container">
      <header className="app-header">
        <h1>📖 Biblia Católica</h1>
      </header>

      <div className="controls-panel">
        {/* Top Row: Version */}
        <div className="control-row">
          <select
            value={selectedVersion}
            onChange={(e) => handleVersionChange(e.target.value)}
            disabled={loading}
            className="version-select"
          >
            {versions.map(v => (
              <option key={v.id} value={v.id}>{v.name}</option>
            ))}
          </select>
        </div>

        {/* Bottom Row: Navigation (Book, Chapter, Verse) */}
        <div className="control-row navigation-row">
          <select
            value={selectedBook}
            onChange={(e) => handleBookChange(e.target.value)}
            disabled={loading}
          >
            {BIBLE_BOOKS.map(b => (
              <option key={b.id} value={b.id}>{b.name}</option>
            ))}
          </select>

          <select
            value={selectedChapter}
            onChange={(e) => handleChapterChange(Number(e.target.value))}
            disabled={loading}
          >
            {Array.from({ length: totalChapters }, (_, i) => i + 1).map(num => (
              <option key={num} value={num}>Capítulo {num}</option>
            ))}
          </select>

          <select
            value={selectedVerse || ''}
            onChange={(e) => handleVerseSelect(Number(e.target.value))}
            disabled={loading || verses.length === 0}
          >
            <option value="">Ir a verso...</option>
            {verses.map(v => (
              <option key={v.verse} value={v.verse}>Verso {v.verse}</option>
            ))}
          </select>
        </div>
      </div>

      {error && <div className="error-message">{error}</div>}

      <main className="reader-content">
        {loading ? (
          <div className="loading-spinner">Cargando...</div>
        ) : (
          <>
            {verses.length > 0 ? (
              <>
                <div className="chapter-header">
                  <h2>{currentBookMeta?.name} {selectedChapter}</h2>
                  <p className="version-label">{versions.find(v => v.id === selectedVersion)?.shortName}</p>
                </div>

                <div className="verses-list" ref={versesContainerRef}>
                  {verses.map((v, i) => (
                    <div key={i} id={`verse-${v.verse}`} className={selectedVerse === v.verse ? 'highlighted verse-block' : 'verse-block'}>
                      {v.comment && (
                        <div
                          className="verse-comment"
                          dangerouslySetInnerHTML={{
                            __html: makeReferencesClickable(v.comment)
                          }}
                        ></div>
                      )}
                      <p className="verse-content">
                        <sup className="verse-num">{v.verse}</sup>
                        {v.text}
                      </p>
                    </div>
                  ))}
                </div>

                {hasComments && chapterComments.length > 0 && (
                  <>
                    <hr className="divider" />
                    <CommentsSection
                      bookId={selectedBook}
                      chapter={selectedChapter}
                      comments={chapterComments}
                    />
                  </>
                )}
              </>
            ) : (
              <div className="empty-state">
                <p>No hay contenido disponible para este capítulo en la versión de prueba.</p>
                <small>Nota: Solo algunos capítulos están disponibles en la demo (Génesis 1, Juan 3).</small>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
