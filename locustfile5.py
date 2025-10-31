from locust import HttpUser, task, between

#* mô phỏng đăng nhập và truy cập thông tin người dùng
class AuthUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        res = self.client.post("/auth/login", json={
            "username": "kminchelle",
            "password": "0lelplR"
        })
        self.token = res.json()["token"]

    @task
    def get_profile(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        self.client.get("/auth/me", headers=headers)
        
    
