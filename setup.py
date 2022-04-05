from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="scrapping_vivareal",
    version="0.0.1",
    author="Wallison Rodrigues",
    author_email="wallisonlino137@gmail.com",
    description="Scrapping vivareal",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wallisonc2k/scrapping_vivareal.git"
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)