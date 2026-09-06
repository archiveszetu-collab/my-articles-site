import feedparser
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from articles.models import Article

class Command(BaseCommand):
    help = 'Import articles from a Substack RSS feed, scraping full content and cover image'

    def add_arguments(self, parser):
        parser.add_argument('feed_url', type=str)

    def scrape_page(self, url):
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')

            body = soup.find('div', class_='available-content')
            content = None
            if body:
                paragraphs = body.find_all(['p', 'h1', 'h2', 'h3', 'blockquote'])
                content = '\n\n'.join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

            image = None
            og_image = soup.find('meta', property='og:image')
            if og_image:
                image = og_image.get('content')

            return content, image
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not scrape {url}: {e}'))
            return None, None

    def handle(self, *args, **kwargs):
        feed_url = kwargs['feed_url']
        feed = feedparser.parse(feed_url)

        imported = 0
        for entry in feed.entries:
            title = entry.title
            link = entry.get('link', '')
            rss_content = entry.get('content', [{}])[0].get('value', entry.get('summary', ''))

            if Article.objects.filter(title=title).exists():
                self.stdout.write(f'Skipping (already exists): {title}')
                continue

            self.stdout.write(f'Scraping: {title}')
            full_content, cover_image = self.scrape_page(link)
            content = full_content if full_content else rss_content

            Article.objects.create(
                title=title,
                content=content,
                source_url=link,
                cover_image=cover_image,
            )
            imported += 1
            self.stdout.write(f'Imported: {title}')

        self.stdout.write(self.style.SUCCESS(f'Done. Imported {imported} new articles.'))