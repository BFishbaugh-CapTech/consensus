const BASE_URL = "http://localhost:8000";


/**
 * Retrieve all analyzed news articles.
 */
export async function getAnalysis() {
    const response = await fetch(
        `${BASE_URL}/analysis`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load analysis."
        );
    }

    return await response.json();
}


/**
 * Retrieve the raw articles.
 */
export async function getArticles() {
    const response = await fetch(
        `${BASE_URL}/articles`
    );

    if (!response.ok) {
        throw new Error(
            "Unable to load articles."
        );
    }

    return await response.json();
}


/**
 * Execute the Consensus pipeline.
 */
export async function runPipeline() {
    const response = await fetch(
        `${BASE_URL}/pipeline/run`,
        {
            method: "POST",
        }
    );

    if (!response.ok) {
        throw new Error(
            "Pipeline execution failed."
        );
    }

    return await response.json();
}