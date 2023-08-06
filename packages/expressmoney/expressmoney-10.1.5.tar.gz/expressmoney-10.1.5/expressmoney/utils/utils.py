__all__ = ('get_secret', 'timeit', 'get')

import time

from django.conf import settings
from google.cloud import secretmanager
from google.cloud import secretmanager_v1

from expressmoney.utils.requests import Request

secret_manager_client = secretmanager.SecretManagerServiceClient()
access_secret_version = secretmanager_v1.types.service.AccessSecretVersionRequest()


def get_secret(secret_key: str):
    name = f'projects/{"1086735462412" if settings.IS_PROD else "506185804933"}/secrets/{secret_key}/versions/1'
    access_secret_version.name = name
    return secret_manager_client.access_secret_version(request=access_secret_version).payload.data.decode("utf-8")


def timeit(method):
    def wrapper(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))
        return result

    return wrapper


def get(service: str, path: str, read_pages: int = 1) -> list:
    data = list()
    pages_readed = 0
    next_page_is_exists = True
    while next_page_is_exists and (pages_readed < read_pages or read_pages == 0):
        response = Request(service=service, path=f'{path}?page={pages_readed + 1}').get()
        page_data = response.json().get('results')
        next_page_is_exists = True if response.json().get('next') is not None else False
        if page_data:
            data.extend(page_data)
        pages_readed += 1
    return data
