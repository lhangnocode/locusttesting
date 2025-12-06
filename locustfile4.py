from locust import HttpUser, task, between
from locust import LoadTestShape
import random
import string
import math


class DummyJSONUser(HttpUser):
    wait_time = between(5, 15)
    host = "https://dummyjson.com"

    @task(5)
    def get_products(self):
        self.client.get("/products", name="/products")

    @task(1)
    def get_users(self):
        self.client.get("/users", name="/users")

    @task(4)
    def get_posts(self):
        self.client.get("/posts", name="/posts")

    @task(3)
    def create_post(self):
        """Create a new post with random title and userId."""
        title = "Post " + "".join(random.choices(string.ascii_letters, k=6))
        data = {"title": title, "userId": random.randint(1, 136)}

        with self.client.post(
            "/posts/add", json=data, name="/posts/add", catch_response=True
        ) as response:

            if response.status_code not in [200, 201]:
                response.failure(f"❌ POST request failed ({response.status_code})")

        self.client.get("/posts", name="/posts (after add)")

    @task(2)
    def update_post(self):
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
                    f"PUT request failed for ID {post_id} ({response.status_code})"
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
                    f"DELETE request failed for ID {post_id} ({response.status_code})"
                )


# -----------------------------------------------------
# 👇👇 ADD WAVE LOAD TEST SHAPE HERE
# -----------------------------------------------------

class WaveShape(LoadTestShape):
    """
    Hình wave (dạng sóng sin):
    - Số user dao động liên tục lên xuống.
    - max_users: đỉnh cao nhất của wave
    - period: thời gian 1 chu kỳ sóng (giây)
    """

    max_users = 100          # Số user tối đa trong 1 wave
    period = 10             # Thời gian 1 chu kỳ (10 giây)
    spawn_rate = 5          # Tốc độ tạo user

    def tick(self):
        run_time = self.get_run_time()

        # Công thức sóng sin: users = A * (sin(x) + 1)
        radians = 2 * math.pi * (run_time / self.period)
        wave_value = (math.sin(radians) + 1) / 2   # chuẩn hóa về [0,1]

        users = int(self.max_users * wave_value)

        return users, self.spawn_rate
