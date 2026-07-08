from app.services.rss_service import RSSService
import logging

print("TEST SCRIPT IS RUNNING")
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

rss = RSSService()

articles = rss.get_articles()

rss.export_articles_to_json(articles)