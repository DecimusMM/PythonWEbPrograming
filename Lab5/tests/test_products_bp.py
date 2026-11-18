import io
import os
import tempfile
import unittest
from app import app


class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".json")
        app.config["PRODUCTS_DB_PATH"] = self.db_path
        self.client = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_product_list(self):
        """GET /product відображає список товарів."""
        response = self.client.get("/product")
        self.assertEqual(response.status_code, 200)
        for name in (b"Laptop", b"Phone", b"PC"):
            self.assertIn(name, response.data)

    def test_product_detail(self):
        """GET /product/<id> відображає повну інформацію про товар."""
        response = self.client.get("/product/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200.00", response.data)

    def test_product_not_found(self):
        """Неіснуючий id повертає 404."""
        response = self.client.get("/product/999")
        self.assertEqual(response.status_code, 404)

    def test_product_create(self):
        """POST /product/add створює новий товар у TinyDB."""
        response = self.client.post(
            "/product/add",
            data={
                "name": "Monitor 4K",
                "content": "27-inch IPS 4K UHD Monitor",
                "price": "450.50",
                "category": "Electronics",
                "quantity": "8",
                "image": (io.BytesIO(b"\x89PNG\r\n\x1a\nfakedata"), "monitor.png"),
            },
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Monitor 4K", response.data)
        self.assertIn(b"450.50", response.data)

    def test_product_edit(self):
        """POST /product/<id>/edit оновлює дані товару без зміни id та created_at."""
        self.client.get("/product")  # ініціалізація початкових товарів
        response = self.client.post(
            "/product/1/edit",
            data={
                "name": "Laptop Pro",
                "content": "Оновлений опис ноутбука",
                "price": "1499.99",
                "category": "Computers",
                "quantity": "10",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop Pro", response.data)
        self.assertIn(b"1499.99", response.data)

    def test_product_delete(self):
        """POST /product/<id>/delete видаляє товар із TinyDB."""
        self.client.get("/product")
        response = self.client.post("/product/2/delete", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        detail_resp = self.client.get("/product/2")
        self.assertEqual(detail_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
