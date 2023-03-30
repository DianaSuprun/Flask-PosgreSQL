from datetime import datetime

from flask import jsonify, make_response
from models.actor import Actor
from models.movie import Movie
from settings.constants import *
from controllers.parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'name' not in data or 'gender' not in data or 'date_of_birth' not in data:
        err = 'Missing required fields'
        return make_response(jsonify(error=err), 400)

        # Check if any inputted fields do not exist
    invalid_fields = set(data.keys()) - set(ACTOR_FIELDS)
    if invalid_fields:
        err = 'Invalid field(s): ' + ', '.join(invalid_fields)
        return make_response(jsonify(error=err), 400)

    if data['date_of_birth'].find('/') != -1:
        err = 'should be data'
        return make_response(jsonify(error=err), 400)

    new_record = Actor.create(**data)
    new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(new_actor), 200)


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()

    invalid_fields = set(data.keys()) - set(ACTOR_FIELDS)
    if invalid_fields:
        err = 'Invalid field(s): ' + ', '.join(invalid_fields)
        return make_response(jsonify(error=err), 400)

    if 'id' not in data:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    try:
        row_id = int(data['id'])
    except ValueError:
        err = 'Id must be integer'
        return make_response(jsonify(error=err), 400)

    if not Actor.query.filter_by(id=row_id).first():
        err = 'Record with such id does not exist'
        return make_response(jsonify(error=err), 400)

    if 'date_of_birth' in data:
        try:
            datetime.strptime(data['date_of_birth'], DATE_FORMAT)
        except ValueError:
            err = f"Invalid date format. Should be in format '{DATE_FORMAT}'"
            return make_response(jsonify(error=err), 400)
    upd_record = Actor.update(row_id, **data)
    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
    return make_response(jsonify(upd_actor), 200)


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        upd_record = Actor.delete(row_id)
        if upd_record == 1:
                msg = 'Record successfully deleted'
                print(msg)
                return make_response(jsonify(message=msg), 200)
        elif upd_record == 0:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)



def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    if 'id' and 'relation_id' in data.keys():
        try:
            actor_id = int(data['id'])
            movie_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            movie = Movie.query.filter_by(id=movie_id).first()
            actor = Actor.add_relation(actor_id, movie)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            actor = Actor.clear_relations(row_id)
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###
