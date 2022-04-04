from typing import List
import requests
import json


class Hashtag:
    def __init__(self, query):
        scrape = requests.get(
            f"https://instagram.com/explore/tags/{query}/?__a=1"
        ).json()
        self.hashtag_data = scrape["graphql"]["hashtag"]["edge_hashtag_to_media"]
        self.count = self.hashtag_data["count"]
        self.data_container = self.hashtag_data["edges"]

    data_list = []

    def scrape(self) -> list:
        """
        The whole scraping algorithm.

        Returns:
            data_list: list
        """
        # FIXME: There's an issue that the objects do not load completely.
        # you cannot get the first 100 posts right now.
        # HACK: This is not the right way. Because of the above issue,
        # currently we can only get the first fifty posts.
        # After fixing, replace 50 with the desired_amount or all
        for post_number in range(0, 50):
            print(post_number)
            data = self.data_container[post_number]["node"]["shortcode"]
            print(data)
            self.data_list.append(data)
            print(self.data_container)
        return self.data_list


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
