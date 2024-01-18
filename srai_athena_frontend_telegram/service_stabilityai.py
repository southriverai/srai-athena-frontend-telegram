import base64
import os
from typing import Dict, List
from uuid import uuid4

import requests


class ServiceStabilityai:
    _instance: "ServiceStabilityai" = None  # type: ignore

    @staticmethod
    def get_instance() -> "ServiceStabilityai":
        if ServiceStabilityai._instance is None:
            raise Exception("ServiceSceduling not initialized")
        return ServiceStabilityai._instance

    @staticmethod
    def initialize() -> None:
        ServiceStabilityai._instance = ServiceStabilityai()

    def __init__(self):
        self.api_key_stabilityai = os.environ.get("STABILITYAI_API_KEY")
        if self.api_key_stabilityai is None:
            raise Exception("STABILITYAI_API_KEY not set")

    def get_text_to_image(self, prompt: str) -> str:
        list_text_prompt = [{"text": prompt, "weight": 1}, {"text": "blurry, bad", "weight": -1}]
        return self.get_text_to_image_for_list(list_text_prompt)  # type: ignore

    def get_text_to_image_for_list(self, list_text_prompt: List[Dict]) -> str:  # type: ignore
        url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

        body = {
            "steps": 40,
            "width": 1024,
            "height": 1024,
            "seed": 0,
            "cfg_scale": 5,
            "samples": 1,
            "text_prompts": list_text_prompt,
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": self.api_key_stabilityai,
        }

        response = requests.post(
            url,
            headers=headers,
            json=body,
        )

        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
        guid = str(uuid4())
        path_file_target = guid + ".png"
        for i, image in enumerate(data["artifacts"]):
            with open(path_file_target, "wb") as f:
                f.write(base64.b64decode(image["base64"]))

        return path_file_target
