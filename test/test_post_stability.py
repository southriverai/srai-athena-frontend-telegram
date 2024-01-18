import json
import os

import requests

from srai_athena_frontend_telegram.generator_hackernews import GeneratorHackernews
from srai_athena_frontend_telegram.service_linkedin import ServiceLinkedin
from srai_athena_frontend_telegram.service_stabilityai import ServiceStabilityai


def main():
    ServiceStabilityai.initialize()
    ServiceLinkedin.initialize()
    generator_hackernews = GeneratorHackernews()
    if not os.path.exists("post.json"):
        post = generator_hackernews.generate()
        with open("post.json", "w") as f:
            json.dump(post, f)
    else:
        with open("post.json", "r") as f:
            post = json.load(f)

    if not os.path.exists("post.txt"):
        post_body = post["text generated"]
        title = generator_hackernews.generate_title(post_body)
        path_file_image = ServiceStabilityai.get_instance().get_text_to_image(title)
        print(path_file_image)

        post_text = title + "\n\n" + post_body + post["suffix"]

        with open("post.txt", "w") as f:
            f.write(post_text)
    else:
        with open("post.txt", "r") as f:
            post_text = f.read()

    print(post_text)
    ServiceLinkedin.get_instance().post(post_text)


if __name__ == "__main__":
    main()
