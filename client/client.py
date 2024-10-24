import os

import allure

from client.request import Request
from client.response import Response


class RestClient:
    """
    Class for Rest api client
    """

    def __init__(self):
        self.rest_url = "https://petstore.swagger.io/v2"

    @allure.step("Get response for endpoint")
    def get_request(self, url, params=None):
        url = f"{self.rest_url}/{url}"
        req = Request(url=url, params=params)

        resp = Response(req.submit_request())
        return resp

    @allure.step("Post request for endpoint")
    def post_request(self, url, request_body, params=None):
        url = f"{self.rest_url}/{url}"
        req = Request(url=url, method="post", data=request_body, params=params)
        resp = Response(req.submit_request())
        return resp

    @allure.step("Put request for endpoint")
    def put_request(self, url, request_body, params=None):
        url = f"{self.rest_url}/{url}"
        req = Request(url=url, method="put", data=request_body, params=params)
        resp = Response(req.submit_request())
        return resp

    @allure.step("Access endpoint {endpoint}")
    def access_endpoint(
        self, method="GET", endpoint=None, path=None, request_body=None, params=None
    ):
        url = endpoint
        if path not in ({}, None):
            for v in path.values():
                url += f"/{v}"

        return self.dispatch_request(method, url, request_body, params)

    @allure.step("Dispatch request for method {method}")
    def dispatch_request(self, method, url, request_body, params):
        if method == "GET":
            response = self.get_request(url=url, params=params)
        elif method == "POST":
            response = self.post_request(
                url=url, request_body=request_body, params=params
            )
        elif method == "PUT":
            response = self.put_request(
                url=url, request_body=request_body, params=params
            )
        else:
            _log.warning(f"No method - {method} implemented")
            raise NameError(f"No method - {method} implemented")

        return response
