import { makeReferencesClickable } from '../utils/bibleReferences';

interface CommentItem {
    verseStart: number;
    verseEnd: number;
    text: string;
    id: string;
}

interface Props {
    bookId: string;
    chapter: number;
    comments: CommentItem[];
}

export function CommentsSection({ comments }: Props) {
    if (comments.length === 0) return null;

    const handleBackToVerse = (verse: number, e: React.MouseEvent) => {
        e.preventDefault();
        const el = document.getElementById(`verse-${verse}`);
        if (el) {
            el.scrollIntoView({ behavior: 'smooth', block: 'center' });
            // Add a temporary highlight effect
            el.classList.add('highlight-temp');
            setTimeout(() => el.classList.remove('highlight-temp'), 2000);
        }
    };

    return (
        <div className="comments-section">
            <h3>Comentarios</h3>

            <div className="bible-comments-list">
                {comments.map((item) => (
                    <div key={item.id} id={item.id} className="bible-comment-card">
                        <div className="comment-header">
                            <span className="comment-verse-ref">
                                {item.verseStart === item.verseEnd
                                    ? `Versículo ${item.verseStart}`
                                    : `Versículos ${item.verseStart}-${item.verseEnd}`}
                            </span>
                            <a
                                href={`#verse-${item.verseStart}`}
                                onClick={(e) => handleBackToVerse(item.verseStart, e)}
                                className="back-to-verse-link"
                                title="Volver al versículo"
                            >
                                ↑ Ver texto
                            </a>
                        </div>
                        <div
                            className="comment-text"
                            dangerouslySetInnerHTML={{ __html: makeReferencesClickable(item.text) }}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
}
