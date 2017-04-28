# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared utilities used by both downloads and uploads.

This utilities are explicitly catered to ``requests``-like transports.
"""


import functools

from google.resumable_media import _helpers


class RequestsMixin(object):
    """Mix-in class implementing ``requests``-specific behavior.

    These are methods that are more general purpose, with implementations
    specific to the types defined in ``requests``.
    """

    @staticmethod
    def _get_status_code(response):
        """Access the status code from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            int: The status code.
        """
        return response.status_code

    @staticmethod
    def _get_headers(response):
        """Access the headers from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            ~requests.structures.CaseInsensitiveDict: The header mapping (keys
            are case-insensitive).
        """
        return response.headers

    @staticmethod
    def _get_body(response):
        """Access the response body from an HTTP response.

        Args:
            response (~requests.Response): The HTTP response object.

        Returns:
            bytes: The body of the ``response``.
        """
        return response.content


def http_request(transport, method, url, data=None, headers=None):
    """Make an HTTP request.

    Args:
        transport (~requests.Session): A ``requests`` object which can make
            authenticated requests via a ``request()`` method. This method
            must accept an HTTP method, an upload URL, a ``data`` keyword
            argument and a ``headers`` keyword argument.
        method (str): The HTTP method for the request.
        url (str): The URL for the request.
        data (Optional[bytes]): The body of the request.
        headers (Mapping[str, str]): The headers for the request (``transport``
            may also add additional headers).

    Returns:
        ~requests.Response: The return value of ``transport.request()``.
    """
    func = functools.partial(
        transport.request, method, url, data=data, headers=headers)
    return _helpers.wait_and_retry(func, RequestsMixin._get_status_code)
