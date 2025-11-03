from locust import HttpUser, task, between
import random
import time


class RandomUserLogin(HttpUser):
    """
    🔹 Simulates users logging into https://dummyjson.com with random credentials.
    """

    wait_time = between(1, 3)
    host = "https://dummyjson.com"
    MAX_LOGIN_ATTEMPTS = 5

    def on_start(self):
        """Executed once per simulated user."""
        self.token = None

        # Step 1: Fetch users
        try:
            res = self.client.get("/users", timeout=10)
            res.raise_for_status()
            users = res.json().get("users", [])
            if not users:
                print("[INIT] No users found.")
                return
        except Exception as e:
            print(f"[INIT] Failed to fetch /users: {e}")
            return

        # Step 2: Pick random user
        user = random.choice(users)
        username = user.get("username") or user.get("email") or user.get("firstName")
        print(f"[USER] Trying login for: {username}")

        # Step 3: Build candidate passwords
        pw_list = []
        if user.get("password"):
            pw_list.append(user["password"])
        if username:
            pw_list += [f"{username}123", f"{username}1234"]
        pw_list += ["123456", "password", "qwerty"]
        pw_list = list(dict.fromkeys(pw_list))[:self.MAX_LOGIN_ATTEMPTS]

        # Step 4: Attempt login
        for pw in pw_list:
            try:
                resp = self.client.post(
                    "/auth/login",
                    json={"username": username, "password": pw},
                    timeout=10,
                )
            except Exception:
                print(f"[LOGIN] Error with pw='{pw}' (connection issue)")
                time.sleep(0.5)
                continue

            if not resp.ok:
                print(f"[LOGIN] {username}: pw='{pw}' -> {resp.status_code}")
                if resp.status_code in (429, 503):
                    break
                continue

            data = resp.json()
            token = data.get("token") or data.get("accessToken") or data.get("jwt")
            if token:
                self.token = token
                self.current_user = username
                self.current_pw = pw
                print(f"[LOGIN] ✅ Success for '{username}' (pw='{pw}')")
                break

        # Step 5: Verify token
        if self.token:
            verify = self.client.get(
                "/auth/me", headers={"Authorization": f"Bearer {self.token}"}
            )
            print(
                f"[VERIFY] /auth/me -> {verify.status_code} ({'OK' if verify.ok else 'FAIL'})"
            )
        else:
            print(f"[LOGIN] ❌ All attempts failed for '{username}'")

    @task
    def get_profile(self):
        """Fetch profile using a valid token."""
        if not self.token:
            return  # Skip if no token

        res = self.client.get(
            "/auth/me", headers={"Authorization": f"Bearer {self.token}"}
        )
        print(f"[TASK] /auth/me -> {res.status_code}")
