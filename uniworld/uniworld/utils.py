from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.cache import cache

def invalidate_cache(path=''):
    ''' this function uses Django's caching function get_cache_key(). Since 1.7,
        Django has used more variables from the request object (scheme, host,
        path, and query string) in order to create the MD5 hashed part of the
        cache_key. Additionally, Django will use your server's timezone and
        language as properties as well. If internationalization is important to
        your application, you will most likely need to adapt this function to
        handle that appropriately.
    '''
    request = HttpRequest()
    request.META = {'SERVER_NAME': '118.190.77.81', 'SERVER_PORT': 8000}
    request.LANGUAGE_CODE = 'en-us'
    request.path = path
    try:
        cache_key = get_cache_key(request)
        if cache_key:
            if cache.has_key(cache_key):
                cache.delete(cache_key)
                return (True)
            else:
                return (False)
        else:
            raise ValueError('failed to create cache_key')
    except (ValueError, Exception) as e:
        print(e)
        return False