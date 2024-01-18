import base64
import os

import requests


class ServiceLinkedin:
    _instance: "ServiceLinkedin" = None  # type: ignore

    @staticmethod
    def get_instance() -> "ServiceLinkedin":
        if ServiceLinkedin._instance is None:
            raise Exception("ServiceSceduling not initialized")
        return ServiceLinkedin._instance

    @staticmethod
    def initialize() -> None:
        ServiceLinkedin._instance = ServiceLinkedin()

    def __init__(self):
        self.api_key_linkedin = os.environ["LINKEDIN_TOKEN"]
        if self.api_key_linkedin is None:
            raise Exception("LINKEDIN_TOKEN not set")

    def post(self, text: str):
        base_url = "https://linkedin-api-wrapper.onrender.com/"

        post_url = base_url + "create/linkedin_post"
        payload = {
            "accessToken": self.api_key_linkedin,
            "text": text,
        }
        response = requests.post(post_url, json=payload)
        print(response.json())

    def post_with_image(self, text: str, image_title: str, image_description: str, image_url: str) -> str:  # type: ignore
        url = "https://linkedin-wrapper1.p.rapidapi.com/create/linkedin_post/image"

        payload = {"text": text, "mediaUrl": "", "imageTitle": image_title, "imageDescription": image_description}
        headers = {
            "content-type": "application/json",
            "Authorization": "<REQUIRED>",
            "X-RapidAPI-Key": "SIGN-UP-FOR-KEY",
            "X-RapidAPI-Host": "linkedin-wrapper1.p.rapidapi.com",
        }

        response = requests.post(url, json=payload, headers=headers)

        print(response.json())

    def post_with_image_for_path_file(
        self,
        text: str,
        image_title: str,
        image_description: str,
        path_file_image: str,
    ) -> None:  # type: ignore
        with open(path_file_image, "rb") as f:
            image_base64 = base64.b64encode(f.read()).decode("utf-8")
        print(image_base64[:10])
        exit()
        url = "https://linkedin-api-wrapper.onrender.com/create/linkedin_post/image"
        headers = {
            "content-type": "application/json",
            "Authorization": "Bearer " + self.api_key_linkedin,
        }
        payload = {
            "text": text,
            "mediaUrl": "",
            "base64string": "data:image/png;base64," + image_base64,
            "imageTitle": image_title,
            "imageDescription": image_description,
        }

        response = requests.post(url, json=payload, headers=headers)
        print(response.json())

    def post_with_image_for_base64(self) -> None:  # type: ignore
        url = "https://linkedin-api-wrapper.onrender.com/create/linkedin_post/image"
        print(self.api_key_linkedin)
        headers = {
            "content-type": "application/json",
            "Authorization": "Bearer " + self.api_key_linkedin,
        }
        payload = {
            "text": "Test post with base64 image",
            "mediaUrl": "",
            "base64string": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==",
            "imageTitle": "Test Image",
            "imageDescription": "A small red dot",
        }
        print("done")
        response = requests.post(url, json=payload, headers=headers)
        print(response.json())
