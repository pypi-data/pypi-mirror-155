import os
from enum import Enum

from notedrive.sqlalchemy.base import BaseTable, create_engines, meta
from notetool.secret import read_secret
from sqlalchemy import BIGINT, INT, TIMESTAMP, Column, String, Table, func

uri = read_secret(cate1='notetiktok', cate2='dataset', cate3='db_path')
uri = uri or f'sqlite:///{os.path.abspath(os.path.dirname(__file__))}/data/notetiktok.db'

engine = create_engines(uri)


class ResourceType:
    UNKNOWN = 0
    PIC = 1
    VIDEO = 2
    M3U8 = 3


class SourceDetail(BaseTable):
    def __init__(self, table_name="source_detail", *args, **kwargs):
        super(SourceDetail, self).__init__(table_name=table_name, engine=engine, *args, **kwargs)
        self.table = Table(self.table_name, meta,
                           Column('source_id', String, comment='来源ID', primary_key=True),
                           Column('main_url', String, comment='来源网站主页', default='')
                           )
        self.create()


class AuthorDetail(BaseTable):
    def __init__(self, table_name="author_detail", *args, **kwargs):
        super(AuthorDetail, self).__init__(table_name=table_name, engine=engine, *args, **kwargs)
        self.table = Table(self.table_name, meta,
                           Column('source_id', String, comment='来源ID', primary_key=True),
                           Column('author_id', String, comment='用户ID', primary_key=True),
                           Column('gmt_create', TIMESTAMP(True), server_default=func.now()),
                           Column('gmt_modified', TIMESTAMP(True), server_default=func.now()),
                           Column('name', String, comment='名称', default='无名氏'))
        self.create()


class ResourceDetail(BaseTable):
    def __init__(self, table_name="resource_detail", *args, **kwargs):
        super(ResourceDetail, self).__init__(table_name=table_name, engine=engine, *args, **kwargs)
        self.table = Table(self.table_name, meta,
                           Column('source_id', String, comment='来源ID', primary_key=True),
                           Column('resource_id', String, comment='资源ID', primary_key=True),
                           Column('gmt_create', TIMESTAMP(True), server_default=func.now()),
                           Column('gmt_modified', TIMESTAMP(True), server_default=func.now()),
                           Column('resource_type', BIGINT, comment='资源类型', default=0),
                           Column('author_id', String, comment='作者ID', default=''),
                           Column('title', String, comment='标题', default=''),
                           Column('sub_title', String, comment='子标题', default=''),
                           Column('content', String, comment='内容', default=''),
                           Column('url', String, comment='资源地址', default=''),
                           Column('source_url', String, comment='资源原地址', default=''))
        self.create()
