from flask import request, session 
from sqlalchemy import text
from flask_restful import Resource
from marshmallow import EXCLUDE
from project.blueprints.user.models import UserModel
from project.blueprints.user.schemas import UserSchema
from datetime import datetime, timedelta
import json
from project.extensions import cache

user_schema = UserSchema(unknown=EXCLUDE)
multiple_user_schema = UserSchema(many=True)


class Client_Side_Cache:
    """"
    Client side implementation is done with built-in flask session while server side caching is done with redis
    All session data stored on client-side as Cookies.
    What was Cached: 
      - the endpoint visited by the user
      - the response from the endpoint
    """
    url = None
    data = None
    default_time = None
    
    def __init__(self, url=None, data=None, default_time=30):
        self.url = url
        self.data = data
        self.default_time = timedelta(seconds=default_time)
    
    def add(self, url, data=None, timeout=None):
        if timeout:
            expire = datetime.now() +  timedelta(seconds=timeout)
            session[url] = json.dumps(expire, default=str), data
        else:
            expire = self.default_time
            session[url] = json.dumps(expire, default=str), data
        
    def get(self, url):
        if session.get(url):
        # if session[url]:
            expire_time = session[url][0]
            data = session[url][1]
            expire_str = json.loads(expire_time)
            date_time = datetime.strptime(expire_str, '%Y-%m-%d %H:%M:%S.%f')
            if datetime.now() <  date_time:
                return data
            else:
                session.pop(url, None)
        return None

client_side_caching = Client_Side_Cache(30)

class UsersList(Resource):
    @classmethod
    # @cache.memoize(timeout=60)
    def get(cls,):
        data = None
        try:
            url = f'{request.url}'
            redis_data = cache.get(url) # get server side cache
            data = redis_data
            # if not data:
            if not redis_data:
                client_data = client_side_caching.get(url) # get client side cache  
                sort_by = UserModel.sort_by(request.args.get('sort', 'created_on'),
                                request.args.get('direction', 'desc'))
                order_values = 'users.{0} {1}'.format(sort_by[0], sort_by[1])
                
                # implement caching
                page = int(request.args.get('page', 1))

                users_per_page = int(request.args.get('users_per_page', 20))
                
                page_object = UserModel.query.filter(UserModel.search(request.args.get('q', ''))) \
                    .order_by(text(order_values)) \
                    .paginate(page, users_per_page,  False)

                data = multiple_user_schema.dump(page_object.items)
                # with open('./tit.txt', 'a') as f:
                #     f.write(f"I'm still adding...")
                client_side_caching.add(url, data, timeout=60) # client side cache
                cache.set(url, data, timeout=60) # Server Side Cache
        
        except:
            ...

        return {
            "responseCode": 200,
            "responseDescription": "Success",
            "responseMessage": data
        }


