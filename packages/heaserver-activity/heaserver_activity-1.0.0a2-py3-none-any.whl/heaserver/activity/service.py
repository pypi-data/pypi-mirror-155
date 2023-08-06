"""
The HEA Server Activity Microservice provides ...
"""

from heaserver.service import response, appproperty
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaobject.activity import Activity

MONGODB_ACTIVITY_COLLECTION = 'activity'


@routes.get('/activity/{id}')
@action('heaserver-activity-activity-get-properties', rel='properties')
@action('heaserver-activity-activity-open', rel='opener', path='/activity/{id}/opener')
@action('heaserver-activity-activity-duplicate', rel='duplicator', path='/activity/{id}/duplicator')
async def get_activity(request: web.Request) -> web.Response:
    """
    Gets the activity with the specified id.
    :param request: the HTTP request.
    :return: the requested activity or Not Found.
    ---
    summary: A specific activity.
    tags:
        - activity
    parameters:
        - $ref: '#/components/parameters/id'
    responses:
      '200':
        $ref: '#/components/responses/200'
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get(request, MONGODB_ACTIVITY_COLLECTION)


@routes.get('/activity/byname/{name}')
async def get_activity_by_name(request: web.Request) -> web.Response:
    """
    Gets the activity with the specified name.
    :param request: the HTTP request.
    :return: the requested activity or Not Found.
    """
    return await mongoservicelib.get_by_name(request, MONGODB_ACTIVITY_COLLECTION)


@routes.get('/activity')
@routes.get('/activity/')
@action('heaserver-activity-activity-get-properties', rel='properties')
@action('heaserver-activity-activity-open', rel='opener', path='/activity/{id}/opener')
@action('heaserver-activity-activity-duplicate', rel='duplicator', path='/activity/{id}/duplicator')
async def get_all_activity(request: web.Request) -> web.Response:
    """
    Gets all activity.
    :param request: the HTTP request.
    :return: all activity.
    """
    return await mongoservicelib.get_all(request, MONGODB_ACTIVITY_COLLECTION)


@routes.get('/activity/{id}/duplicator')
@action(name='heaserver-activity-activity-duplicate-form')
async def get_activity_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested activity.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested activity was not found.
    """
    return await mongoservicelib.get(request, MONGODB_ACTIVITY_COLLECTION)


@routes.post('/activity/duplicator')
async def post_activity_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided activity for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the Location header.
    """
    return await mongoservicelib.post(request, MONGODB_ACTIVITY_COLLECTION, Activity)


@routes.post('/activity')
@routes.post('/activity/')
async def post_activity(request: web.Request) -> web.Response:
    """
    Posts the provided activity.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_ACTIVITY_COLLECTION, Activity)


@routes.put('/activity/{id}')
async def put_activity(request: web.Request) -> web.Response:
    """
    Updates the activity with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    """
    return await mongoservicelib.put(request, MONGODB_ACTIVITY_COLLECTION, Activity)


@routes.delete('/activity/{id}')
async def delete_activity(request: web.Request) -> web.Response:
    """
    Deletes the activity with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    """
    return await mongoservicelib.delete(request, MONGODB_ACTIVITY_COLLECTION)


def main() -> None:
    config = init_cmd_line(description='A service for tracking activity in hea',
                           default_port=8080)
    start(db=mongo.MongoManager, wstl_builder_factory=builder_factory(__package__), config=config)
