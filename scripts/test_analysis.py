from pprint import pprint

from app.ai.analyzer import Analyzer
from app.ai.llm_client import LLMClient
from app.services.rss_service import RSSService


def main() -> None:
    print("Fetching articles...")

    rss = RSSService()

    articles = rss.get_articles()

    if not articles:
        print("No articles were found.")
        return

    article = articles[0]

    print(f"Analyzing: {article.title}")
    print()

    client = LLMClient()

    analyzer = Analyzer(client)

    analysis = analyzer.analyze(article)

    print("Analysis Complete")
    print("-" * 80)

    pprint(analysis)


if __name__ == "__main__":
    main()