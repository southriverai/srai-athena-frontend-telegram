import os

import requests


def main():
    base_url = "https://linkedin-api-wrapper.onrender.com/"
    accessToken = os.environ["LINKEDIN_TOKEN"]
    post_url = base_url + "create/linkedin_post"
    text = """
    In this era of information overload, maintaining productivity has become a significant challenge. Social media platforms are continuously bombarded with data, often leading to distraction and decreased productivity for users. South River AI is tackling this conundrum head-on with their new application, Athena. This social media interaction application is uniquely designed to synthesize posts from an array of sources and present them to users in a way that enhances productivity, filtering out the noise and focusing on what truly matters.
    Drawing inspiration from the latest research in artificial intelligence, South River AI has incorporated powerful algorithms that form the backbone of Athena. A remarkable paper titled "Turing Complete Transformers: Two Transformers Are More Powerful Than One," sheds light on the \'Find+Replace transformers’ - multi-transformer architectures that outperform single transformers in terms of computational capacity and generalization. Athena leverages similar principles to efficiently compress and curate content, making it impressively user-friendly and effective.
    Yet, as we forge ahead with advancements in AI, we are confronted with unique challenges, particularly in terms of ethical considerations and fair use of content. OpenAI recently drew attention when it claimed that The New York Times had tricked its AI model, ChatGPT, into copying its articles. Despite this controversy, OpenAI emphasized the role of AI models in absorbing and repurposing the vast pool of human knowledge available on the internet, falling under \'fair use\' rules. South River AI aligns with this notion, ensuring that Athena adheres strictly to fair use policies while delivering premium content to users.
    In conclusion, South River AI's Athena is a promising venture in the realm of social media productivity. Powered by cutting-edge AI research and meticulously designed to respect fair use policies, Athena is opening new avenues for users to interact with social media content productively. By integrating advancements in AI and addressing contemporary challenges, South River AI is paving the way for more sophisticated and ethical use of technology in our daily lives.
    Generation Code Repo
    https://lnkd.in/eTXDGWxY
    Content repo
    https://lnkd.in/e9ZhJeQZ
    """
    payload = {
        "accessToken": accessToken,
        "text": text,
    }
    requests.post(post_url, json=payload)


if __name__ == "__main__":
    main()
