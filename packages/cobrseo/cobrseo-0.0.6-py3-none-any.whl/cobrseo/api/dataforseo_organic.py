from http.client import HTTPSConnection
import json
import os
import hashlib
import time
from typing import List
import logging
import pandas as pd

SAVE_FILE = 'post_id_save.csv'


# ===================================
#     Adding logger to the module
# ===================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s: %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

file_handler = logging.FileHandler('dataforseo.log', mode='w')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# ===================================


class RestClient:
    domain = 'api.dataforseo.com'

    def __init__(self, credential):
        self.credential = credential

    def request(self, path, method, data=None):
        connection = HTTPSConnection(self.domain)

        try:
            headers = {
                'Authorization': f'Basic {self.credential}',
                'Content-Type': 'application/json'
            }
            connection.request(method, path, headers=headers, body=data)
            response = connection.getresponse()

            return json.loads(response.read().decode())
        finally:
            connection.close()

    def get(self, path):
        return self.request(path, 'GET')

    def post(self, path, data):
        if isinstance(data, str):
            data_str = data
        else:
            data_str = json.dumps(data)
        return self.request(path, 'POST', data_str)


def make_post_request(client, post_data, size_remained):
    post_ids = []

    post_response = client.post('/v3/serp/google/organic/task_post', post_data)
    if post_response['status_code'] == 20000:

        post_ids = [{'id': t['id'], 'keyword': t['data']['keyword']} for t in post_response['tasks']
                    if t['status_message'] == 'Task Created.']

        logger.info(
            f'POST. id size = {len(post_ids)}. Remained keywords size = {size_remained}.')

        pd.DataFrame(data=post_ids).to_csv(SAVE_FILE, index=False)

    else:
        logger.error(
            f"POST error. Code: {post_response['status_code']} Message: {post_response['status_message']}")
        time.sleep(5)

    return post_ids


def make_ready_request(client, post_ids, failed_keywords, max_retries, resend_post_if_ready_failed):
    post_ids_size = len(post_ids)

    if post_ids_size <= 10:
        timeout = post_ids_size * 5
    elif post_ids_size <= 20:
        timeout = post_ids_size * 4
    elif post_ids_size <= 40:
        timeout = post_ids_size * 3
    else:
        timeout = post_ids_size * 2

    post_ids_2 = [p['id'] for p in post_ids]
    ready_ids = None
    retry = 0
    size_saved = 0
    while True:
        time.sleep(timeout)

        ready_response = client.get('/v3/serp/google/organic/tasks_ready')

        if ready_response['status_code'] == 20000:
            if ready_response['tasks'][0]['result'] is None:
                logger.warning('READY returned None. Retrying...')
                continue

            ready_ids = [t['id'] for t in ready_response['tasks']
                         [0]['result'] if t['id'] in post_ids_2]

            if len(ready_ids) == len(post_ids_2):
                logger.info(
                    f'READY. All keywords are ready. Returning {len(post_ids)}/{len(post_ids)} ids. Quitting...')
                return post_ids

            if len(ready_ids) != size_saved:
                size_saved = len(ready_ids)
                retry = 0

            elif len(ready_ids) == size_saved:

                if retry == max_retries:
                    logger.info(f'READY. Reached max_retries.')
                    new_post_ids = [
                        p for p in post_ids if p['id'] in ready_ids]
                    if resend_post_if_ready_failed:
                        logger.info(f'READY. Collecting absent keywords.')
                        absent_keywords = [p['keyword']
                                           for p in post_ids if p['id'] not in ready_ids]
                        failed_keywords.extend(absent_keywords)
                    else:
                        logger.info(f'READY. Skipping absent keywords...')

                    logger.info(
                        f'READY. Returning {len(new_post_ids)}/{len(post_ids)} ids. Quitting...')
                    return new_post_ids
                else:
                    retry += 1

            logger.info(
                f'READY. [Attempt # {retry}/{max_retries}] id size = {len(ready_ids)}/{len(post_ids_2)}')
        else:
            logger.error(
                f"READY error. Retrying... Code: {ready_response['status_code']} Message: {ready_response['status_message']}")
            time.sleep(5)


