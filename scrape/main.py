from typing import List
import requests
import json


# class Hashtag:
#     def __init__(self, query):
#         print("AFTER INIT")
#         print(query)
#         scrape = requests.get(
#             f"https://instagram.com/explore/tags/{query}/?__a=1"
#         ).json()
#         print("AFTER GRAPHQL")
#         self.hashtag_data = scrape["graphql"]["hashtag"]["edge_hashtag_to_media"]
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
        headers={
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": 'mid=YkSqfAAEAAGicyuRvG6XLSt8mqjx; ig_did=93DEC88A-4441-4C82-B215-82B374288912; ig_nrcb=1; shbid="4998\0549995949688\0541680626518:01f7de189be75bf44cc08cdcca6d367d64e504680c602578dcb6e637392d6e8a5690b019"; shbts="1649090518\0549995949688\0541680626518:01f7e47fcc3e286b74fb2a9f9022c635cf338ec6bbdabbca94314033ee81d4ac37f088a3"; csrftoken=PTWyyPvqMCYmLvWAmJCB45z5F9RbiDMR; ds_user_id=9995949688; sessionid=9995949688%3AwSUp9EmUQ2Yq6F%3A1; rur="LDC\0549995949688\0541680822623:01f70a615cf734a734e53da385592b2a5285ac774780725bf861e66abf43918ed22e4fd4"',
            "Host": "www.instagram.com",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "TE": "trailers",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (X11;Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
        },
    ).json()
    print(data.headers)


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
