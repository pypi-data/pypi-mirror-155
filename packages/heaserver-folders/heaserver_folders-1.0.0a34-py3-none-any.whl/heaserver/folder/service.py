from heaserver.service.runner import init_cmd_line, routes, start
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaserver.service import response, appproperty
from heaserver.service.heaobjectsupport import new_heaobject_from_type, PermissionGroup, has_permissions
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.appproperty import HEA_DB
from heaobject.folder import Folder, Item
from heaobject.error import DeserializeException
from heaobject.root import ShareImpl
from heaobject.user import ALL_USERS
from aiohttp import web
from aiohttp.client_exceptions import ClientResponseError
import logging


_logger = logging.getLogger(__name__)

MONGODB_FOLDER_COLLECTION = 'folders'
MONGODB_ITEMS_COLLECTION = 'folders_items'

ROOT_FOLDER = Folder()
ROOT_FOLDER.id = 'root'
_root_share = ShareImpl()
_root_share.user = ALL_USERS
_root_share.permissions = PermissionGroup.POSTER_PERMS.perms
ROOT_FOLDER.shares = [_root_share]


@routes.get('/folders/{folder_id}/items')
@routes.get('/folders/{folder_id}/items/')
@action(name='heaserver-folders-item-move', path='/folders/{folder_id}/items/{id}/mover', rel='hea-mover')
@action(name='heaserver-folders-item-duplicate', rel='hea-duplicator', path='/folders/{folder_id}/items/{id}/duplicator')
@action(name='heaserver-folders-item-get-actual', rel='hea-actual', path='{+actual_object_uri}', root='')
async def get_items(request: web.Request) -> web.Response:
    """
    Gets the items of the folder with the specified id.
    :param request: the HTTP request.
    :return: the requested items, or Not Found if the folder was not found.
    ---
    summary: All items in a folder.
    tags:
        - heaserver-folders-get-all-folder-items
    parameters:
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    responses:
      '200':
        $ref: '#/components/responses/200'
    """
    folder = request.match_info['folder_id']
    _logger.debug('Requested items from the "%s" folder', folder)
    items = await request.app[appproperty.HEA_DB].get_all(request,
                                                          MONGODB_ITEMS_COLLECTION,
                                                          var_parts='folder_id',
                                                          sub=request.headers.get(SUB))
    _logger.debug('got items from mongo: %s', items)
    return await response.get_all(request, items)


@routes.get('/folders/{folder_id}/items/{id}')
@action(name='heaserver-folders-item-move', path='/folders/{folder_id}/items/{id}/mover', rel='hea-mover')
@action(name='heaserver-folders-item-duplicate', rel='hea-duplicator', path='/folders/{folder_id}/items/{id}/duplicator')
@action(name='heaserver-folders-item-get-actual', rel='hea-actual', path='{+actual_object_uri}', root='')  # Maybe have a different syntax when we do not want to encode.
async def get_item(request: web.Request) -> web.Response:
    """
    Gets the requested item from the given folder.

    :param request: the HTTP request. Required.
    :return: the requested item, or Not Found if it was not found.
    ---
    summary: A specific folder item.
    tags:
        - heaserver-folders-get-folder-item
    parameters:
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_item_response(request)


@routes.get('/folders/{folder_id}/items/{id}/duplicator')
@action(name='heaserver-folders-item-duplicate-form', path='/folders/{folder_id}/items/{id}')
async def get_item_duplicator(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested item.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested item was not found.
    """
    return await _get_item_response(request)


