from setuptools import find_packages, setup


# todo remove this
def read_setup_cfg() -> dict:
    path_file_setup_cfg = "setup.cfg"
    dict_setup_cfg = {}
    with open(path_file_setup_cfg, "r") as file_setup_cfg:
        list_line = file_setup_cfg.readlines()
        for line in list_line:
            if "=" not in line:
                continue
            key = line.split("=")[0]
            value = line.split("=")[1]
            key = key.strip()
            value = value.strip()
            value = value.replace('"', "")
            dict_setup_cfg[key] = value
    return dict_setup_cfg


# todo remove this
def read_module_init() -> dict:
    dict_setup_cfg = read_setup_cfg()
    module_name = dict_setup_cfg["module-name"]
    path_file_module_init = f"{module_name}/__init__.py"
    dict_module_init = {}
    with open(path_file_module_init, "r") as file_module_init:
        list_line = file_module_init.readlines()
        for line in list_line:
            key = line.split("=")[0]
            value = line.split("=")[1]
            key = key.strip()
            value = value.strip()
            value = value.replace('"', "")
            dict_module_init[key] = value
    return dict_module_init


module_init = read_module_init()

with open("README.md", "r") as f:
    long_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name=module_init["__title__"],
    packages=find_packages(),
    version=module_init["__version__"],
    license="MIT",
    package_data={},
    python_requires=">=3.5",
    install_requires=requirements,
    author="Jaap Oosterbroek",
    author_email="jaap.oosterbroek@southriverai.com",
    description="A telegram frontend for srai services.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/southriverai/srai-athena-frontend-telegram",
    download_url="https://github.com/southriverai/srai-athena-frontend-telegram/archive/v_01.tar.gz",
    keywords=["SRAI", "TOOLS"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",  # Define that your audience are developers
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",  # Again, pick a license
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
