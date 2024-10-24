from report.report import add_json_to_report


class Response:
    """
    Class for wrapping up response object
    """

    def __init__(self, resp):
        """
        Initializing default response properties
        :param resp: response object
        """
        # Setting up response equal to json
        _log.info(f"Response is {resp}")

        if resp.headers.get("content-type"):
            is_json = "application/json" in resp.headers["content-type"]

        if is_json:
            self.response = resp.json()
            _log.info(f"Response data is {resp.json()}")
            add_json_to_report("Response", resp.json())
        else:
            self.response = None
        # Setting up code equal to status code of response
        self.code = resp.status_code
        # Setting up header if returned in response
        self.headers = resp.headers._store

        if self.response is None:
            _log.error(
                f"Returned response is None due to an error - Response from server {resp}"
            )
            raise TypeError(
                f"Returned response is None due to an error - Response from server {resp}"
            )
