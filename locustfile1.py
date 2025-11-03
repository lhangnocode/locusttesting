from locust import HttpUser, task, between
import random
import string


class DummyJSONUser(HttpUser):
    """
    🔹 Simulates users interacting with the public API at https://dummyjson.com
    🔹 Tasks are weighted to mimic realistic user behavior distribution.
    """

    wait_time = between(1, 2)
    host = "https://dummyjson.com"

    # ----------------------------
    # 🔹 TASK GROUP: GET requests
    # ----------------------------

    @task(5)
    def get_products(self):
        """Fetch a list of products (most frequently accessed)."""
        self.client.get("/products", name="/products")

    @task(1)
    def get_users(self):
        """Fetch a list of users."""
        self.client.get("/users", name="/users")

    @task(4)
    def get_posts(self):
        """Fetch a list of posts."""
        self.client.get("/posts", name="/posts")

    # ----------------------------
    # 🔹 TASK GROUP: CRUD operations with dynamic data
    # ----------------------------

    @task(3)
    def create_post(self):
        """Create a new post with random title and userId."""
        title = "Post " + "".join(random.choices(string.ascii_letters, k=6))
        data = {"title": title, "userId": random.randint(1, 136)}

        with self.client.post(
            "/posts/add", json=data, name="/posts/add", catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"❌ POST request failed ({response.status_code})")

        # After creating, fetch posts again to measure latency and system responsiveness
        self.client.get("/posts", name="/posts (after add)")

    @task(2)
    def update_post(self):
        """Update a random existing post."""
        post_id = random.randint(1, 150)
        new_title = "Updated " + "".join(random.choices(string.ascii_uppercase, k=5))
        data = {"title": new_title}

        with self.client.put(
            f"/posts/{post_id}",
            json=data,
            name="/posts/:id (update)",
            catch_response=True,
        ) as response:
            if response.status_code != 200:
                response.failure(
                    f"❌ PUT request failed for ID {post_id} ({response.status_code})"
                )

    @task(1)
    def delete_post(self):
        """Delete a random post."""
        post_id = random.randint(1, 150)
        with self.client.delete(
            f"/posts/{post_id}", name="/posts/:id (delete)", catch_response=True
        ) as response:
            if response.status_code not in [200, 204]:
                response.failure(
                    f"❌ DELETE request failed for ID {post_id} ({response.status_code})"
                )
