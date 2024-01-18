from srai_athena_frontend_telegram.generator_github import GeneratorGithub
from srai_athena_frontend_telegram.service_linkedin import ServiceLinkedin
from srai_athena_frontend_telegram.service_stabilityai import ServiceStabilityai


def main():
    dict_post = GeneratorGithub().generate()
    print(dict_post)
    ServiceStabilityai.initialize()
    ServiceLinkedin.initialize()
    ServiceLinkedin.get_instance().post_with_image_for_path_file(
        "post",
        "athena",
        "description",
        "77421994-7fd1-49a5-b009-7c36e1c3372c.png",
    )
    # ServiceLinkedin.get_instance().post_with_image_for_base64()


if __name__ == "__main__":
    main()
