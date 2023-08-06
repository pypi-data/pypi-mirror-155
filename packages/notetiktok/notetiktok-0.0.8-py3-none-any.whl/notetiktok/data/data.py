from notesecret.secret import get_md5_str
from notetiktok.data.base import (AuthorDetail, ResourceDetail, ResourceType,
                                  SourceDetail)

resource_db = ResourceDetail()
source_db = SourceDetail()
author_db = AuthorDetail()


def add_resource_list(url_list, source_id='', author_id='', resource_type=0):
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


def add_image_list(url_list, source_id='', author_id=''):
    add_resource_list(url_list, source_id, author_id, resource_type=ResourceType.PIC)


def add_video_list(url_list, source_id='', author_id=''):
    add_resource_list(url_list, source_id, author_id, resource_type=ResourceType.VIDEO)
