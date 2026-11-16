# Olin PageRank

A search-engine prototype for Olin College web pages. The project crawls links within `olin.edu`, builds a directed page graph, ranks pages with a Google-style PageRank algorithm, stores page content in MongoDB, and serves a Flask search interface.

## How It Works

1. **Crawl** - `pagerank_algo/scrape_olin.py` discovers eligible Olin pages and saves their outlinks.
2. **Rank** - `pagerank_algo/rank_pages.py` calculates a PageRank ordering.
3. **Index** - `pagerank_algo/write_database.py` stores page titles, text, and rankings in MongoDB.
4. **Search** - `site/app.py` searches indexed page text and sorts results by PageRank.

## Repository Layout

- `pagerank_algo/scrape_olin.py` - Olin.edu crawler and graph generator.
- `pagerank_algo/rank_pages.py` - PageRank calculation.
- `pagerank_algo/write_database.py` - MongoDB indexing script.
- `site/app.py` - Flask search application.
- `site/templates/` - HTML templates.
- `site/static/` - CSS styling.
- `page_rank.ipynb` - Notebook exploration.
- `random_walk.py` - Animated random-walk visualization.
- `site/test.py` - Example MongoDB search query.

## Requirements

Python 3.8+ is recommended. Install the dependencies with:

```sh
pip install flask requests beautifulsoup4 numpy scikit-learn networkx matplotlib pymongo jupyter
