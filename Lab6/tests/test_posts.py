import unittest
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """US01: Створити новий пост."""
        with self.app.app_context():
            response = self.client.post(
                "/post/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD!",
                    "category": "tech",
                    "is_active": "y",
                },
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)

            stmt = db.select(Post).where(Post.title == "My first post")
            post = db.session.scalar(stmt)
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")

    def test_list_posts(self):
        """US02: Перегляд усіх постів."""
        with self.app.app_context():
            p1 = Post(title="Post One", content="Content 1", category="news", is_active=True)
            p2 = Post(title="Hidden Post", content="Secret", category="other", is_active=False)
            db.session.add_all([p1, p2])
            db.session.commit()

            response = self.client.get("/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post One", response.data)
            self.assertNotIn(b"Hidden Post", response.data)

    def test_view_post_detail(self):
        """US03: Перегляд одного поста."""
        with self.app.app_context():
            post = Post(title="Detailed Post", content="Full text of the article", category="publication")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            response = self.client.get(f"/post/{post_id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detailed Post", response.data)
            self.assertIn(b"Full text of the article", response.data)

    def test_update_post(self):
        """US04: Редагування поста."""
        with self.app.app_context():
            post = Post(title="Old Title", content="Old content", category="news", is_active=True)
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            response = self.client.post(
                f"/post/{post_id}/update",
                data={
                    "title": "Updated Title",
                    "content": "Updated content body",
                    "category": "tech",
                    "is_active": "y",
                },
                follow_redirects=True,
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Updated Title", response.data)

            updated = db.session.get(Post, post_id)
            self.assertEqual(updated.title, "Updated Title")
            self.assertEqual(updated.content, "Updated content body")

    def test_delete_post(self):
        """US05: Видалення поста."""
        with self.app.app_context():
            post = Post(title="Post to Delete", content="Will be deleted", category="other")
            db.session.add(post)
            db.session.commit()
            post_id = post.id

            confirm_resp = self.client.get(f"/post/{post_id}/delete")
            self.assertEqual(confirm_resp.status_code, 200)
            self.assertIn(b"Post to Delete", confirm_resp.data)

            response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIsNone(db.session.get(Post, post_id))

    def test_404_not_found(self):
        """US06: 404 при відсутньому пості."""
        response = self.client.get("/post/9999")
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404", response.data)
        self.assertIn(b"Oops! Page Not Found", response.data)


if __name__ == "__main__":
    unittest.main()
