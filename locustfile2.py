from locust import HttpUser, task, between

class DummyJSONUser(HttpUser):
    wait_time = between(1, 2)

    #* Kiem thu nhieu endpoint voi trong so khac nhau
    @task(3)
    def get_products(self):
        self.client.get("/products")

    @task(2)
    def get_users(self):
        self.client.get("/users")

    @task(1)
    def get_posts(self):
        self.client.get("/posts")
