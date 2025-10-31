from locust import HttpUser, task

class ImageTestUser(HttpUser):
    
    #* Kiem thu endpoint /image
    @task
    def get_image(self):
        self.client.get("/image/400x200/282828/eae0d0?text=HelloLocust&type=jpg")
