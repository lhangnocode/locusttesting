from locust import HttpUser, task, between
import random


class ImageTestUser(HttpUser):
    """
    🔹 Simulates users requesting random images from https://dummyjson.com
    🔹 Each request has a random size, text, and image format.
    🔹 Prints out the full image URL for verification.
    """

    host = "https://dummyjson.com"
    wait_time = between(1, 3)

    @task
    def get_random_image(self):
        """
        🔸 Request a random image with:
          - Random size between 100x100 and 800x600
          - Random image type (jpg, png, webp)
          - Random text label
        """
        width = random.randint(100, 800)
        height = random.randint(100, 600)
        image_type = random.choice(["jpg", "png", "webp"])
        text = random.choice(["Hello", "Locust", "Testing", "Random", "LoadTest"])

        # Build full URL for DummyJSON
        path = f"/image/{width}x{height}?type={image_type}&text={text}"
        full_url = f"{self.host}{path}"

        # ✅ Print the image link
        print(f"[REQUEST] 🖼️ {full_url}")

        # Send GET request
        with self.client.get(path, name="/image/random", catch_response=True) as res:
            if res.status_code != 200:
                res.failure(f"❌ Failed with status {res.status_code}")
            else:
                res.success()
