from flask import jsonify, make_response

from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS, ACTOR_FIELDS
from controllers.parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        act = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(act)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
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

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()

    if 'name' not in data or 'genre' not in data or 'year' not in data:
        err = 'All required fields must be specified'
        return make_response(jsonify(error=err), 400)

        # Check if any inputted fields do not exist
    invalid_fields = set(data.keys()) - set(MOVIE_FIELDS)
    if invalid_fields:
        err = 'Invalid field(s): ' + ', '.join(invalid_fields)
        return make_response(jsonify(error=err), 400)

    try:
        # Convert year to integer
        data['year'] = int(data['year'])

        # Create new movie
        new_record = Movie.create(**data)

        # Extract fields of interest
        new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}

        return make_response(jsonify(new_movie), 200)
    except ValueError:
        err = 'Year must be an integer'
        return make_response(jsonify(error=err), 400)
    except:
        err = 'Invalid data'
        return make_response(jsonify(error=err), 400)


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()

    if 'id' in data.keys():

        # Check if any inputted fields do not exist
        invalid_fields = set(data.keys()) - set(MOVIE_FIELDS)
        if invalid_fields:
            err = 'Invalid field(s): ' + ', '.join(invalid_fields)
            return make_response(jsonify(error=err), 400)

        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        try:
            upd_record = Movie.update(row_id, **data)
            upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
        return make_response(jsonify(upd_movie), 200)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        upd_record = Movie.delete(row_id)
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


def movie_add_relation(movie=None):
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    ### YOUR CODE HERE ###

    if 'id' and 'relation_id' in data.keys():
        try:
            movie_id = int(data['id'])
            actor_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            actor = Actor.query.filter_by(id=actor_id).first()
            movie = Movie.add_relation(movie_id, actor)
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def movie_clear_relations():
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
            movie = Movie.clear_relations(row_id)
            rel_movie = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)