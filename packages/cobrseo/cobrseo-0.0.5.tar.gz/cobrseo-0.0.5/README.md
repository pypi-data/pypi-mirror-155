# cobrseo

[![Build Status](https://img.shields.io/badge/pypi-v0.0.5-blue)](https://pypi.org/project/cobrseo/)

### How to install

```sh
pip install cobrseo==0.0.5
```

### Package structure with all methods

```
   cobrseo
   └───json
   │   └───serp_processing
   │        │   read_json()
   │        │   get_keyword()
   │        │   get_urls_by_item_type()
   │        │   get_organic_info()
   │        │   get_related_searches()
   │        │   get_people_also_ask()
   │        │   get_knowledge_graph()
   │        │   get_featured_snippet()
   │
   └───crawler
   │   └───crawler3k
   │        │   crawl_article()
   │        │   get_content_from_urls()
   |
   └───api
       └───dataforseo_organic
            │   save_dataforseo_organic_serps()
```

# **Examples**

## SERP PROCESSING

### Get organic items with the most important information:

`get_organic_info(json_path: str) -> dict`

```python
>>> from cobrseo.json.serp_processing import get_organic_info
>>> json_path = './007b1216b666d5dbe4b1b00a3b760eb4.json'

>>> get_organic_info(json_path)
{0: {'domain': 'usa.kaspersky.com', 'title': 'Your mobile security & privacy covered - Kaspersky', 'url': 'https://usa.kaspersky.com/android-security', 'description': 'Antivirus. Protects you from viruses and malware on your Android devices by detecting, isolating and removing threats · Automatic scan. Continuously scans for\xa0...', 'date': None},
1: {'domain': 'play.google.com', 'title': 'Kaspersky Security & VPN - Apps on Google Play', 'url': 'https://play.google.com/store/apps/details?id=com.kms.free&hl=en_US&gl=US', 'description': 'Free antivirus and phone security for Android™ devices from Kaspersky Kaspersky Security & VPN for Android is a FREE-to-download antivirus solution that\xa0...', 'date': None},
...
7: {'domain': 'www.pcmag.com', 'title': 'The Best Android Antivirus Apps for 2022 | PCMag', 'url': 'https://www.pcmag.com/picks/the-best-android-antivirus-apps', 'description': 'Kaspersky Internet Security includes a comprehensive Android security suite. It scans for malware on demand and in real time, and keeps you from visiting\xa0...', 'date': None}}
```

### Get all organic urls. You can specify domains, that should not be included:

`get_urls_by_item_type(json_path: str, item_type: str, url_stoplist: List[str]=['google.com','facebook.com','instagram.com']) -> List[str]:`

- Available item types: `'organic'` and `'news_search'`

```python
>>> from cobrseo.json.serp_processing import get_urls_by_item_type

>>> get_urls_by_item_type(json_path, 'organic')
['https://usa.kaspersky.com/android-security',
'https://www.tomsguide.com/reviews/kaspersky-mobile-security',
'https://kaspersky-mobile-security.en.uptodown.com/android',
'https://apps.apple.com/us/app/kaspersky-security-vpn/id1089969624',
'https://www.safetydetectives.com/best-antivirus/kaspersky/',
'https://ltonlinestore.com/1-Device-1-Year-Kaspersky-internet-Security-For-Android-p73383495',
'https://www.pcmag.com/picks/the-best-android-antivirus-apps']

>>> get_urls_by_item_type(json_path, 'organic', url_stoplist=['kaspersky.com'])
['https://play.google.com/store/apps/details?id=com.kms.free&hl=en_US&gl=US',
'https://www.tomsguide.com/reviews/kaspersky-mobile-security',
'https://kaspersky-mobile-security.en.uptodown.com/android',
'https://apps.apple.com/us/app/kaspersky-security-vpn/id1089969624',
'https://www.safetydetectives.com/best-antivirus/kaspersky/',
'https://ltonlinestore.com/1-Device-1-Year-Kaspersky-internet-Security-For-Android-p73383495',
'https://www.pcmag.com/picks/the-best-android-antivirus-apps']
```

### Get keyword from json-serp:

`get_keyword(json_path: str) -> str`

```python
>>> from cobrseo.json.serp_processing import get_keyword

>>> get_keyword(json_path)
'kaspersky mobile antivirus'
```

### Get related searches:

`get_related_searches(json_path: str) -> List[str]:`

```python
>>> from cobrseo.json.serp_processing import get_related_searches

>>> get_related_searches(json_path)
['kaspersky mobile antivirus free',
'kaspersky mobile antivirus cracked apk',
'kaspersky mobile antivirus apk',
'kaspersky mobile security android',
'kaspersky mobile antivirus download',
'kaspersky mobile security activation key',
'kaspersky free antivirus',
'kaspersky mobile antivirus review']
```

### Get people aslo ask:

`get_people_also_ask(json_path: str)-> dict:`

```python
>>> from cobrseo.json.serp_processing import get_people_also_ask

>>> get_people_also_ask(json_path)
{'questions': ['Is Kaspersky antivirus good for mobile?', 'Is Kaspersky free for mobile?', 'Which antivirus is best for mobile?', 'Do I need Kaspersky on my Android?'],
'urls': ['https://www.pcmag.com/reviews/kaspersky-internet-security-for-android', 'https://www.safetydetectives.com/blog/best-really-free-antivirus-programs-for-android/', 'https://www.tomsguide.com/best-picks/best-android-antivirus', 'https://support.kaspersky.com/consumer/products/Kaspersky_Internet_Security_for_Android'],
'descriptions': ["The Bottom Line. Kaspersky Internet Security offers Android users top-tier malware protection, great anti-phishing protection, and tools to secure and recover lost and stolen phones. But some features didn't work as advertised in our hands-on testing. Sep 30, 2015", "Kaspersky Security Free — Easy to Use with Decent On-Demand Virus Scanning. Kaspersky Security Free is a decent free internet security app for Android users — and because it only provides a couple of free features, it's very easy to use.", 'Bitdefender Mobile Security. Best paid option. ...\nNorton Mobile Security. Specifications. ...\nAvast Mobile Security. Specifications. ...\nKaspersky Mobile Antivirus. Specifications. ...\nLookout Security & Antivirus. Specifications. ...\nMcAfee Mobile Security. Specifications. ...\nGoogle Play Protect. Specifications.', 'Kaspersky Internet Security for Android provides comprehensive protection for your mobile devices. Along with providing protection against viruses and other malware, the app protects your internet connection, the data on your device, access to other apps, and also allows you to block unwanted calls.']}
```

## CRAWLER

### Crawling list of urls:

`get_content_from_urls`
Parameters:

- `urls: List[str]`: Urls to be crawled.
- `lang: List[str]=['en']`: Selected languages.
- `words_limit: tuple=(0,10000)`: Minimum and maximum word limit for article length.
- `json_path: str='file'`: Name of json file with SERP for logging purpose.

Returns:

- `List[str]`: List of crawled urls.

```python
>>> from cobrseo.crawler.crawler3k import get_content_from_urls

>>> urls = ['https://www.pcmag.com/reviews/kaspersky-internet-security-for-android',
'https://www.safetydetectives.com/blog/best-really-free-antivirus-programs-for-android/',
'https://www.tomsguide.com/best-picks/best-android-antivirus',
'https://support.kaspersky.com/consumer/products/Kaspersky_Internet_Security_for_Android']

>>> len(get_content_from_urls(urls))
4
```

## API

### DataForSeo (google organic):

`save_dataforseo_organic_serps`
Parameters:

- `keywords: List[str]`: Keywords for search.
- `destination_path: str`: Directory for json saving.
- `rewrite_serp: bool`: Allow to rewrite already saved json.
- `token: str`: API-KEY from DataForSeo.
- `max_retries_ready_request: int=30`: Number of allowed READY requests with same progress that would be sent before interrupting.
- `resend_post_if_ready_failed: bool=True`: If the value is `True` then failed keywords from READY request will be added again in POST request queue.
- `max_retries_get_request: int=5`: Number of allowed GET requests with `None` value that would be received before interrupting.
- `resend_post_if_get_failed: bool=True`: If the value is `True` then failed keywords from GET request will be added again in POST request queue.
- `post_size: int=80`: Number of keywords in one POST request (max=100, but 80 is recommended).
- `lang: str='en'`: Language (DataForSeo parameter).
- `loc: int=2840`: Location (DataForSeo parameter).
- `depth: int=10`: SERP depth (DataForSeo parameter).

Returns:

- `List[dict]`: List of dict with keywords and mapped json paths.

### Small cheatsheet

| Country | `lang` | `loc`  |
| ------- | ------ | ------ |
| US      | `en`   | `2840` |
| Germany | `de`   | `2276` |
| Spain   | `es`   | `2724` |
| Italy   | `it`   | `2380` |
| France  | `fr`   | `2250` |

```python
>>> from cobrseo.api.dataforseo_organic import save_dataforseo_organic_serps

>>> keywords = ['Industroyer', 'blackcat', 'revil', 'Moncler', 'Conti ransomware']
>>> destination_path = './serps'
>>> rewrite_serp = False
>>> token = 'API_KEY'

>>> save_dataforseo_organic_serps(
            keywords,
            destination_path,
            rewrite_serp,
            token
        )
[{'keyword': 'revil', 'path': './serps/d1c0dd7a20099294bfe3dba2c0b4e507.json'},
{'keyword': 'blackcat', 'path': './serps/5c55d71b4c47d141072cf0540c046d07.json'},
{'keyword': 'Industroyer', 'path': './serps/492ed356c6aa5e4bd9de4a81b4fa2add.json'},
{'keyword': 'Conti ransomware', 'path': './serps/6ba632a49d9e504bad1fde6f9281a2db.json'},
{'keyword': 'Moncler', 'path': './serps/faf6dd008e4b7640583c95e1cbbf1533.json'}]
```

### Version changes

##### `v0.0.1`

- Initial release.

##### `v0.0.2`

- Python version changed from 3.8 to 3.6 in PyPI.

##### `v0.0.3`

- `cobrseo.api.dataforseo_organic`:
  - Removed `dirs_to_check` parameter from `save_dataforseo_organic_serps` method.
    Flag `rewrite_serp` was added instead.
    Now SERP checking is performed in `destination_path` directory only.
  - Fixed bug with `save_dataforseo_organic_serps` return value.
    Now list with all keywords is returned, even with the ones that have already existed.
- Documentation updated.

##### `v0.0.4`

- `cobrseo.json.serp_processing`:

  - Added `get_knowledge_graph` method. If knowledge graph exists then `str` will be returned, otherwise - `None`.
  - Added `get_featured_snippet` method. Returns snippet in `dict`.

- `cobrseo.api.dataforseo_organic`:

  - Fixed bug with `null` in json. From now on, if GET request returns `None` in `result` section, it will continue sending GET request with same id untill it returns correct result.
  - Updated logging messages.

- `tests`:

  - New correct approuch for testing.
  - New tests for new methods.
  - Refactoring `source.py`.

- README.md available on pypi.org.

##### `v0.0.5`

- `cobrseo.api.dataforseo_organic`:

  - Added 4 new parameters to `save_dataforseo_organic_serps` method for dealing with response repetitions:

    - `max_retries_ready_request` - How many READY requests with same progress would be sent before interrupting.
    - `resend_post_if_ready_failed` - What to do with those keywords that are not returned from READY requests. If the value is `True` then this keyword will be added again in POST request queue.
    - `max_retries_get_request` - How many GET requests with `None` value would be received before interrupting.
    - `resend_post_if_get_failed` - What to do with those keywords that are not returned from GET requests. If the value is `True` then this keyword will be added again in POST request queue.

  - Added new feature that specifies directories for different `lang` and `loc`.
  - Updated logging massages.
  - Changed file extension for ids returned from POST request.

- Removed `__pycahce__` folders from repository.
