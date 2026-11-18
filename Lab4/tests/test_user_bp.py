import unittest
from app import app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_greetings_page(self):
        """Тест маршруту /users/hi/<name>."""
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_greetings_without_age(self):
        """Тест маршруту /users/hi/<name> без віку."""
        response = self.client.get("/users/hi/John")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Not provided", response.data)

    def test_admin_page(self):
        """Тест маршруту /users/admin, який перенаправляє."""
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_admin_redirect_status(self):
        """/users/admin має повертати 302."""
        response = self.client.get("/users/admin")
        self.assertEqual(response.status_code, 302)

    def test_login_get(self):
        """GET /users/login повертає форму входу."""
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_login_success_and_profile(self):
        """Успішний вхід зберігає користувача в сесію та перенаправляє на профіль."""
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "password123"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"user1!", response.data)

    def test_login_invalid_credentials(self):
        """Невдалий вхід повертає на login із flash-повідомленням про помилку."""
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "wrong"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong data! Try again!", response.data)

    def test_profile_requires_login(self):
        """Неавторизований доступ до /users/profile перенаправляє на /users/login."""
        response = self.client.get("/users/profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_logout(self):
        """Вихід очищує сесію та перенаправляє на /users/login."""
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"
        response = self.client.post("/users/logout", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_cookies_add_and_delete(self):
        """Додавання та видалення кукі на сторінці профілю."""
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"

        response = self.client.post(
            "/users/profile",
            data={
                "action": "add_cookie",
                "cookie_key": "test_key",
                "cookie_value": "test_val",
                "cookie_max_age": "3600",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"test_key", response.data)
        self.assertIn(b"test_val", response.data)

        response = self.client.post(
            "/users/profile",
            data={"action": "delete_cookie", "delete_key": "test_key"},
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_theme_switching(self):
        """Зміна кольорової схеми профілю."""
        with self.client.session_transaction() as sess:
            sess["username"] = "user1"

        response = self.client.get("/users/theme/dark", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"theme-dark", response.data)


if __name__ == "__main__":
    unittest.main()
