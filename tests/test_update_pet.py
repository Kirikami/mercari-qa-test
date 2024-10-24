import allure
from json import dumps
from client.client import RestClient


@allure.feature("Store feauter")
class TestUpdatePet:
    """
    Test class for store functionality
    """

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Store owner can update the pet information of pets named “kurikuri” under category “Pomeranian” to add the tag 'Super Cute'"
    )
    def test_update_tag(self):
        """
        Test for updating tag for the pet
        """
        client = RestClient()
        response_find = client.access_endpoint(
            method="GET", endpoint="pet/findByStatus", params={"status": "available"}
        )
        pets = []
        pet_id = 0
        for resp in response_find.response:
            if "category" in resp:
                if resp["category"]["name"] == "Pomeranian":
                    pets.append(resp)

        for pet in pets:
            if pet["name"] == "kurikuri":
                pet_id = pet["id"]
                break

        request_data = dumps(
            {"petId": pet_id, "tags": [{"id": 2, "name": "Super Cute"}]}
        )

        response_update_tag = client.access_endpoint(
            method="PUT", endpoint="pet", request_body=request_data
        )

        tag_response = response_update_tag.response
        tags = []
        for tag in tag_response["tags"]:
            tags = tag["name"]
        assert (
            response_update_tag.code == 200
        ), f"Expected response code 200 but got {response_update_tag.code}"
        assert (
            tag_response["id"] == pet_id
        ), f'Expected {pet_id} but got {tag_response["id"]}'
        assert "Super Cute" in tags, f"Expected tag to be Super Cute but got {tags}"
