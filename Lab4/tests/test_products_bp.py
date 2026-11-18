import unittest
from app import app


class ProductsBlueprintTestCase(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_product_list(self):
        """Список товарів повертає 200 і містить усі товари."""
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        for name in (b"Laptop", b"Phone", b"PC"):
            self.assertIn(name, response.data)

    def test_product_detail(self):
        """Деталі товару за id."""
        response = self.client.get("/products/1")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Laptop", response.data)
        self.assertIn(b"1200", response.data)

    def test_product_detail_phone(self):
        response = self.client.get("/products/2")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Phone", response.data)
        self.assertIn(b"800", response.data)

    def test_product_not_found(self):
        """Неіснуючий id повертає 404."""
        response = self.client.get("/products/999")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
