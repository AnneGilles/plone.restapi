HTTP Status Codes
=================

This is the list of status codes that are used in plone.restapi. Here is a `full list of all HTTP status codes`_.

2xx Success
-----------

This class of status codes indicates the action requested by the client was received, understood, accepted and processed successfully.

.. _`200 OK`:

200 OK
******

    Standard response for successful HTTP requests. The actual response will depend on the request method used. In a GET request, the response will contain an entity corresponding to the requested resource. In a POST request, the response will contain an entity describing or containing the result of the action.

.. _`201 Created`:

201 Created
***********

    The request has been fulfilled and resulted in a new resource being created.

.. _`204 No Content`:

204 No Content
**************

    The server successfully processed the request, but is not returning any content. Usually used as a response to a successful delete request.


4xx Client Error
----------------

The 4xx class of status code is intended for cases in which the client seems to have errored.

.. _`400 Bad Request`:

400 Bad Request
***************

    The server cannot or will not process the request due to something that is perceived to be a client error (e.g., malformed request syntax, invalid request message framing, or deceptive request routing)

.. _`401 Unauthorized`:

401 Unautorized
***************

    Similar to 403 Forbidden, but specifically for use when authentication is required and has failed or has not yet been provided. The response must include a WWW-Authenticate header field containing a challenge applicable to the requested resource.

.. _`403 Forbidden`:

403 Forbidden
*************

    The request was a valid request, but the server is refusing to respond to it. Unlike a 401 Unauthorized response, authenticating will make no difference.

.. _`404 Not Found`:

404 Not Found
*************

    The requested resource could not be found but may be available again in the future. Subsequent requests by the client are permissible.

.. _`409 Conflict`:

409 Conflict
************

    Indicates that the request could not be processed because of conflict in the request, such as an edit conflict in the case of multiple updates.


5xx Server Error
----------------

.. _`500 Internal Server Error`:

500 Internal Server Error
*************************

    The server failed to fulfill an apparently valid request.

.. _`full list of all HTTP status codes`: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
