import { useEffect, useState } from "react";

import Header from "./components/Header";
import Stats from "./components/Stats";
import AnalysisCard from "./components/AnalysisCard";
import LoadingSpinner from "./components/LoadingSpinner";

import { getAnalysis } from "./services/api";

import "./style/App.css";


function App() {

    const [analysis, setAnalysis] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadAnalysis();
    }, []);


    async function loadAnalysis() {

        try {
            setLoading(true);

            const data = await getAnalysis();

            setAnalysis(data);
            setError(null);

        } catch (err) {

            console.error(err);

            setError(
                "Unable to load analysis from the server."
            );

        } finally {

            setLoading(false);

        }
    }


    if (loading) {
        return <LoadingSpinner />;
    }

    if (error) {
        return (
            <div className="app">

                <Header />

                <div className="error">
                    <h2>Error</h2>
                    <p>{error}</p>
                </div>

            </div>
        );
    }


    return (
        <div className="app">

            <Header />

            <Stats
                articleCount={analysis.length}
                generatedAt={new Date().toLocaleString()}
            />

            <main className="analysis-container">

                {analysis.length === 0 ? (

                    <p>No analysis available.</p>

                ) : (

                    analysis.map((item) => (
                        <AnalysisCard
                            key={item.article_id}
                            analysis={item}
                        />
                    ))

                )}

            </main>

        </div>
    );
}

export default App;