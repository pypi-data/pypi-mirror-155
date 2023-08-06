from typing import Dict

from notesecret import decrypt, encrypt, get_md5_str
from notetiktok.data.base import (AuthorDetail, ResourceDetail, ResourceType,
                                  SourceDetail)

resource_db = ResourceDetail()
source_db = SourceDetail()
author_db = AuthorDetail()


def resource_encrypt(resource: Dict, cipher_key=None):
    if cipher_key is None:
        return resource
    for key in resource.keys():
        value = resource[key]
        if key in ['title', 'sub_title', 'content', 'source_url', 'url']:
            resource[key] = encrypt(value, cipher_key)
    return resource


def resource_decrypt(resource: Dict, cipher_key=None):
    if cipher_key is None:
        return resource
    for key in resource.keys():
        value = resource[key]
        if key in ['title', 'sub_title', 'content', 'source_url', 'url']:
            resource[key] = decrypt(value, cipher_key)
    return resource


def add_resource(url, resource_id=None, title=None, sub_title=None, content=None, source_url=None, source_id=None,
                 author_id=None, resource_type=0, cipher_key=None, *args, **kwargs):
    if source_id:
        source_db.upsert({'source_id': source_id})
    if author_id:
        author_db.upsert({'source_id': source_id, 'author_id': author_id})

    if isinstance(url, list):
        url = ','.join(url)
    resource_json = {
        'url': url,
        'source_id': source_id,
        'resource_id': resource_id or get_md5_str(url),
        'title': title,
        'sub_title': sub_title,
        'content': content,
        'source_url': source_url,
        'author_id': author_id,
        'resource_type': resource_type,
    }
    if cipher_key is not None:
        resource_json = resource_encrypt(resource_json, cipher_key)
    resource_db.upsert(resource_json)


def add_source(source_id, main_url=None, *args, **kwargs):
    source_db.upsert({'source_id': source_id, 'main_url': main_url})


def add_author(author_id, source_id=None, name='', *args, **kwargs):
    author_db.upsert({'source_id': source_id, 'author_id': author_id, 'name': name})


def add_image(url, resource_id=None, title=None, sub_title=None, content=None, source_url=None, source_id=None,
              author_id=None, *args, **kwargs):
    add_resource(url,
                 resource_id=resource_id,
                 title=title,
                 sub_title=sub_title,
                 content=content,
                 source_url=source_url,
                 source_id=source_id,
                 author_id=author_id,
                 resource_type=ResourceType.PIC)


def add_video(url, resource_id=None, title=None, sub_title=None, content=None, source_url=None, source_id=None,
              author_id=None, *args, **kwargs):
    add_resource(url,
                 resource_id=resource_id,
                 title=title,
                 sub_title=sub_title,
                 content=content,
                 source_url=source_url,
                 source_id=source_id,
                 author_id=author_id,
                 resource_type=ResourceType.VIDEO)


def add_resource_list(url_list, source_id='', author_id='', resource_type=0, *args, **kwargs):
    data = []
    if source_id:
        source_db.upsert({'source_id': source_id})
    if author_id:
        author_db.upsert({'source_id': source_id, 'author_id': author_id})
    for resource in url_list:
        if isinstance(resource, list):
            resource = ','.join(resource)
        resource_json = {
            'source_id': source_id,
            'author_id': author_id,
            'resource_type': resource_type,
            'resource_id': get_md5_str(resource),
            'url': resource
        }
        data.append(resource_json)
    resource_db.upsert(data)


def add_image_list(url_list, source_id='', author_id='', *args, **kwargs):
    add_resource_list(url_list, source_id, author_id, resource_type=ResourceType.PIC)


def add_video_list(url_list, source_id='', author_id='', *args, **kwargs):
    add_resource_list(url_list, source_id, author_id, resource_type=ResourceType.VIDEO)
