import allure
from json import dumps
from client.client import RestClient


@allure.feature("Pets feautre")
class TestGetPet:
    """
    Test class for the pet functionality
    """

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Buyer can check available pets named “pupo” with category name “pajaro” and place an order for a pet"
    )
    def test_place_an_order(self):
        """
        Test for getting the pet and placing an order
        """
        client = RestClient()
        response_find = client.access_endpoint(
            method="GET", endpoint="pet/findByStatus", params={"status": "available"}
        )
        pajaro_pets = []
        pet_id = 0
        for resp in response_find.response:
            if "category" in resp:
                if resp["category"]["name"] == "pajaro":
                    pajaro_pets.append(resp)

        for pet in pajaro_pets:
            if pet["name"] == "pupo":
                pet_id = pet["id"]
                break

        request_data = dumps(
            {"petId": pet_id, "quantity": 1, "status": "placed", "complete": True}
        )

        response_order = client.access_endpoint(
            method="POST", endpoint="store/order", request_body=request_data
        )

        order = response_order.response
        assert (
            response_order.code == 200
        ), f"Expected response code 200 but got {response_order.code}"
        assert order["petId"] == pet_id, f'Expected {pet_id} but got {order["petId"]}'
        assert (
            order["status"] == "placed"
        ), f'Expected placed status but got {order["status"]}'
        assert order["complete"] == True, f'Expected True but got {order["complete"]}'
