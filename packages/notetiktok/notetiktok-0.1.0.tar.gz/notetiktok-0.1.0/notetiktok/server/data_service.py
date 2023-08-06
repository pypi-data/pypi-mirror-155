from fastapi import APIRouter
from notebuild.tool.fastapi import add_api_routes, api_route
from notetiktok.data import ResourceType, resource_db
from notetiktok.data.core import (add_favorite, add_follow, add_image,
                                  add_video, favorite_db, follow_db)


class ResourceService(APIRouter):
    def __init__(self, prefix='/resource', *args, **kwargs):
        super(ResourceService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    @api_route('/get', description="get value")
    def get_resource(self, page_no: int = 1, page_size: int = 10):
        return resource_db.get_resource(start=page_size * (page_no - 1),
                                        stop=page_size * page_no,
                                        resource_type=ResourceType.VIDEO)

    @api_route('/add/video', description="add video")
    def add_video(self, *args, **kwargs):
        add_video(*args, **kwargs)

    @api_route('/add/image', description="add image")
    def add_image(self, *args, **kwargs):
        add_image(*args, **kwargs)


class FavoriteService(APIRouter):
    def __init__(self, prefix='/favorite', *args, **kwargs):
        super(FavoriteService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    # @api_route('/get', description="get value")
    # def get_favorite(self, *args, **kwargs):
    #     return favorite_db.get_favor(*args, **kwargs)

    # @api_route('/add', description="add video")
    # def add_favorite(self, *args, **kwargs):
    #     add_favorite(*args, **kwargs)


class FollowService(APIRouter):
    def __init__(self, prefix='/follow', *args, **kwargs):
        super(FollowService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    # @api_route('/get', description="get value")
    # def get_follow(self, *args, **kwargs):
    #     return follow_db.get_following(*args, **kwargs)

    # @api_route('/add', description="add video")
    # def add_follow(self, *args, **kwargs):
    #     add_follow(*args, **kwargs)
