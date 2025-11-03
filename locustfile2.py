from locust import HttpUser, task, between
import random


class ImageTestUser(HttpUser):
    """
    🔹 Simulates users requesting random images from https://dummyimage.com
    🔹 Each request has a random size, background/text color, text, and format.
    🔹 Useful for testing performance and cache efficiency under variable workloads.
    """

    host = "https://dummyimage.com"
    wait_time = between(1, 3)

    @task
    def get_random_image(self):
        """
        🔸 Request a random image with:
          - Random size between 100x100 and 800x600
          - Random background and text colors (hex)
          - Random image type (jpg, png, webp)
          - Random text label
        """
        # Generate random image parameters
        width = random.randint(100, 800)
        height = random.randint(100, 600)
        bg_color = f"{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        text_color = f"{random.randint(0, 255):02x}{random.randint(0, 255):02x}{random.randint(0, 255):02x}"
        image_type = random.choice(["jpg", "png", "webp"])
        text = random.choice(["Hello", "Locust", "Testing", "Random", "LoadTest"])

        # Build request path
        path = (
            f"/{width}x{height}/{bg_color}/{text_color}?text={text}&type={image_type}"
        )

        # Send GET request
        self.client.get(path, name="/image/random")
