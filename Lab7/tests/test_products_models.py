import unittest
from app import create_app, db
from app.products.models import Product, Category


class ProductCategoryModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_product_and_category_relationship(self):
        with self.app.app_context():
            laptops = Category(name="Laptops")
            db.session.add(laptops)
            p1 = Product(name="Pc", price=700.0)
            p2 = Product(name="Gaming Laptop", price=1500.0, active=False, category=laptops)
            db.session.add_all([p1, p2])
            db.session.commit()

            self.assertTrue(p1.active)
            self.assertIsNotNone(p1.created_at)
            self.assertIsNone(p1.category)

            self.assertFalse(p2.active)
            self.assertEqual(p2.category.name, "Laptops")
            self.assertEqual(len(laptops.products), 1)
            self.assertEqual(laptops.products[0].name, "Gaming Laptop")


if __name__ == "__main__":
    unittest.main()
