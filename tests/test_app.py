import unittest
import os

os.environ["TESTING"] = "true"

from app import app


class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert (
            'computer science major'
            in html
        )

    def test_navbar_default_style(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'id="home_route"' in html

        # Test the education page
        response = self.client.get("/education")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'id="education_route"' in html

        # Test the map page
        response = self.client.get("/map")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert 'id="map_route"' in html

    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json

    def test_api_timeline_post_create(self):
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "content": "This is a test post.",
        }
        response = self.client.post("/api/timeline_post", data=data)
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "name" in json
        assert "email" in json
        assert "content" in json

        assert json["name"] == data["name"]
        assert json["email"] == data["email"]
        assert json["content"] == data["content"]

        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json

        assert json["timeline_posts"][0]["name"] == data["name"]
        assert json["timeline_posts"][0]["email"] == data["email"]
        assert json["timeline_posts"][0]["content"] == data["content"]

    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        assert (
            'Timeline'
            in response.get_data(as_text=True)
        )

    def test_malformed_timeline_post(self):
        response = self.client.post(
            "/api/timeline_post",
            data={"email": "john@example.com", "content": "Hello world, I'm John!"},
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid name" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "email": "john@example.com",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid content" in html

        response = self.client.post(
            "/api/timeline_post",
            data={
                "name": "John Doe",
                "content": "Hello world, I'm John!",
            },
        )
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid email" in html
