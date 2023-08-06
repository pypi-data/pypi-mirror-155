"""
The HEA Volumes Microservice provides ...
"""
from heaobject.folder import Folder, Item
from heaserver.service import client, response, appproperty
from heaserver.service.appproperty import HEA_DB
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaserver.service.heaobjectsupport import type_to_resource_url
from heaserver.service.oidcclaimhdrs import SUB
from heaobject.volume import Volume, FileSystem
from yarl import URL

MONGODB_VOLUME_COLLECTION = 'volumes'
MONGODB_FILE_SYSTEM_COLLECTION = 'filesystems'


@routes.get('/volumes/{id}')
@action('heaserver-volumes-volume-get-properties', rel='properties')
@action('heaserver-volumes-volume-get-open-choices', rel='hea-opener-choices', path='/volumes/{id}/opener')
@action('heaserver-volumes-volume-duplicate', rel='duplicator', path='/volumes/{id}/duplicator')
async def get_volume(request: web.Request) -> web.Response:
    """
    Gets the volume with the specified id.
    :param request: the HTTP request.
    :return: the requested volume or Not Found.
    ---
    summary: A specific volume.
    tags:
        - heaserver-volumes-get-volume
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes/{id}/content')
async def get_volume_content(request: web.Request) -> web.Response:
    """
    Gets the content of the volume with the given id.
    :param request: the HTTP request.
    :return: the contents of the volume or Not Found.
    ---
    summary: A specific volume's contents.
    tags:
        - heaserver-volumes-get-volume-content
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    volume_dict = await request.app[HEA_DB].get(request, MONGODB_VOLUME_COLLECTION, var_parts='id')
    if volume_dict is None:
        return response.status_not_found()
    volume = Volume()
    volume.from_dict(volume_dict)
    if volume.folder_id is None:
        return response.status_not_found()
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
    url = await type_to_resource_url(request, Folder, volume.file_system_type, volume.file_system_name)
    if url is None:
        raise ValueError(f'No folder service registered for file system type {volume.file_system_type} and file system name {volume.file_system_name}')
    items = [i.to_dict() async for i in client.get_all(request.app, URL(url) / volume.folder_id / 'items', Item, headers=headers)]
    return await response.get_all(request, items)


