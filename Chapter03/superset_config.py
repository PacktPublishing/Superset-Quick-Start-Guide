# Superset Configuration file
# add file superset_config.py to PYTHONPATH for usage
import os
import json
from flask_appbuilder.security.manager import AUTH_OAUTH

# Metadata database
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://superset:superset@localhost/superset"
# Securing Session data
SECRET_KEY = 'AdLcixY34P' # random string
# Caching Queries
CACHE_CONFIG = {    
    # Specify the cache type 
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': 'redis://localhost:6379/0',
    # The key prefix for the cache values stored on the server 
    'CACHE_KEY_PREFIX': 'superset_results'
}
# Set this API key to enable Mapbox visualizations 
MAPBOX_API_KEY = os.environ.get('MAPBOX_API_KEY')
# Long running query handling using Celery workers
class CeleryConfig(object): 
    BROKER_URL = 'redis://localhost:6379/0' 
    CELERY_IMPORTS = ('superset.sql_lab', ) 
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    # Rate limit new long queries to 10 per second 
    CELERY_ANNOTATIONS = {'tasks.add': {'rate_limit': '10/s'}} 
         
CELERY_CONFIG = CeleryConfig
         
# Persisting results from running query handling using Celery workers
from werkzeug.contrib.cache import RedisCache 
RESULTS_BACKEND = RedisCache(host='localhost', port=6379, key_prefix='superset_results')

# Google OAUTH Secrets
CSRF_ENABLED = True
AUTH_TYPE = AUTH_OAUTH
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Admin"
auth_credentials = json.load(open(os.environ.get('GOOGLE_OAUTH_CREDENTIALS')))['web']
OAUTH_PROVIDERS = [
        {
            'name': 'google',
            'whitelist': ['shashank@packtpub.com'],
            'icon': 'fa-google',
            'token_key': 'access_token', 
            'remote_app': {
                'base_url': 'https://www.googleapis.com/oauth2/v2/',
                'request_token_params': {
                    'scope': 'email profile'
                },
                'request_token_url': None,
                'access_token_url': auth_credentials['token_uri'],
                'authorize_url': auth_credentials['auth_uri'],
                'consumer_key': auth_credentials['client_id'],
                'consumer_secret': auth_credentials['client_secret']
            }
        }
    ]
