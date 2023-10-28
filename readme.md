
URL Shortener Backend Developer Exercise
===================================

This is a Django project that implement a URL Shortener with hit count for each shorten link.

Short URL -
-----------

The Short Url is saved as 6 characters of Base62, using *`_generate_rand_str`* method.
It stored in the "short_path" `CharField` field in the URLMapper Model.
"short_path" field enforce `unique=True`, hence it maintain unique property.
"short_path" currently limited to 6 characters, that ensure 62^6 unique identifiers.
Notice: 62^6 = 5.68 x 10 ^ 10 unique identifiers.

When it will not be enough, two main options to solve it are:
1. reused "short_path" identifiers that wasn't been in use for a long period of time.
2. raise the "short_path" identifier length by 1 will ensure us additional large range of unused unique identifiers.


Hit Count logic -
------------------
Update:
Is made by calling: *'UrlMapper.objects.filter(short_path=kwargs['pk']).update(hits=F('hits')+1)'*, from the RedirectViewUrl.get_redirect_url.

Exists in the URLMapper model as PositiveBigIntegerField field named "hits".
Increment by 1, by calling URLMapper.increase_hits from the RedirectViewUrl view.
Each hit will create or update the browser cache, and will cause subsequent requests to fullfill by the browser cache.
Request that will not reach to our view, will not increase the hit counter.


Note: Each Session expire after two weeks (default value of SESSION_COOKIE_AGE).

unittest -
----------
There are 3 tests for the CreateViewShortener:
1. test_createapiview_get_200 - Test the 200 response status code, when calling a GET on the create_url_mapper.
2. test_createapiview_create_valid_url - Test the creation of a URLMapper and the status code, using valid data.
3. test_createapiview_create_invalid_url - Test the create_url_mapper, using invalid URL string.

There are 2 tests for the RedirectViewUrlTest:
1. test_redirect_url - Test the correct redirect process, using a valid short path.
2. test_redirect_non_existing_url - Test the process of an invalid short path as input.


Additional modifications -
--------------------------
1. Change RedirectViewUrl.permanent attribute to True, so the browser will cache the address.
   Only the initial request will reach the server.
   Any subsequent request will be handled by the browser. 


Future Improvements -
---------------------

1. To Add User management option. A User should manage its own items and modify them.
2. Maybe to Add a feature that could collect data about the hits (location, etc) using kafka.
