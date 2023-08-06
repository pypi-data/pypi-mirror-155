from fastapi import APIRouter
from notebuild.tool.fastapi import add_api_routes, api_route
from notetiktok.data import (ResourceType, add_favorite, add_follow,
                             add_resource, favorite_db, follow_db, resource_db)


class ResourceService(APIRouter):
    def __init__(self, prefix='/tiktok/resource', *args, **kwargs):
        super(ResourceService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    @api_route('/get', description="get value")
    def get_resource(self, page_no: int = 1, page_size: int = 10):
        return resource_db.get_resource(start=page_size * (page_no - 1),
                                        stop=page_size * page_no,
                                        resource_type=ResourceType.VIDEO)

    @api_route('/add/video', description="add video")
    def add_video(self, url, resource_id=None, title=None, sub_title=None, content=None, source_url=None,
                  source_id=None, author_id=None, *args, **kwargs):
        add_resource(url,
                     resource_id=resource_id,
                     title=title,
                     sub_title=sub_title,
                     content=content,
                     source_url=source_url,
                     source_id=source_id,
                     author_id=author_id,
                     resource_type=ResourceType.VIDEO, **kwargs)

    @api_route('/add/image', description="add image")
    def add_image(self, url, resource_id=None, title=None, sub_title=None, content=None, source_url=None,
                  source_id=None, author_id=None, **kwargs):
        add_resource(url,
                     resource_id=resource_id,
                     title=title,
                     sub_title=sub_title,
                     content=content,
                     source_url=source_url,
                     source_id=source_id,
                     author_id=author_id,
                     resource_type=ResourceType.PIC, **kwargs)


class FavoriteService(APIRouter):
    def __init__(self, prefix='/tiktok/favorite', *args, **kwargs):
        super(FavoriteService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    @api_route('/get', description="get value")
    def get_favorite(self, start=0, stop=20, user_id=None, source_id=None):
        return favorite_db.get_favor(start=start, stop=stop, user_id=user_id, source_id=source_id)

    @api_route('/add', description="add video")
    def add_favorite(self, user_id, resource_id, source_id=None):
        add_favorite(user_id=user_id, resource_id=resource_id, source_id=source_id)


class FollowService(APIRouter):
    def __init__(self, prefix='/tiktok/follow', *args, **kwargs):
        super(FollowService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    @api_route('/get', description="get value")
    def get_follow(self, start=0, stop=20, user_id=None, source_id=None):
        return follow_db.get_following(start=start, stop=stop, user_id=user_id, source_id=source_id)

    @api_route('/add', description="add video")
    def add_follow(self, user_id, author_id, source_id=None):
        add_follow(user_id=user_id, author_id=author_id, source_id=source_id)
