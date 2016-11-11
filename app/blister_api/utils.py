from flask import url_for, current_app,g
from functools import wraps
from flask import request
from flask_restful import abort
from app.blister_api.models import BucketList


def paginate(f):
    @wraps(f)
    def func_wrapper(*args, **kwargs):
        query = f(*args, **kwargs)
        page = request.args.get('page', 1, type=int)
        limit = min(request.args.get('limit',
                                     current_app.config['DEFAULT_PER_PAGE'],
                                     type=int),
                    current_app.config['MAX_PER_PAGE'])
        q = request.args.get('q')
        page_bucketlist = BucketList.query.filter(BucketList.user_id == g.user.id)
        page_bucketlist = page_bucketlist.paginate(page=page, per_page=limit)
        bucketlists = page_bucketlist.items
        if not bucketlists:
            abort(404)
        pagination = {
            'page': page_bucketlist.page,
            'number_of_pages': page_bucketlist.pages,
            'total': page_bucketlist.total,
        }
        if page_bucketlist.has_next:
            pagination['next'] = url_for(endpoint=request.endpoint,
                                         limit=limit,
                                         page=page_bucketlist.next_num,
                                         _method='GET', q=q, _external=True,
                                         **kwargs)
        if page_bucketlist.has_prev:
            pagination['previous'] = url_for(endpoint=request.endpoint,
                                             limit=limit, page=page_bucketlist
                                             .prev_num, q=q, _method='GET',
                                             _external=True, **kwargs)
        return {'bucketlists': bucketlists, 'pagination': pagination}, 200
    return func_wrapper
