import { useState, useRef, useEffect } from 'react';
import { BIBLE_BOOKS } from '../constants/BibleBooks';
import './BookSelector.css';

interface BookSelectorProps {
    selectedBook: string;
    onSelectBook: (bookId: string) => void;
    disabled?: boolean;
}

export function BookSelector({ selectedBook, onSelectBook, disabled }: BookSelectorProps) {
    const [isOpen, setIsOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    const selectedBookName = BIBLE_BOOKS.find(b => b.id === selectedBook)?.name || 'Seleccionar Libro';

    // Close dropdown when clicking outside
    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    const handleSelect = (bookId: string) => {
        onSelectBook(bookId);
        setIsOpen(false);
    };

    const oldTestament = BIBLE_BOOKS.filter(b => b.testament === 'Antiguo Testamento');
    const newTestament = BIBLE_BOOKS.filter(b => b.testament === 'Nuevo Testamento');

    return (
        <div className="book-selector-container" ref={dropdownRef}>
            <label className="control-label">Libro</label>
            <button
                className="book-selector-button"
                onClick={() => !disabled && setIsOpen(!isOpen)}
                disabled={disabled}
                type="button"
            >
                {selectedBookName}
                <span className="dropdown-arrow">▼</span>
            </button>

            {isOpen && (
                <div className="book-dropdown-menu">
                    <div className="testament-column">
                        <h4 className="testament-title">ANTIGUO TESTAMENTO</h4>
                        <div className="books-grid">
                            {oldTestament.map(book => (
                                <div
                                    key={book.id}
                                    className={`book-option ${selectedBook === book.id ? 'selected' : ''}`}
                                    onClick={() => handleSelect(book.id)}
                                >
                                    {book.name}
                                </div>
                            ))}
                        </div>
                    </div>

                    <div className="testament-column">
                        <h4 className="testament-title">NUEVO TESTAMENTO</h4>
                        <div className="books-grid">
                            {newTestament.map(book => (
                                <div
                                    key={book.id}
                                    className={`book-option ${selectedBook === book.id ? 'selected' : ''}`}
                                    onClick={() => handleSelect(book.id)}
                                >
                                    {book.name}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