@routes.get('/folders/{id}/duplicator')
@action(name='heaserver-folders-folder-duplicate-form', path='/folders/{folder_id}/items/{id}')
async def get_folder_duplicator(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested folder.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested folder was not found.
    """
    return await _get_folder(request)


@routes.post('/folders/{folder_id}/duplicator')
async def post_item_duplicator(request: web.Request) -> web.StreamResponse:
    """
    Posts the provided item for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await post_item_in_folder(request)


@routes.get('/folders/{folder_id}/items/{id}/mover')
@action(name='heaserver-folders-item-move-form', path='/folders/{folder_id}/items/{id}')
async def get_item_mover(request: web.Request) -> web.Response:
    """
    Gets a form template for moving the requested item.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested item was not found.
    """
    return await _get_item_response(request)


@routes.post('/folders/{folder_id}/mover')
async def post_item_mover(request: web.Request) -> web.StreamResponse:
    """
    Posts the provided item for moving.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await put_item_in_folder(request)


@routes.post('/folders/{folder_id}/items')
@routes.post('/folders/{folder_id}/items/')
async def post_item_in_folder(request: web.Request) -> web.Response:
    """
    Creates a new folder item.

    :param request: the HTTP request. The body of the request is expected to be an item or an actual object.
    :return: the response, with a 204 status code if an item was created or a 400 if not. If an item was created, the
    Location header will contain the URL of the created item.
    ---
    summary: A specific folder item.
    tags:
        - heaserver-folders-post-folder-item
    parameters:
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
    requestBody:
        description: A new folder item object.
        required: true
        content:
            application/vnd.collection+json:
              schema:
                type: object
              examples:
                example:
                  summary: Organization example
                  value: {
                    "template": {
                      "data": [{
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
                        "name": "name",
                        "value": "joe"
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
                        "name": "folder_id",
                        "value": "root"
                      },
                      {
                        "name": "actual_object_id",
                        "value": "666f6f2d6261722d71757578"
                      },
                      {
                        "name": "actual_object_type_name",
                        "value": "heaobject.registry.Component"
                      },
                      {
                        "name": "actual_object_uri",
                        "value": "/components/666f6f2d6261722d71757578"
                      }]
                    }
                  }
            application/json:
              schema:
                type: object
              examples:
                example:
                  summary: Organization example
                  value: {
                    "created": null,
                    "derived_by": null,
                    "derived_from": [],
                    "description": null,
                    "display_name": "Joe",
                    "invited": [],
                    "modified": null,
                    "name": "joe",
                    "owner": "system|none",
                    "shares": [],
                    "source": null,
                    "type": "heaobject.folder.Item",
                    "version": null,
                    "folder_id": "root",
                    "actual_object_id": "666f6f2d6261722d71757578",
                    "actual_object_type_name": "heaobject.registry.Component",
                    "actual_object_uri": "/folders/666f6f2d6261722d71757578"
                  }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB)

    # Check permissions on the folder
    if request.match_info['folder_id'] == ROOT_FOLDER.id:
        folder = ROOT_FOLDER
    else:
        folder = Folder()
        folder_dict = await request.app[HEA_DB].get(request, MONGODB_FOLDER_COLLECTION, var_parts='folder_id', sub=sub)
        if folder_dict is None:
            return response.status_not_found()
        folder.from_dict(folder_dict)

    if not has_permissions(folder, sub, PermissionGroup.POSTER_PERMS.perms):
        return response.status_bad_request(f'400: Bad Request; Permission denied')
    try:
        item = await new_heaobject_from_type(request, Item)
    except DeserializeException as e:
        return response.status_bad_request(f'400: Bad Request; {e}')
    try:
        if item.folder_id is None:
            item.folder_id = request.match_info['folder_id']
        elif request.match_info['folder_id'] != item.folder_id:
            return response.status_bad_request(body='400: Bad Request; Invalid folder_id')
        if item.actual_object_type_name is None:
            return response.status_bad_request(body='400: Bad Request; actual_object_type_name is required')
        if item.actual_object_id is None:
            return response.status_bad_request(body='400: Bad Request; actual_object_id is required')
        if item.actual_object_uri is None:
            return response.status_bad_request(body='400: Bad Request; actual_object_uri is required')
        result = await request.app[appproperty.HEA_DB].post(request, item, MONGODB_ITEMS_COLLECTION)
        return await response.post(request, result, MONGODB_ITEMS_COLLECTION)
    except ClientResponseError as e:
        return response.status_from_exception(e)



