import "./../style/App.css";

function LoadingSpinner() {
    return (
        <div className="loading-container">

            <div className="spinner"></div>

            <h2>Analyzing Today's News...</h2>

            <p>
                Consensus is collecting articles and generating
                structured analyses. This may take a minute.
            </p>

        </div>
    );
}

export default LoadingSpinner;