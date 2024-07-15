import pytest


@pytest.fixture(scope="module")
def member_id(test_app):
    payload = {
        "name": "HARIMU",
        "name_orig": "박혜림",
        "image_url": "https://scontent.cdninstagram.com/v/t51.2885-19/296840194_783755619314668_2379122151401318130_n.jpg?_nc_ht=scontent.cdninstagram.com&_nc_cat=104&_nc_ohc=HEWLyaEPQmQQ7kNvgFxzwCS&edm=APs17CUBAAAA&ccb=7-5&oh=00_AYCgi1By22gsIoGcFupngDDXu9UMLXIa8HZweeybXLqWGA&oe=664C4CA5&_nc_sid=10d13b",
        "nationality": "KR",
        "based_in": "Seoul",
        "instagram": "___harimu___",
    }
    response = test_app.post("/dancers/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create member. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


@pytest.fixture(scope="module")
def crew_id(test_app, core_studio_id, core_dancer_id, member_id):
    payload = {
        "name": "1MILLION",
        "bio": "inspire millions",
        "based_in": "Seoul",
        "founded_in": 2022,
        "styles": ["Choreography"],
        "instagram": "1million_swf",
        "home_studio_id": core_studio_id,
        "leader_ids": [core_dancer_id],
        "member_ids": [member_id],
    }
    response = test_app.post("/crews/", json=payload)
    assert (
        response.status_code == 200
    ), f"Failed to create sample crew. Status code: {response.status_code}. Response body: {response.text}"
    data = response.json()
    return data["id"]


class TestCrew:
    def test_get_all_crews(self, test_app, crew_id):
        response = test_app.get("/crews/")
        assert response.status_code == 200
        crews = response.json()
        assert any(
            crew["id"] == crew_id for crew in crews
        ), "Crew not found in the list of all crews."

    def test_get_crew(self, test_app, crew_id):
        response = test_app.get(f"/crews/{crew_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == crew_id

    def test_update_crew(self, test_app, crew_id):
        updated_payload = {"name": "1MILLION SWF"}
        response = test_app.put(f"/crews/{crew_id}", json=updated_payload)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "1MILLION SWF", "Crew was not updated successfully."

        # fetch the crew to verify the update took effect
        response = test_app.get(f"/crews/{crew_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "1MILLION SWF", "Crew update did not persist."

    def test_delete_crew(self, test_app, crew_id):
        # delete the crew
        delete_response = test_app.delete(f"/crews/{crew_id}")
        assert delete_response.status_code == 200

        # attempt to fetch the deleted crew
        fetch_response = test_app.get(f"/crews/{crew_id}")
        assert fetch_response.status_code == 404, "Crew was not deleted successfully."
