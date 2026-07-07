from app.services.rss_service import RSSService

print("TEST SCRIPT IS RUNNING")

rss = RSSService()

articles = rss.get_articles()

rss.export_articles_to_json(articles)

print(f"Downloaded {len(articles)} articles.\n")

for article in articles[:5]:
    print("=" * 80)
    print(f"Title: {article.title}")
    print(f"Source: {article.source}")
    print(f"Published: {article.published_at}")
    print(f"Author: {article.author}")
    print(f"URL: {article.url}")
    print()