# Olin PageRank

A search engine prototype for Olin College’s website. It crawls pages starting at `olin.edu`, ranks them using their link structure, and lets users search the indexed page content through a Flask web interface.

## How it works

1. **Crawl.** Starting at `https://www.olin.edu/`, the crawler collects outgoing links and saves them as a directed graph in `outlinks-dict.pickle`.
2. **Rank.** The ranking script uses NumPy to compute an eigendecomposition of a PageRank-style transition matrix and assigns each page a numerical rank.
3. **Index.** The indexing script fetches page titles and paragraph content and writes each page’s URL, title, content, and rank to MongoDB.
4. **Search.** Flask submits the query to MongoDB Search against the `fulltext` field and displays matching pages in ascending rank order. Rank 1 appears first when it matches the query.

## Run locally

From the repository root, create an environment and install the app and indexing dependencies.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install flask "pymongo[srv]" requests beautifulsoup4 numpy scikit-learn
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

### Configure MongoDB

Use a MongoDB deployment with support for the `$search` aggregation stage, such as MongoDB Atlas. Create a search index named `default` on `page_rank.webpages` that indexes `fulltext` as text. The app uses that default index in its search query.

The source contains hard-coded connection strings. If they contain live credentials, rotate them before sharing the project. To configure your own connection, add `import os` and replace the `uri` assignment with `uri = os.environ["MONGODB_URI"]` in both `site/app.py` and `pagerank_algo/write_database.py`. Apply the same change in `site/test.py` if you plan to run that example. Set `MONGODB_URI` in your shell to your deployment’s connection string.

### Populate the collection

The repository includes a saved link graph. From the repository root, run the indexer from inside `pagerank_algo/` so it can find the graph.

```sh
(cd pagerank_algo && python write_database.py)
```

This step uses the bundled graph to rank pages and fetches their current content over the network. Start with an empty collection for the first import. The script inserts new documents on each run, so rerunning it against the same collection can create duplicates.

To rebuild the link graph first, run the crawler from the same directory. This overwrites the bundled graph.

```sh
(cd pagerank_algo && python scrape_olin.py)
```

### Start the web app

```sh
python site/app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) and search for a term such as `engineering`. Flask runs in debug mode for local development.

## Project files

| Path | Purpose |
| --- | --- |
| `pagerank_algo/scrape_olin.py` | Crawls links and saves the graph. |
| `pagerank_algo/outlinks-dict.pickle` | Saved URL-to-outlinks mapping. |
| `pagerank_algo/rank_pages.py` | Calculates page ranks from the link graph. |
| `pagerank_algo/write_database.py` | Fetches page content and inserts ranked entries into MongoDB. |
| `site/app.py` | Flask routes and MongoDB search query. |
| `site/templates/` and `site/static/` | Search interface and styling. |
| `site/test.py` | Example MongoDB search query. |
| `page_rank.ipynb` | PageRank exploration in Jupyter. |
| `random_walk.py` | Animates a random walk on a generated directed graph. |

To run the random-walk animation, install the optional visualization dependencies and run the script.

```sh
python -m pip install networkx matplotlib
python random_walk.py
```
