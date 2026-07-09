import "./../style/App.css";

function Header() {
    return (
        <header className="header">

            <h1>Consensus</h1>

            <p className="subtitle">
                AI-Powered News Consensus Generator
            </p>

            <p className="description">
                Consensus analyzes news articles from multiple publishers,
                extracts the underlying facts, identifies key people,
                organizations, and locations, and estimates political
                leaning and bias to produce a structured, source-agnostic
                view of today's news.
            </p>

        </header>
    );
}

export default Header;