@routes.get('/volumes/byname/{name}')
async def get_volume_by_name(request: web.Request) -> web.Response:
    """
    Gets the volume with the specified id.
    :param request: the HTTP request.
    :return: the requested volume or Not Found.
    ---
    summary: A specific volume.
    tags:
        - heaserver-volumes-get-volume-by-name
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get_by_name(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes')
@routes.get('/volumes/')
@action('heaserver-volumes-volume-get-properties', rel='properties')
@action('heaserver-volumes-volume-get-open-choices', rel='hea-opener-choices', path='/volumes/{id}/opener')
@action('heaserver-volumes-volume-duplicate', rel='duplicator', path='/volumes/{id}/duplicator')
async def get_all_volumes(request: web.Request) -> web.Response:
    """
    Gets all volumes.
    :param request: the HTTP request.
    :return: all volumes.
    ---
    summary: All volumes.
    tags:
        - heaserver-volumes-get-all-volumes
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    return await mongoservicelib.get_all(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes/{id}/duplicator')
@action(name='heaserver-volumes-volume-duplicate-form', path='/volumes/{id}')
async def get_volume_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested volume.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested volume was not found.
    """
    return await mongoservicelib.get(request, MONGODB_VOLUME_COLLECTION)


@routes.post('/volume/duplicator')
async def post_volume_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided volume for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_VOLUME_COLLECTION, Volume)


@routes.post('/volumes')
@routes.post('/volumes/')
async def post_volume(request: web.Request) -> web.Response:
    """
    Posts the provided volume.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the Location header.
    ---
    summary: Volume creation
    tags:
        - heaserver-volumes-post-volume
    requestBody:
      description: A new volume object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: A volume
              value: {
                "template": {
                  "data": [
                    {
                      "name": "created",
                      "value": null
                    },
                    {
                      "name": "derived_by",
                      "value": null
                    },
                    {
                      "name": "derived_from",
                      "value": []
                    },
                    {
                      "name": "description",
                      "value": null
                    },
                    {
                      "name": "display_name",
                      "value": "Joe"
                    },
                    {
                      "name": "invited",
                      "value": []
                    },
                    {
                      "name": "modified",
                      "value": null
                    },
                    {
                      "name": "file_system_type",
                      "value": "heaobject.volume.DefaultFileSystem"
                    },
                    {
                      "name": "file_system_name",
                      "value": "DEFAULT_FILE_SYSTEM"
                    },
                    {
                      "name": "owner",
                      "value": "system|none"
                    },
                    {
                      "name": "shares",
                      "value": []
                    },
                    {
                      "name": "source",
                      "value": null
                    },
                    {
                      "name": "version",
                      "value": null
                    }
                  ]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: A volume
              value: {
                "created": None,
                "derived_by": None,
                "derived_from": [],
                "description": None,
                "display_name": "Joe",
                "invited": [],
                "modified": None,
                "file_system_type": "heaobject.volume.DefaultFileSystem",
                "file_system_name": "DEFAULT_FILE_SYSTEM",
                "owner": NONE_USER,
                "shares": [],
                "source": None,
                "type": "heaobject.volume.Volume",
                "version": None
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.post(request, MONGODB_VOLUME_COLLECTION, Volume)


@routes.put('/volumes/{id}')
async def put_volume(request: web.Request) -> web.Response:
    """
    Updates the volume with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    ---
    summary: Volume updates
    tags:
        - heaserver-volumes-put-volume
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
      description: An updated volume object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: A volume
              value: {
                "template": {
                  "data": [
                    {
                      "name": "created",
                      "value": null
                    },
                    {
                      "name": "derived_by",
                      "value": null
                    },
                    {
                      "name": "derived_from",
                      "value": []
                    },
                    {
                      "name": "description",
                      "value": null
                    },
                    {
                      "name": "display_name",
                      "value": "Reximus Max"
                    },
                    {
                      "name": "invited",
                      "value": []
                    },
                    {
                      "name": "modified",
                      "value": null
                    },
                    {
                      "name": "file_system_type",
                      "value": "heaobject.volume.DefaultFileSystem"
                    },
                    {
                      "name": "file_system_name",
                      "value": "DEFAULT_FILE_SYSTEM"
                    },
                    {
                      "name": "owner",
                      "value": "system|none"
                    },
                    {
                      "name": "shares",
                      "value": []
                    },
                    {
                      "name": "source",
                      "value": null
                    },
                    {
                      "name": "version",
                      "value": null
                    },
                    {
                      "name": "id",
                      "value": "666f6f2d6261722d71757578"
                    }
                  ]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: A volume
              value: {
                "created": None,
                "derived_by": None,
                "derived_from": [],
                "description": None,
                "display_name": "Reximus Max",
                "invited": [],
                "modified": None,
                "file_system_type": "heaobject.volume.DefaultFileSystem",
                "file_system_name": "DEFAULT_FILE_SYSTEM",
                "owner": NONE_USER,
                "shares": [],
                "source": None,
                "type": "heaobject.volume.Volume",
                "version": None,
                "id": "666f6f2d6261722d71757578"
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.put(request, MONGODB_VOLUME_COLLECTION, Volume)


@routes.delete('/volumes/{id}')
async def delete_volume(request: web.Request) -> web.Response:
    """
    Deletes the volume with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Volume deletion
    tags:
        - heaserver-volumes-delete-volume
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.delete(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes/{id}/opener')
@action('heaserver-volumes-volume-open-default', rel='hea-opener hea-default application/x.folder', path='/volumes/{id}/content')
async def get_volume_opener(request: web.Request) -> web.Response:
    """

    :param request: the HTTP Request.
    :return: A Response object with a status of Multiple Choices or Not Found.
    ---
    summary: Volume opener choices
    tags:
        - heaserver-volumes-get-volume-open-choices
    parameters:
      - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.opener(request, MONGODB_VOLUME_COLLECTION)


@routes.get('/volumes/byfilesystemtype/{type}/byfilesystemname/{name}')
@routes.get('/volumes/byfilesystemtype/{type}/byfilesystemname/{name}/')
async def get_volumes_by_file_system_type_and_name(request: web.Request) -> web.Response:
    """
    Gets the volumes with the given file system type and name for the current user.

    :param request: the HTTP request.
    :return: the requested volumes or the empty list.
    ---
    summary: A list of volumes.
    tags:
        - heaserver-volumes-get-volumes-by-file-system-type-and-name
    parameters:
        - name: type
          in: path
          required: true
          description: The file system type of the volumes to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A file system type
              value: heaobject.volume.DefaultFileSystem
        - name: name
          in: path
          required: true
          description: The file system name of the volumes to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A file system name
              value: DEFAULT_FILE_SYSTEM
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    result = await request.app[appproperty.HEA_DB].get_all(request,
                                                       MONGODB_VOLUME_COLLECTION,
                                                       mongoattributes={
                                                           'file_system_type': {'$eq': request.match_info['type']},
                                                           'file_system_name': {'$eq': request.match_info['name']}
                                                       }, sub=request.headers.get(SUB))
    return await response.get_all(request, result)


@routes.get('/volumes/byfilesystemtype/{type}')
@routes.get('/volumes/byfilesystemtype/{type}/')
async def get_volumes_by_file_system_type(request: web.Request) -> web.Response:
    """
    Gets the volumes with the given file system type and the default file system of that type for the current user.

    :param request: the HTTP request.
    :return: the requested volumes or the empty list.
    ---
    summary: A list of volumes.
    tags:
        - heaserver-volumes-get-volumes-by-file-system-type-and-name
    parameters:
        - name: type
          in: path
          required: true
          description: The file system type of the volumes to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A file system type
              value: heaobject.volume.DefaultFileSystem
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    result = await request.app[appproperty.HEA_DB].get_all(request,
                                                       MONGODB_VOLUME_COLLECTION,
                                                       mongoattributes={
                                                           'file_system_type': {'$eq': request.match_info['type']},
                                                           'file_system_name': {'$eq': 'DEFAULT_FILE_SYSTEM'}
                                                       }, sub=request.headers.get(SUB))
    return await response.get_all(request, result)


@routes.get('/filesystems/{id}')
@action('heaserver-volumes-file-system-get-properties', rel='properties')
@action('heaserver-volumes-file-system-duplicate', rel='duplicator', path='/filesystems/{id}/duplicator')
async def get_file_system(request: web.Request) -> web.Response:
    """
    Gets the file system with the specified id.
    TODO: pick the actions depending on the actual file system type?

    :param request: the HTTP request.
    :return: the requested file system or Not Found.
    ---
    summary: A specific file system.
    tags:
        - heaserver-volumes-get-file-system
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get(request, MONGODB_FILE_SYSTEM_COLLECTION)


@routes.get('/filesystems/bytype/{type}/byname/{name}')
async def get_file_system_by_type_and_name(request: web.Request) -> web.Response:
    """
    Gets the file system with the specified type and name.
    TODO: make one of these functions per file system type, and hard code the type parameter.

    :param request: the HTTP request.
    :return: the requested file system or Not Found.
    ---
    summary: A specific file system.
    tags:
        - heaserver-volumes-get-file-system-by-type-and-name
    parameters:
        - name: type
          in: path
          required: true
          description: The file system type to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A file system type
              value: heaobject.volume.AWSFileSystem
        - name: name
          in: path
          required: true
          description: The file system name to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A file system name
              value: DEFAULT_FILE_SYSTEM
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    result = await request.app[appproperty.HEA_DB].get(request,
                                                       MONGODB_FILE_SYSTEM_COLLECTION,
                                                       mongoattributes={
                                                               'type': {'$eq': request.match_info['type']},
                                                               'name': {'$eq': request.match_info['name']}
                                                           }, sub=request.headers.get(SUB))
    return await response.get(request, result)


@routes.get('/filesystems')
@routes.get('/filesystems/')
@action('heaserver-volumes-file-system-get-properties', rel='properties')
@action('heaserver-volumes-file-system-duplicate', rel='duplicator', path='/filesystems/{id}/duplicator')
async def get_all_file_systems(request: web.Request) -> web.Response:
    """
    Gets all file systems.
    :param request: the HTTP request.
    :return: all file systems.
    ---
    summary: All file systems.
    tags:
        - heaserver-volumes-get-all-file-systems
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    return await mongoservicelib.get_all(request, MONGODB_FILE_SYSTEM_COLLECTION)


@routes.get('/filesystems/{id}/duplicator')
@action(name='heaserver-volumes-file-system-duplicate-form', path='/filesystems/{id}')
async def get_file_system_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested file system.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested file system was not found.
    """
    return await mongoservicelib.get(request, MONGODB_FILE_SYSTEM_COLLECTION)


@routes.post('/filesystems/duplicator')
async def post_file_system_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided file system for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the Location header
    FIXME: Parse the body for a type field to pass into mongoservicelib.post().
    """
    return await mongoservicelib.post(request, MONGODB_FILE_SYSTEM_COLLECTION, FileSystem)


@routes.post('/filesystems')
@routes.post('/filesystems/')
async def post_file_system(request: web.Request) -> web.Response:
    """
    Posts the provided file system.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the Location header.
    ---
    summary: File system creation
    tags:
        - heaserver-volumes-post-file-system
    requestBody:
      description: A new file system object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: A file system
              value: {
                "template": {
                  "data": [
                    {
                      "name": "created",
                      "value": null
                    },
                    {
                      "name": "derived_by",
                      "value": null
                    },
                    {
                      "name": "derived_from",
                      "value": []
                    },
                    {
                      "name": "description",
                      "value": "Access to Amazon Web Services (AWS)"
                    },
                    {
                      "name": "display_name",
                      "value": "Amazon Web Services"
                    },
                    {
                      "name": "invited",
                      "value": []
                    },
                    {
                      "name": "modified",
                      "value": null
                    },
                    {
                      "name": "name",
                      "value": "aws_file_system"
                    },
                    {
                      "name": "owner",
                      "value": "system|none"
                    },
                    {
                      "name": "shares",
                      "value": []
                    },
                    {
                      "name": "source",
                      "value": null
                    },
                    {
                      "name": "version",
                      "value": null
                    }
                  ]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: A file system
              value: {
                'created': None,
                'derived_by': None,
                'derived_from': [],
                'description': Access to Amazon Web Services (AWS),
                'display_name': 'Amazon Web Services',
                'invited': [],
                'modified': None,
                'name': 'aws_file_system',
                'owner': NONE_USER,
                'shares': [],
                'source': None,
                'type': 'heaobject.volume.AWSFileSystem',
                'version': None
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.post(request, MONGODB_FILE_SYSTEM_COLLECTION, FileSystem)


@routes.put('/filesystems/{id}')
async def put_file_system(request: web.Request) -> web.Response:
    """
    Updates the file system with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    ---
    summary: File system updates
    tags:
        - heaserver-volumes-put-file-system
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
      description: An updated file system object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: A file system
              value: {
                "template": {
                  "data": [
                    {
                      "name": "created",
                      "value": null
                    },
                    {
                      "name": "derived_by",
                      "value": null
                    },
                    {
                      "name": "derived_from",
                      "value": []
                    },
                    {
                      "name": "description",
                      "value": "Amazon Web Services (AWS) - updated description"
                    },
                    {
                      "name": "display_name",
                      "value": "Amazon Web Services - updated display name"
                    },
                    {
                      "name": "invited",
                      "value": []
                    },
                    {
                      "name": "modified",
                      "value": null
                    },
                    {
                      "name": "name",
                      "value": "aws_file_system"
                    },
                    {
                      "name": "owner",
                      "value": "system|none"
                    },
                    {
                      "name": "shares",
                      "value": []
                    },
                    {
                      "name": "source",
                      "value": null
                    },
                    {
                      "name": "version",
                      "value": null
                    },
                    {
                      "name": "id",
                      "value": "666f6f2d6261722d71757578"
                    }
                  ]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: A volume
              value: {
                'created': None,
                'derived_by': None,
                'derived_from': [],
                'description': 'Amazon Web Services (AWS) - updated description',
                'display_name': 'Amazon Web Services - updated display name',
                'invited': [],
                'modified': None,
                'name': 'aws_file_system',
                'owner': NONE_USER,
                'shares': [],
                'source': None,
                'type': 'heaobject.volume.AWSFileSystem',
                'version': None,
                'id': '666f6f2d6261722d71757578'
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.put(request, MONGODB_FILE_SYSTEM_COLLECTION, FileSystem)


@routes.delete('/filesystems/{id}')
async def delete_file_system(request: web.Request) -> web.Response:
    """
    Deletes the file system with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: File system deletion
    tags:
        - heaserver-volumes-delete-file-system
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.delete(request, MONGODB_FILE_SYSTEM_COLLECTION)


def main() -> None:
    config = init_cmd_line(description='The HEA volumes service',
                           default_port=8080)
    start(db=mongo.MongoManager, wstl_builder_factory=builder_factory(__package__), config=config)
