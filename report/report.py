import os
from json import dumps

from allure import attach, attachment_type


def add_json_to_report(name, body):
    """
    Attach json to allure step for logging purposes
    :param name: the name of the attachment
    :param body: json to be attached to report
    """
    if body:
        attach(
            body=dumps(body, indent=2),
            name=name,
            attachment_type=attachment_type.JSON,
        )
