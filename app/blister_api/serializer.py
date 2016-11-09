from flask_restful import fields as f


bucketlistitem_serializer = {

    'id': f.Integer,
    'title': f.String,
    'done': f.Boolean,
    'description': f.String,
    'date_created': f.DateTime(dt_format='rfc822'),
    'date_modified': f.DateTime(dt_format='rfc822'),
    'bucketlist_id': f.Integer(attribute='bucketlist_id'),
}


bucketlist_serializer = {
    'id': f.Integer,
    'title': f.String,
    'description': f.String,
    'date_created': f.DateTime(dt_format='rfc822'),
    'date_modified': f.DateTime(dt_format='rfc822'),
    'created_by': f.Integer(attribute='user_id'),
    'items': f.List(f.Nested(bucketlistitem_serializer)),
}


bucketlist_collection_serializer = {
    'bucketlists': f.List(f.Nested(bucketlist_serializer)),
}
