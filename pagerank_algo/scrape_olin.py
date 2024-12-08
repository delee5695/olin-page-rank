import requests
from bs4 import BeautifulSoup
import pickle


def scrape_page(url):
    out_links_list = []

    # Send a GET request to the URL
    try:
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, "html.parser")
            if "This page cannot be found" in soup.title.string:
                return "broke"
            # Find all <a> tags with an href attribute
            links = soup.find_all("a", href=True)
        else:
            return "broke"

        # Extract and print each href value
        for idx, link in enumerate(links):
            href = link["href"]
            if len(href) > 0:
                # Check links within the page ex. /contact
                if href[0] == "/":
                    out_links_list.append("https://www.olin.edu/" + href[1:].strip())
                elif "olin.edu" in href:
                    out_links_list.append(href.strip())
                elif href.startswith("mailto:") or href.startswith("tel:"):
                    out_links_list.append(href.strip())
    except Exception as e:
        out_links_list = []
    return out_links_list


if __name__ == "__main__":
    links_visited = []
    links_to_visit = []
    links_to_visit.append("https://www.olin.edu/")
    out_links_dict = {}
    while len(links_to_visit) > 0:
        # https://library.olin.edu/
        print(f"left to visit: {len(links_to_visit)}, visited: {len(links_visited)}\n")
        link = links_to_visit[0]
        links_to_visit = links_to_visit[1:]
        links_visited.append(link)
        back_links = scrape_page(link)
        if back_links != "broke":
            out_links_dict[link] = back_links
            print(f"Scraping: {link}\n")
            for unvisited_link in out_links_dict[link]:
                if (
                    links_visited.count(unvisited_link) < 1
                    and links_to_visit.count(unvisited_link) < 1
                ):
                    # print(unvisited_link)
                    if "#" not in unvisited_link and "?" not in unvisited_link:
                        if (
                            "https://my.olin.edu/ics/" not in unvisited_link
                            and "https://my.olin.edu/ICS/" not in unvisited_link
                        ):
                            links_to_visit.append(unvisited_link)
        else:
            print("Broken Link")
    with open("outlinks-dict.pickle", "wb") as handle:
        pickle.dump(out_links_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
