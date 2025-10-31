from locust import HttpUser, task, between

class DummyJSONUser(HttpUser):
    wait_time = between(1, 3)  # người dùng "nghỉ" 1-3 giây giữa các request

    #* Kiem thu 1 endpoint
    @task
    def get_products(self):
        self.client.get("/products")  # gọi API chính
