from langdetect import detect
from newspaper import Article, Config
from typing import List
import concurrent.futures
import logging

MAX_URL_OUTPUT_LENGTH = 40


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


class CrawlingError(ValueError):
    """
    Thrown when there was an error while crawling url.
    """
    pass

class EmptyStringError(ValueError):
    """
    Thrown when empty string was returned from crawling method.
    """
    pass

def crawl_article(url: str) -> str:

    """
    Crawls given url.

    Args:
        url (str): Url to be crawled.

    Returns:
        str: The crawled content.
    """

    text = None
    
    config = Config()
    config.request_timeout = 5
    config.memoize_articles = False
    config.fetch_images = False

    try:
        article = Article(url, config=config)
        article.download()
        article.parse()
        text = article.text
    except Exception as e:
        if url is None:
            logger.warning(f'Could not crawl None url.')
        else:
            logger.warning(f'Could not crawl article. [{url[:MAX_URL_OUTPUT_LENGTH]}].')
        
        raise CrawlingError

    if text == '':
        logger.warning(f'Empty string was crawled. [{url[:MAX_URL_OUTPUT_LENGTH]}].')
        raise EmptyStringError

    logger.debug(f'Crawled successfully. [{url[:MAX_URL_OUTPUT_LENGTH]}].')

    return text


def get_content_from_urls(urls: List[str], lang: List[str]=['en'],  words_limit: tuple=(0,10000), json_path: str='file') -> List[str]:

    """Advanced crawler.

    Returns the list of content from crawled urls.

    Args:
        urls (List[str]): Urls to be crawled.
        lang (List[str]): Selected languages.
        words_limit (tuple): Minimum and maximum word limit for article length.
        json_path (str): Name of json file with SERP for logging purpose.

    Returns:
        list: List of crawled urls.
    """

    if words_limit[0] >= words_limit[1] or words_limit[0] < 0 or words_limit[1] < 0 or len(words_limit) > 2:
        raise ValueError('Incorrect word limits.')

    if not all(isinstance(l, str) for l in lang) or lang == []:
        raise ValueError('Incorrect languages.')

    def get_content(url):
        try:
            text = crawl_article(url)
        except CrawlingError:
            return None
        except EmptyStringError:
            return None


        word_size = len(text.split())
        language = detect(text)
        logger.debug(f'File [{json_path}]. Words: {word_size}, Lang: {language}. [{url[:MAX_URL_OUTPUT_LENGTH]}]')

        if not words_limit[0] <= word_size <= words_limit[1]:
            logger.warning(f'File [{json_path}]. Word limit {words_limit} exceeded. [{url[:MAX_URL_OUTPUT_LENGTH]}].')
            return None
        elif language not in lang:
            logger.warning(f'File [{json_path}]. Wrong language ({language}). [{url[:MAX_URL_OUTPUT_LENGTH]}].')
            return None
        else:
            logger.debug(f'File [{json_path}]. Url successfully crawled. {url[:MAX_URL_OUTPUT_LENGTH]}.')
            return text


    with concurrent.futures.ThreadPoolExecutor() as executor:
        contents = executor.map(get_content, urls)

    contents = [c for c in contents if c is not None]

    if len(contents) == len(urls):
        logger.debug(f'File [{json_path}]. Crawled all {len(urls)} websites.')
    else:
        logger.warning(f'File [{json_path}]. Crawled {len(contents)}/{len(urls)} websites.')
    
    return contents