@routes.put('/folders/{folder_id}/items/{id}')
async def put_item_in_folder(request: web.Request) -> web.Response:
    """
    Updates the item with the specified id.

    :param request: the HTTP request. The body of the request may be an item, optionally with the actual object, or
    just the actual object. If the body contains an item without the actual object, HEA assumes that the item should
    continue to associate with the same actual object as before.
    :return: No Content or Not Found.
    ---
    summary: Folder item updates
    tags:
        - heaserver-folders-put-folder-item
    parameters:
        - name: folder_id
          in: path
          required: true
          description: The id of the folder to retrieve.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    requestBody:
      description: An updated folder item object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Folder item example
              value: {
                "template": {
                  "data": [{
                    "name": "id",
                    "value": "666f6f2d6261722d71757578"
                  },
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
                    "value": "Bob"
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
                    "value": "bob"
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
                    "name": "folder_id",
                    "value": "root"
                  },
                  {
                    "name": "actual_object_id",
                    "value": "666f6f2d6261722d71757578"
                  },
                  {
                    "name": "actual_object_type_name",
                    "value": "heaobject.registry.Component"
                  },
                  {
                    "name": "actual_object_uri",
                    "value": "/components/666f6f2d6261722d71757578"
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Folder item example
              value: {
                "id": "666f6f2d6261722d71757578",
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": null,
                "display_name": "Bob",
                "invited": [],
                "modified": null,
                "name": "bob",
                "owner": "system|none",
                "shares": [],
                "source": null,
                "type": "heaobject.folder.Item",
                "version": null,
                "folder_id": "root",
                "actual_object_id": "666f6f2d6261722d71757578",
                "actual_object_type_name": "heaobject.registry.Component",
                "actual_object_uri": "/folders/666f6f2d6261722d71757578"
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    sub = request.headers.get(SUB)
    if request.content_length == 0:
        return response.status_bad_request('400: Bad Request; Empty body')
    old_item_dict = await request.app[appproperty.HEA_DB].get(request, MONGODB_ITEMS_COLLECTION,
                                                          var_parts=['folder_id', 'id'])
    if old_item_dict is None:
        return response.status_not_found()
    old_item = Item()
    old_item.from_dict(old_item_dict)
    if not has_permissions(old_item, sub, PermissionGroup.PUTTER_PERMS.perms):
        return response.status_bad_request(body='400: Bad Request; Permission denied')

    try:
        item = await new_heaobject_from_type(request, Item)
        if item.id != request.match_info['id']:
            return response.status_bad_request(body='400: Bad Request; Invalid id')
        if item.folder_id != request.match_info['folder_id']:
            return response.status_bad_request(body='400: Bad Request; Invalid folder_id')
        if item.actual_object_type_name is None:
            return response.status_bad_request(body='400: Bad Request; actual_object_type_name property is required')
        if item.actual_object_id is None:
            return response.status_bad_request(body='400: Bad Request; actual_object_id property is required')
        if item.actual_object_uri is None:
            return response.status_bad_request()
        result = await request.app[appproperty.HEA_DB].put(request, item, MONGODB_ITEMS_COLLECTION)
        return await response.put(result)
    except ClientResponseError as e:
        return response.status_from_exception(e)
    except DeserializeException as e:
        return response.status_bad_request(f'400: Bad Request; {e}')


@routes.delete('/folders/{folder_id}/items/{id}')
async def delete_item(request: web.Request) -> web.Response:
    """
    Deletes the item with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder item deletion
    tags:
        - heaserver-folders-delete-folder-item
    parameters:
        - name: folder_id
          in: path
          required: true
          description: The id of the folder.
          schema:
            type: string
          examples:
            example:
              summary: A folder id
              value: root
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    _logger.debug('Deleting item %s from folder %s', request.match_info['id'], request.match_info['folder_id'])
    sub = request.headers.get(SUB)
    result = await request.app[appproperty.HEA_DB].delete(request, MONGODB_ITEMS_COLLECTION,
                                                          var_parts=['folder_id', 'id'], sub=sub)
    return await response.delete(result.deleted_count if result else False)


@routes.get('/folders/{id}')
@action(name='heaserver-folders-folder-get-open-choices', path='/folders/{id}/opener',
        rel='hea-opener-choices')
