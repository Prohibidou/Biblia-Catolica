interface Props {
    bookId: string;
    chapter: number;
    comments: string[];
}

export function CommentsSection({ comments }: Props) {
    if (comments.length === 0) return null;

    return (
        <div className="comments-section">
            <h3>Comentarios de la Biblia</h3>

            <div className="bible-comments-list">
                {comments.map((comment, index) => (
                    <div key={index} className="bible-comment-card">
                        <p className="comment-text" dangerouslySetInnerHTML={{ __html: comment }}></p>
                    </div>
                ))}
            </div>
        </div>
    );
}
