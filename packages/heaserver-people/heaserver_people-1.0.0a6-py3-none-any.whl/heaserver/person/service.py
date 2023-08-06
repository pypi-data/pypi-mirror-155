"""
The HEA Person Microservice provides ...
"""

from heaserver.service import response
from heaserver.service.runner import init_cmd_line, routes, start, web
from heaserver.service.db import mongo, mongoservicelib
from heaserver.service.wstl import builder_factory, action
from heaobject.person import Person

MONGODB_PERSON_COLLECTION = 'people'

@routes.get('/ping')
async def ping(request: web.Request) -> web.Response:
    """
    For testing whether the service is up.

    :param request: the HTTP request.
    :return: Always returns status code 200.
    """
    return response.status_ok(None)


@routes.get('/people/{id}')
@action('heaserver-people-person-get-properties', rel='properties')
@action('heaserver-people-person-open', rel='opener', path='/people/{id}/opener')
@action('heaserver-people-person-duplicate', rel='duplicator', path='/people/{id}/duplicator')
async def get_person(request: web.Request) -> web.Response:
    """
    Gets the person with the specified id.
    :param request: the HTTP request.
    :return: the requested person or Not Found.
    ---
    summary: A specific person.
    tags:
        - persons
    parameters:
        - name: id
          in: path
          required: true
          description: The id of the person to retrieve.
          schema:
            type: string
    responses:
      '200':
        description: Expected response to a valid request.
        content:
            application/json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.collection+json:
                schema:
                    type: array
                    items:
                        type: object
            application/vnd.wstl+json:
                schema:
                    type: array
                    items:
                        type: object
      '404':
        $ref: '#/components/responses/404'
    """
    return await mongoservicelib.get(request, MONGODB_PERSON_COLLECTION)


@routes.get('/people/byname/{name}')
async def get_person_by_name(request: web.Request) -> web.Response:
    """
    Gets the person with the specified id.
    :param request: the HTTP request.
    :return: the requested person or Not Found.
    """
    return await mongoservicelib.get_by_name(request, MONGODB_PERSON_COLLECTION)


@routes.get('/people')
@routes.get('/people/')
@action('heaserver-people-person-get-properties', rel='properties')
@action('heaserver-people-person-open', rel='opener', path='/people/{id}/opener')
@action('heaserver-people-person-duplicate', rel='duplicator', path='/people/{id}/duplicator')
async def get_all_persons(request: web.Request) -> web.Response:
    """
    Gets all persons.
    :param request: the HTTP request.
    :return: all persons.
    """
    return await mongoservicelib.get_all(request, MONGODB_PERSON_COLLECTION)


@routes.get('/people/{id}/duplicator')
@action(name='heaserver-people-person-duplicate-form')
async def get_person_duplicate_form(request: web.Request) -> web.Response:
    """
    Gets a form template for duplicating the requested person.

    :param request: the HTTP request. Required.
    :return: the requested form, or Not Found if the requested person was not found.
    """
    return await mongoservicelib.get(request, MONGODB_PERSON_COLLECTION)


@routes.post('/people/duplicator')
async def post_person_duplicator(request: web.Request) -> web.Response:
    """
    Posts the provided person for duplication.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_PERSON_COLLECTION, Person)


@routes.post('/people')
@routes.post('/people/')
async def post_person(request: web.Request) -> web.Response:
    """
    Posts the provided person.
    :param request: the HTTP request.
    :return: a Response object with a status of Created and the object's URI in the
    """
    return await mongoservicelib.post(request, MONGODB_PERSON_COLLECTION, Person)


@routes.put('/people/{id}')
async def put_person(request: web.Request) -> web.Response:
    """
    Updates the person with the specified id.
    :param request: the HTTP request.
    :return: a Response object with a status of No Content or Not Found.
    """
    return await mongoservicelib.put(request, MONGODB_PERSON_COLLECTION, Person)


@routes.delete('/people/{id}')
async def delete_person(request: web.Request) -> web.Response:
    """
    Deletes the person with the specified id.
    :param request: the HTTP request.
    :return: No Content or Not Found.
    """
    return await mongoservicelib.delete(request, MONGODB_PERSON_COLLECTION)


def main() -> None:
    config = init_cmd_line(description='A microservice designed to provide CRUD operations for the Person HEA object type',
                           default_port=8080)
    start(db=mongo.MongoManager, wstl_builder_factory=builder_factory(__package__), config=config)
