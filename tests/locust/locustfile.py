import uuid
from locust import HttpUser, task, between, SequentialTaskSet


class BlogSequentialTaskSet(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = None
        self.post_id = None

    def on_start(self):
        self.username = f"user_{uuid.uuid4()}"

    @task
    def create_and_read_post_sequence(self):
        response = self.client.post("/posts", json={
            "author": self.username,
            "title": "New Post Title"
        }, name="/posts (create)")

        if response.status_code == 201:
            response_data = response.json()
            self.post_id = response_data.get("id")

            if self.post_id:
                self.client.get(f"/posts/{self.post_id}", name="/posts/[id] (get created)")
        else:
            print(f"Failed when creating post: {response.status_code}")


class BlogUser(HttpUser):
    wait_time = between(1, 3)
    tasks = [BlogSequentialTaskSet]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.specific_id = 1

    @task(5)
    def get_all_posts(self):
        self.client.get("/posts", name="/posts (get all)")

    @task(3)
    def get_specific_post(self):
        self.client.get(f"/posts/{self.specific_id}", name=f"/posts/{self.specific_id} (get specific)")