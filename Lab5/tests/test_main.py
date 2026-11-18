import os
import tempfile
import unittest
from app import app


class MainViewsTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.log_fd, self.log_path = tempfile.mkstemp(suffix=".log")
        app.config["CONTACTS_LOG_PATH"] = self.log_path
        self.client = app.test_client()

    def tearDown(self):
        os.close(self.log_fd)
        if os.path.exists(self.log_path):
            os.remove(self.log_path)

    def test_index(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_homepage(self):
        response = self.client.get("/homepage")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Home page", response.data)

    def test_contact_form_get(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Send Message", response.data)

    def test_contact_form_valid_post(self):
        response = self.client.post(
            "/contact",
            data={
                "name": "Maksym",
                "email": "maksym@example.com",
                "phone": "+380680712475",
                "subject": "general",
                "message": "Hello from unit test!",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Maksym", response.data)
        with open(self.log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
        self.assertIn("maksym@example.com", log_content)

    def test_contact_form_invalid_post(self):
        response = self.client.post(
            "/contact",
            data={
                "name": "Ab",  # min=4 violated
                "email": "not-an-email",
                "phone": "12345",
                "subject": "general",
                "message": "",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Помилка валідації".encode("utf-8"), response.data)


if __name__ == "__main__":
    unittest.main()
