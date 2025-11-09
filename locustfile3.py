from locust import HttpUser, task, between
import random
import threading
import requests


class RandomUserLogin(HttpUser):
    wait_time = between(1, 3)
    host = "https://dummyjson.com"
    users_data = []
    users_lock = threading.Lock()

    @classmethod
    def fetch_users_once(cls):
        with cls.users_lock:
            if cls.users_data:
                return
            try:
                res = requests.get("https://dummyjson.com/users?limit=208", timeout=10)
                res.raise_for_status()
                cls.users_data = res.json().get("users", [])
            except Exception:
                cls.users_data = []

    def on_start(self):
        self.fetch_users_once()

    @task
    def login_and_get_profile(self):
        if not self.users_data:
            return
        user = random.choice(self.users_data)
        username = user.get("username")
        password = user.get("password")
        if not username or not password:
            return
        login_resp = self.client.post(
            "/auth/login",
            json={"username": username, "password": password},
            name="/auth/login",
            timeout=30,
        )
        if not login_resp.ok:
            return
        token = (
            login_resp.json().get("token")
            or login_resp.json().get("accessToken")
            or login_resp.json().get("jwt")
        )
        if not token:
            return
        self.client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {token}"},
            name="/auth/me",
            timeout=30,
        )
