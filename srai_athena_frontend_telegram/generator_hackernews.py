import json
import os
from typing import Dict, List

import requests
from bs4 import BeautifulSoup
from hackernews import HackerNews
from openai import OpenAI

from srai_athena_frontend_telegram.generator_post import GeneratorPost


class GeneratorHackernews:
    def __init__(self):
        pass

    def generate(self):
        hn = HackerNews()

        list_story = hn.top_stories()
        dict_story = {}
        for story in list_story:
            dict_story[story.title] = story.item_id

        list_selected_title = self.select_title(list(dict_story.keys()))

        # cache stories
        post_template = self.build_template(dict_story, list_selected_title)

        post = GeneratorPost().generate(post_template)

        return post

    # promt openai
    def select_title(self, list_title: List[str]) -> dict:
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

        promt = """
        Given the following list of blog post titles, select the three best ones for a blog on a for a socail media AI company:
        """
        promt += f"{list_title}"
        promt += """
        Do not include any explanations, only provide a RFC8259 compliant JSON response following this format without deviation.
        {
            "list_selection": [
                {
                    "title": "title_0"
                }
            ]
        }
        """

        system_message = {
            "role": "system",
            "content": "You are a asssitent for selecting content for blog posts",
        }
        promt_message = {
            "role": "user",
            "content": promt,
        }
        list_message = []
        list_message.append(system_message)
        list_message.append(promt_message)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=list_message,
            temperature=1,
        )
        print(response.choices[0].message)
        return json.loads(response.choices[0].message.content)

    def build_template(self, dict_story: Dict[str, str], list_selected_title: dict) -> dict:
        hn = HackerNews()
        dict_prompt = {}
        dict_prompt[
            "goal"
        ] = """
        Create a blog post that relates to the datasources for a socail media AI company of araound 500 words.
        The company is called South River AI they are developing Athena a social media interaction application.
        The application is designed to help users interact with social media in a more productive way.
        It systhesizes posts from a variety of sources and presents them to the user in a way that is more condusive to productivity.
        """
        dict_prompt["list_data_source"] = []
        for title in list_selected_title["list_selection"]:
            try:
                item = hn.get_item(dict_story[title["title"]], expand=True)
                print(item.title)
                print(item.url)
                if item.text is None:
                    html_text = requests.get(item.url).content.decode("utf8")
                    text = self.extract_text_from_html(html_text)
                else:
                    text = item.text
                dict_prompt["list_data_source"].append({"title": item.title, "url": item.url, "text": text[:1000]})
            except Exception as e:
                print(e)
                continue
        return dict_prompt

    # parse text
    def extract_text_from_html(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        return soup.get_text(separator="\n", strip=True)
