import json
from typing import List
import logging


# ===================================
#     Adding logger to the module
# ===================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s : %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

file_handler = logging.FileHandler('log.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# ===================================


def read_json(json_path: str) -> dict:
    """
    Reads given json.

    Args:
        json_path (str): Json file path.

    Returns:
        dict: Data from json file.
    """
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)

    except Exception as e:
        logger.exception(f'File [{json_path}].', exc_info=e)
        raise

    logger.debug(f'File [{json_path}] was read successfully.')

    return data


def get_keyword(json_path: str) -> str:
    """
    Returns keyword from json file.

    Args:
        json_path (str): Json file path.

    Returns:
        str: Keyword.
    """
    data = read_json(json_path)
    keyword = data[0]['keyword']

    return keyword


def get_urls_by_item_type(json_path: str, item_type: str,
                          url_stoplist: List[str] = ['google.com', 'facebook.com', 'instagram.com']) -> List[str]:
    """
    Returns urls from json file.

    Args:
        json_path (str): Json file path.
        item_type (str): Item type from json.
        url_stoplist (list): Domain names to exclude.

    Returns:
        list: Urls.
    """
    supported_item_types = ['organic', 'news_search']

    if item_type not in supported_item_types:
        logger.error(
            f'File [{json_path}]. Unsupported item type [{item_type}].')
        raise ValueError(f'Unsupported item type [{item_type}].')

    all_urls = list()

    data = read_json(json_path)
    items = data[0]['items']

    if item_type not in data[0]['item_types']:
        logger.warning(f'File [{json_path}]. No "{item_type}" type found.')
        return all_urls

    all_urls = [i['url'] for i in items if i['type'] == item_type]

    all_urls_count = len(all_urls)

    if all_urls_count == 0:
        logger.warning(f'File [{json_path}]. No urls found.')
        return all_urls

    def filter_func(s): return not any(x in s for x in url_stoplist)
    filtered_urls = [u for u in all_urls if filter_func(u)]

    filtered_urls_count = len(filtered_urls)

    if filtered_urls_count == all_urls_count:
        logger.debug(
            f'File [{json_path}]. Found {filtered_urls_count}/{all_urls_count} urls.')
    else:
        logger.warning(
            f'File [{json_path}]. Found {filtered_urls_count}/{all_urls_count} urls.')

    return filtered_urls


def get_organic_info(json_path: str) -> dict:
    """
    Returns dict of dicts with the most important organic information.

    Args:
        json_path (str): Json file path.

    Returns:
        dict: Dict with dicts.
    """
    data = read_json(json_path)
    items = data[0]['items']
    result = dict()

    if 'organic' not in data[0]['item_types']:
        logger.warning(f'File [{json_path}]. No "organic" type found.')
        return result

    for i in items:
        if i['type'] == 'organic':
            result[len(result)] = {
                'domain': i['domain'],
                'title': i['title'],
                'url': i['url'],
                'description': i['description'],
                'date': i['timestamp']
            }

    organic_count = len(result)
    logger.debug(f'File [{json_path}]. Found {organic_count} organic results.')

    return result


def get_related_searches(json_path: str) -> List[str]:
    """
    Returns list with **related_searches** section from json file.

    Args:
        json_path (str): Json file path.

    Returns:
        list: Related searches.
    """

    related_searches = list()
    data = read_json(json_path)

    if 'related_searches' not in data[0]['item_types']:
        logger.warning(
            f'File [{json_path}]. No "related_searches" type found.')
        return related_searches

    items = data[0]['items']
    for i in items:
        if i['type'] == 'related_searches':
            related_searches = i['items']
            break

    related_searches_count = len(related_searches)
    logger.debug(
        f'File [{json_path}]. Found {related_searches_count} related searches.')

    return related_searches


def get_people_also_ask(json_path: str) -> dict:
    """
    Returns dict with **people_also_ask** section from json file.

    Args:
        json_path (str): Json file path.

    Returns:
        dict: People also ask.
    """

    people_also_ask = dict()
    data = read_json(json_path)

    if 'people_also_ask' not in data[0]['item_types']:
        logger.warning(f'File [{json_path}]. No "people_also_ask" type found.')
        return people_also_ask

    items = data[0]['items']
    for i in items:
        if i['type'] == 'people_also_ask':
            people_also_ask_items = i['items']

    people_also_ask['questions'] = [p['title'] for p in people_also_ask_items]
    people_also_ask['urls'] = [p['expanded_element'][0]['url']
                               for p in people_also_ask_items]
    people_also_ask['descriptions'] = [p['expanded_element']
                                       [0]['description'] for p in people_also_ask_items]
    people_also_ask_q_count = len(people_also_ask['questions'])

    none_urls_count = len([a for a in people_also_ask['urls'] if not a])
    none_descriptions_count = len(
        [a for a in people_also_ask['descriptions'] if not a])

    logger.debug(
        f'File [{json_path}]. Found {people_also_ask_q_count} "people_also_ask" items.')

    if none_urls_count or none_descriptions_count:
        logger.warning(
            f'File [{json_path}]. None values - "urls":{none_urls_count}, "description":{none_descriptions_count}.')

    return people_also_ask


def get_knowledge_graph(json_path: str):
    """
    Returns knowledge graph from json file.

    Args:
        json_path (str): Json file path.

    Returns:
        str: Knowledge graph.
    """
    knowledge_graph_description = None
    data = read_json(json_path)

    if 'knowledge_graph' not in data[0]['item_types']:
        logger.warning(
            f'File [{json_path}]. No "knowledge_graph" type found.')
        return None

    items = data[0]['items']
    for i in items:
        if i['type'] == 'knowledge_graph':
            knowledge_graph_description = i['description']
            break

    logger.debug(
        f'File [{json_path}]. Found "knowledge_graph" type.')

    return knowledge_graph_description


def get_featured_snippet(json_path: str) -> dict:
    """
    Returns featured_snippet from json file.

    Args:
        json_path (str): Json file path.

    Returns:
        dict: Featured snippet.
    """
    featured_snippet = dict()
    data = read_json(json_path)

    if 'featured_snippet' not in data[0]['item_types']:
        logger.warning(
            f'File [{json_path}]. No "featured_snippet" type found.')
        return featured_snippet

    items = data[0]['items']
    for i in items:
        if i['type'] == 'featured_snippet':
            featured_snippet['domain'] = i['domain']
            featured_snippet['title'] = i['title']
            featured_snippet['description'] = i['description']
            featured_snippet['url'] = i['url']
            break

    logger.debug(
        f'File [{json_path}]. Found "featured_snippet" type.')

    return featured_snippet
