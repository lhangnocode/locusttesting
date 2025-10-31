from locust import HttpUser, task, between

class DummyJSONUser(HttpUser):
    wait_time = between(1, 3)

    #* kiem thu CRUD operations tren /posts endpoint
    @task
    def create_post(self):
        data = {"title": "Hello Locust", "userId": 5}
        self.client.post("/posts/add", json=data)

    @task
    def update_post(self):
        data = {"title": "Updated Title"}
        self.client.put("/posts/1", json=data)

    @task
    def delete_post(self):
        self.client.delete("/posts/1")
