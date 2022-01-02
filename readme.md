
URL Shortener Backend Developer Exercise
===================================

This is a Django project that implement a URL Shortener with hit count for each shorten link.

Short URL -
-----------

The Short Url is saved as 6 characters of Base64.
It stored in the "short_path" `CharField` field in the URLMapper Model.
"short_path" identifier is a Base64 representation of the URLMapper id, hence its unique.
"short_path" currently limited to 6 characters, that ensure 64^6 unique identifiers.
Notice: 64^6 = 6.87 x 10 ^ 10 unique identifiers.

When it will not be enough, two main options to solve it are:
1. reused "short_path" identifiers that wasn't been in use for a long period of time.
2. raise the "short_path" identifier length by 1 will ensure us additional large range of unused unique identifiers.


Hit Count logic -
------------------
Exists in the URLMapper model as PositiveBigIntegerField field named "hits".
Increment by 1, by calling URLMapper.increase_hits from the RedirectViewUrl view.
Each session has limitation on the counter increment for a specific URLMapper, that enforce only one increment in 24 hours.
The implementation is by using the session dictionary with datetime and located in RedirectViewUrl.get_redirect_url.

Note: Each Session expire after two weeks (default value of SESSION_COOKIE_AGE).

unittest -
----------
There are 3 tests for the CreateViewShortener:
1. test_createapiview_get_405 - Test the 405 response status code, when calling a GET on the CreateAPIView.
2. test_createapiview_create_valid_url - Test the creation of a URLMapper and the status code, using valid data.
3. test_createapiview_create_invalid_url - Test the CreateAPIView, using invalid URL string.

There are 2 tests for the RedirectViewUrlTest:
1. test_redirect_url - Test the correct redirect process, using a valid short path.
2. test_redirect_non_existing_url - Test the process of an invalid short path as input.


Additional modifications -
--------------------------
1. Make "increase_hits" Atomic Block (using @transaction.atomic)
2. Change RedirectViewUrl.permanent attribute to True, so the browser will cache the address.
   Only the initial request will reach the server.
   Any subsequent request will be handled by the browser. 
