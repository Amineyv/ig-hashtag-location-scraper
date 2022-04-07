from typing import List
import requests
import json

from scrape.metadata import COOKIES, HEADERS


# class Hashtag:
#     def __init__(self, query):
#         print("AFTER INIT")
#         print(query)
#         scrape = requests.get(
#             f"https://instagram.com/explore/tags/{query}/?__a=1"
#         ).json()
#         print("AFTER GRAPHQL")
#         self.ag_data = scrape["graphql"]["hashtag"]["edge_hashtag_to_media"]
#         self.count = self.hashtag_data["count"]
#         self.data_container = self.hashtag_data["edges"]
#         print("INIT FINISH")

#     data_list = []


def scrape_graphql(query) -> list:
    """
    The whole scraping algorithm.

    Returns:
        data_list: list
    """
    data = requests.get(f"https://instagram.com/explore/tags/{query}/?__a=1").json()
    hashtag_data = data["graphql"]["hashtag"]["edge_hashtag_to_media"]
    count = hashtag_data["count"]
    data_container = hashtag_data["edges"]
    print(count)
    # FIXME: There's an issue that the objects do not load completely.
    # you cannot get the first 100 posts right now.
    # HACK: This is not the right way. Because of the above issue,
    # currently we can only get the first fifty posts.
    # After fixing, replace 50 with the desired_amount or all
    print("scrape initiated, before loop")
    data_list = []
    for post_number in range(0, 50):
        print(post_number)
        data = data_container[post_number]["node"]["shortcode"]
        print(data)
        data_list.append(data)
        print(data_container)
    return data_list


def scrape_http(query):

    data = requests.get(
        f"https://instagram.com/explore/tags/{query}/?__a=1",
        headers=HEADERS,
        cookies=COOKIES,
    ).json()
    print(data.headers)
    # TODO: return the data from scraped web page.


def _save_to_file(dict_data) -> None:
    """
    Pass a dictionary file and save as a json file.
    Parameters:
        dict_data: Dict

    Returns:
        None
    """
    json_data = json.dumps(dict_data)
    with open("data.json", "w") as file:
        file.write(json_data)
    file.close()