def make_get_request(client, post_ids, destination_path, keywords_paths_mapped, failed_keywords, max_retries, resend_post_if_get_failed):
    for i in post_ids:
        retry = 0

        while True:
            get_response = client.get(
                f'/v3/serp/google/organic/task_get/advanced/{i["id"]}')
            if get_response['status_code'] == 20000:
                json_result = get_response['tasks'][0]['result']
                if json_result is None and retry < max_retries:
                    retry += 1
                    logger.warning(
                        f'GET. Returned None. [Attempt # {retry}/{max_retries}]. keyword = {i["keyword"]}.')
                    time.sleep(3)
                    continue
                elif json_result is None and retry == max_retries and not resend_post_if_get_failed:
                    logger.warning(
                        f'GET. Skipping... keyword = {i["keyword"]}.')
                    time.sleep(3)
                    break
                elif json_result is None and retry == max_retries and resend_post_if_get_failed:
                    logger.warning(
                        f'GET. Saving to resend... keyword = {i["keyword"]}.')
                    failed_keywords.append(i["keyword"])
                    time.sleep(3)
                    break

                keyword = get_response['tasks'][0]['data']['keyword']
                json_name = f"{hashlib.md5(keyword.encode('utf-8')).hexdigest()}.json"
                json_path = os.path.join(destination_path, json_name)

                keywords_paths_mapped.append(
                    {'keyword': keyword, 'path': json_path})

                logger.info(
                    f'GET. Saving json... keyword = {keyword}, file = {json_path}.')
                with open(json_path, 'w') as f:
                    json.dump(json_result, f)

                break
            else:
                logger.error(
                    f"GET error. Code: {get_response['status_code']} Message: {get_response['status_message']}")
                time.sleep(5)

    os.remove(SAVE_FILE)


def check_kw_in_dir(keyword, directory, keywords_paths_mapped):
    json_name = f"{hashlib.md5(keyword.encode('utf-8')).hexdigest()}.json"

    files = [f for f in os.listdir(directory) if os.path.isfile(
        os.path.join(directory, f))]

    if json_name in files:
        keywords_paths_mapped.append(
            {'keyword': keyword, 'path': os.path.join(directory, json_name)})
        return True

    return False


def save_dataforseo_organic_serps(keywords: List[str],
                                  destination_path: str,
                                  rewrite_serp: bool,
                                  token: str,
                                  max_retries_ready_request: int = 5,
                                  resend_post_if_ready_failed: bool = True,
                                  max_retries_get_request: int = 5,
                                  resend_post_if_get_failed: bool = True,
                                  post_size: int = 80,
                                  lang: str = 'en',
                                  loc: int = 2840,
                                  depth: int = 10) -> List[dict]:

    keywords_copy = keywords.copy()
    client = RestClient(token)
    post_data = dict()
    keywords_paths_mapped = list()
    failed_keywords = list()

    destination_path = f'{destination_path}/{lang}/{loc}'
    os.makedirs(destination_path, exist_ok=True)

    if os.path.exists(SAVE_FILE) and os.path.isfile(SAVE_FILE):
        post_ids_save = pd.read_csv(SAVE_FILE).to_dict('records')
        logger.info(f'SAVED POST. id size = {len(post_ids_save)}')
        post_ids_save = make_ready_request(client, post_ids_save, failed_keywords,
                                           max_retries_ready_request, resend_post_if_ready_failed)
        make_get_request(client, post_ids_save,
                         destination_path, keywords_paths_mapped, failed_keywords, max_retries_get_request, resend_post_if_get_failed)

        if resend_post_if_get_failed or resend_post_if_ready_failed:
            logger.warning(
                f'Failed keywords size = {len(failed_keywords)}, keywords = {failed_keywords}.')
            keywords_copy.extend(failed_keywords)
            failed_keywords.clear()

    while True:

        while True:
            try:
                k = keywords_copy.pop(0)
            except IndexError:
                break

            if not rewrite_serp and check_kw_in_dir(k, destination_path, keywords_paths_mapped):
                logger.warning(f'ALREADY EXISTS. [{k}].')
                continue

            post_data[len(post_data)] = dict(
                language_code=lang,
                location_code=loc,
                keyword=k,
                depth=depth
            )
            if len(post_data) == post_size:
                break

        if len(post_data) > 0:
            post_ids = make_post_request(client, post_data, len(keywords_copy))
            post_ids = make_ready_request(client, post_ids, failed_keywords,
                                          max_retries_ready_request, resend_post_if_ready_failed)
            make_get_request(client, post_ids,
                             destination_path, keywords_paths_mapped, failed_keywords, max_retries_get_request, resend_post_if_get_failed)

            if resend_post_if_get_failed or resend_post_if_ready_failed:
                logger.warning(
                    f'Failed keywords size = {len(failed_keywords)}, keywords = {failed_keywords}.')
                keywords_copy.extend(failed_keywords)
                failed_keywords.clear()

        post_data.clear()
        if not keywords_copy:
            logger.info(f'Finishing DataForSeo session...')
            break

    return keywords_paths_mapped
