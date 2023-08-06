from cryptography.fernet import Fernet
from notesecret.secret import get_md5_str
from notetiktok.data.base import ResourceDetail, SourceDetail, AuthorDetail, ResourceType

resource_db = ResourceDetail()
source_db = SourceDetail()
author_db = AuthorDetail()


def generate_key():
    return Fernet.generate_key().decode()


def encrypt(text, cipher_key="322323"):
    """
    加密，我也没测试过，不知道能不能正常使用，纯字母的应该没问题，中文的待商榷
    :param text: 需要加密的文本
    :param cipher_key: 加密key
    :return: 加密后的文本
    """
    cipher = Fernet(bytes(cipher_key, encoding="utf8"))
    return cipher.encrypt(text.encode()).decode()


def decrypt(encrypted_text, cipher_key="23423423"):
    """
    解密，我也没测试过，不知道能不能正常使用，纯字母的应该没问题，中文的待商榷
    :param cipher_key: 加密key
    :param encrypted_text: 需要解密的文本
    :return:解密后的文本
    """
    cipher = Fernet(bytes(cipher_key, encoding="utf8"))
    return cipher.decrypt(bytes(encrypted_text, encoding='utf8')).decode()


def add_resource(url, resource_id=None, title=None, sub_title=None, content=None, source_url=None, source_id=None,
                 author_id=None, resource_type=0, *args, **kwargs):
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
