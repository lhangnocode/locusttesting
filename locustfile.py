from locust import HttpUser, task, between

# Một "người dùng ảo" (virtual user)
class DummyUser(HttpUser):
    # Mỗi người dùng sẽ đợi 1-3 giây giữa các yêu cầu
    wait_time = between(1, 3)

    # Đường dẫn mặc định tới API DummyJSON
    host = "https://dummyjson.com"

    @task
    def get_products(self):
        # Lấy danh sách sản phẩm
        self.client.get("/products")

    @task
    def get_users(self):
        # Lấy danh sách người dùng
        self.client.get("/users")

    @task
    def get_posts(self):
        # Lấy danh sách bài viết
        self.client.get("/posts")

    @task
    def search_product(self):
        # Tìm kiếm sản phẩm có từ khóa "phone"
        self.client.get("/products/search?q=phone")
