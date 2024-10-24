from time import sleep

import allure
import requests
from requests.status_codes import codes as status_code
from report.report import add_json_to_report


class Request:
    """
    Class for wrapping up request object
    """

    def __init__(self, url, method="get", headers=None, data=None, params=None):
        """
        Initializing default request parameters
        :param url: url for request
        :param method: method for request
        :param headers: request headers
        :param data: request data
        :param params: dict of parameters to request
        """
        self.url = url
        self.params = {}
        # Setup headers
        if headers:
            self.headers = headers
        else:
            self.headers = {
                "Content-type": "application/json",
                "Accept": "application/json",
            }

        self.method = method
        if params is not None:
            self.params.update(params)

        if data:
            self.data = data

    @allure.step("Submit request")
    def submit_request(self, retries=3):
        """
        Method for defining request method and submitting request
        :return: response
        """
        _log.info(
            f"Request method is {self.method}, endpoint is {self.url}, request headers are {self.headers}, "
            f"request params are {self.params}"
        )
        add_json_to_report(
            "Request meta",
            {
                "method": self.method,
                "endpoint": self.url,
                "headers": self.headers,
                "params": self.params,
            },
        )
        try:
            if self.method.lower() == "get":
                resp = requests.get(
                    url=self.url,
                    headers=self.headers,
                    params=self.params,
                    timeout=(25, 30),
                )
            elif self.method.lower() == "post":
                _log.info(f"Request data is {self.data}")
                add_json_to_report("Request data", self.data)
                resp = requests.post(
                    url=self.url,
                    data=self.data,
                    headers=self.headers,
                    params=self.params,
                    timeout=(25, 30),
                )
            elif self.method.lower() == "put":
                _log.info(f"Request data is {self.data}")
                resp = requests.put(
                    url=self.url,
                    data=self.data,
                    headers=self.headers,
                    params=self.params,
                    timeout=(25, 30),
                )
            elif self.method.lower() == "delete":
                resp = requests.delete(
                    url=self.url,
                    headers=self.headers,
                    params=self.params,
                    timeout=(25, 30),
                )
            else:
                _log.error(f"No method specified {self.method}")
                raise AttributeError(self.method)
        except TimeoutError as error:
            sleep(3)
            if retries < 1:
                raise RecursionError(
                    f"Submitting request produced timeout error, please check logs. Maximum "
                    f"retries {retries} reached"
                )
            else:
                _log.warning(f"Timeout error {error}")
                return self.submit_request(retries=retries - 1)

        # If status code in response is 500* retrying to submit same request
        if (
            resp.status_code in (status_code.server_error, status_code.unavailable)
            and not self.allow_error
        ):
            sleep(3)
            if retries < 1:
                raise RecursionError(
                    f"Submitting request produced an error, please check request and response in "
                    f"logs. Maximum retries {retries} reached"
                )
            else:
                _log.warning(
                    f"Server error {resp.status_code} in response {resp}, retrying (retries remaining: {retries})"
                )
                return self.submit_request(retries=retries - 1)
        return resp