@action(name='heaserver-folders-folder-get-properties', rel='hea-properties')
@action(name='heaserver-folders-folder-duplicate', rel='hea-duplicator', path='/folders/{id}/duplicator')
async def get_folder(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.
    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-folders-post-folder
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await _get_folder(request)


@routes.get('/folders/byname/{name}')
async def get_folder_by_name(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified name.
    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-folders-get-folder-by-name
    parameters:
        - $ref: '#/components/parameters/name'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get_by_name(request, MONGODB_FOLDER_COLLECTION)


@routes.get('/folders')
@routes.get('/folders/')
@action(name='heaserver-folders-folder-get-open-choices', path='/folders/{id}/opener',
        rel='hea-opener-choices')
@action(name='heaserver-folders-folder-get-properties', rel='hea-properties')
@action(name='heaserver-folders-folder-duplicate', rel='hea-duplicator', path='/folders/{id}/duplicator')
async def get_folders(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.
    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    ---
    summary: A specific folder.
    tags:
        - heaserver-folders-get-all-folders
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get_all(request, MONGODB_FOLDER_COLLECTION)


@routes.post('/folders')
@routes.post('/folders/')
async def post_folder(request: web.Request) -> web.Response:
    """
    Creates a folder.
    :param request: the HTTP request.
    :return: Created.
    ---
    summary: Folder creation
    tags:
        - heaserver-folders-post-folder
    requestBody:
      description: A new folder object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Folder example
              value: {
                "template": {
                  "data": [{
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
                    "name": "name",
                    "value": "joe"
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
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Folder example
              value: {
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": null,
                "display_name": "Joe",
                "invited": [],
                "modified": null,
                "name": "joe",
                "owner": "system|none",
                "shares": [],
                "source": null,
                "type": "heaobject.folder.Folder",
                "version": null
              }
    responses:
      '201':
        $ref: '#/components/responses/201'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.post(request, MONGODB_FOLDER_COLLECTION, Folder)


@routes.put('/folders/{id}')
async def put_folder(request: web.Request) -> web.Response:
    """
    Updates the folder with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder updates
    tags:
        - heaserver-folders-put-folder
    parameters:
        - $ref: '#/components/parameters/id'
    requestBody:
      description: An updated folder object.
      required: true
      content:
        application/vnd.collection+json:
          schema:
            type: object
          examples:
            example:
              summary: Folder example
              value: {
                "template": {
                  "data": [{
                    "name": "id",
                    "value": "666f6f2d6261722d71757578",
                  },
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
                    "value": "Bob"
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
                    "value": "bob"
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
                  }]
                }
              }
        application/json:
          schema:
            type: object
          examples:
            example:
              summary: Folder example
              value: {
                "id": "666f6f2d6261722d71757578",
                "created": null,
                "derived_by": null,
                "derived_from": [],
                "description": null,
                "display_name": "Bob",
                "invited": [],
                "modified": null,
                "name": "bob",
                "owner": "system|none",
                "shares": [],
                "source": null,
                "type": "heaobject.folder.Folder",
                "version": null
              }
    responses:
      '204':
        $ref: '#/components/responses/204'
      '400':
        $ref: '#/components/responses/400'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.put(request, MONGODB_FOLDER_COLLECTION, Folder)


@routes.delete('/folders/{id}')
async def delete_folder(request: web.Request) -> web.Response:
    """
    Deletes the folder with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    ---
    summary: Folder deletion
    tags:
        - heaserver-folders-delete-folder
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '204':
        $ref: '#/components/responses/204'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.delete(request, MONGODB_FOLDER_COLLECTION)


@routes.get('/folders/{id}/opener')
@action('heaserver-folders-folder-open-default', rel='hea-opener hea-default application/x.folder', path='/folders/{id}/items/')
async def get_folder_opener(request: web.Request) -> web.Response:
    """
    Opens the requested folder.
    :param request: the HTTP request. Required.
    :return: the opened folder, or Not Found if the requested item does not exist.
    ---
    summary: Folder opener choices
    tags:
        - heaserver-folders-get-folder-open-choices
    parameters:
      - $ref: '#/components/parameters/id'
    responses:
      '300':
        $ref: '#/components/responses/300'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.opener(request, MONGODB_FOLDER_COLLECTION)


def main():
    config = init_cmd_line(description='Repository of folders', default_port=8086)
    start(db=mongo.MongoManager, wstl_builder_factory=builder_factory(__package__), config=config)


async def _get_folder(request: web.Request) -> web.Response:
    """
    Gets the folder with the specified id.
    :param request: the HTTP request.
    :return: the requested folder or Not Found.
    """
    _logger.debug('Requested folder %s', request.match_info["id"])
    if request.match_info['id'] == 'root':
        return ROOT_FOLDER
    else:
        return await mongoservicelib.get(request, MONGODB_FOLDER_COLLECTION)


async def _get_item_response(request) -> web.Response:
    """
    Gets the item with the specified id and in the specified folder.
    :param request: the HTTP request.
    :return: a response containing the returned item or an empty body.
    """
    folder = request.match_info['folder_id']
    _logger.debug('Requested an item from the "%s" folder', folder)
    item = await request.app[appproperty.HEA_DB].get(request, MONGODB_ITEMS_COLLECTION,
                                                     var_parts=['folder_id', 'id'], sub=request.headers.get(SUB))
    _logger.debug('got from mongo: %s', item)
    return await response.get(request, item)
