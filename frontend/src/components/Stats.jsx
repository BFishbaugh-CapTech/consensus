import "./../style/App.css";

function Stats({
    articleCount,
    generatedAt,
}) {
    return (
        <section className="stats">

            <div className="stat-card">
                <h3>Articles Analyzed</h3>
                <p>{articleCount}</p>
            </div>

            <div className="stat-card">
                <h3>Generated</h3>
                <p>{generatedAt}</p>
            </div>

            <div className="stat-card">
                <h3>Status</h3>
                <p>Complete</p>
            </div>

        </section>
    );
}

export default Stats;