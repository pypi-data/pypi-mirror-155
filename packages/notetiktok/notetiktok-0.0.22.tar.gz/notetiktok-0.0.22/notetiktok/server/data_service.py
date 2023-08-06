from fastapi import APIRouter
from notebuild.tool.fastapi import add_api_routes, api_route
from notetiktok.data import ResourceType, resource_db


class ResourceService(APIRouter):
    def __init__(self, prefix='/resource', *args, **kwargs):
        super(ResourceService, self).__init__(prefix=prefix, *args, **kwargs)
        add_api_routes(self)

    @api_route('/get', description="get value")
    def get_resource(self, page_no:int=1, page_size:int=10):
        return resource_db.get_resource(start=page_size * (page_no - 1),
                                        stop=page_size * page_no,
                                        resource_type=ResourceType.VIDEO)
