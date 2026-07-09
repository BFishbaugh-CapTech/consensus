import "./../style/Card.css";

function AnalysisCard({ analysis }) {
    return (
        <div className="analysis-card">

            <div className="card-header">
                <h2>{analysis.headline}</h2>

                <span className="source">
                    {analysis.source ?? "Unknown Source"}
                </span>
            </div>

            <div className="card-metrics">

                <div className="metric">
                    <strong>Political Lean</strong>
                    <span>{analysis.political_lean ?? "Unknown"}</span>
                </div>

                <div className="metric">
                    <strong>Bias Score</strong>
                    <span>{analysis.bias_score}</span>
                </div>

                <div className="metric">
                    <strong>Confidence</strong>
                    <span>
                        {analysis.confidence != null
                            ? `${Math.round(analysis.confidence * 100)}%`
                            : "Unknown"}
                    </span>
                </div>

            </div>

            <div className="section">
                <h3>Summary</h3>
                <p>{analysis.summary}</p>
            </div>

            <div className="section">
                <h3>Topics</h3>
                <div className="tags">
                    {analysis.topics.map((topic) => (
                        <span
                            key={topic}
                            className="tag"
                        >
                            {topic}
                        </span>
                    ))}
                </div>
            </div>

            <div className="section">
                <h3>People</h3>
                <div className="tags">
                    {analysis.people.map((person) => (
                        <span
                            key={person}
                            className="tag"
                        >
                            {person}
                        </span>
                    ))}
                </div>
            </div>

            <div className="section">
                <h3>Organizations</h3>
                <div className="tags">
                    {analysis.organizations.map((organization) => (
                        <span
                            key={organization}
                            className="tag"
                        >
                            {organization}
                        </span>
                    ))}
                </div>
            </div>

            <div className="section">
                <h3>Locations</h3>
                <div className="tags">
                    {analysis.locations.map((location) => (
                        <span
                            key={location}
                            className="tag"
                        >
                            {location}
                        </span>
                    ))}
                </div>
            </div>

            <div className="section">
                <h3>Reasoning</h3>
                <p>{analysis.reasoning}</p>
            </div>

        </div>
    );
}

export default AnalysisCard;