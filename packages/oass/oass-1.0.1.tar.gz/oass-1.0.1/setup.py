from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="oass",
    version="1.0.1",
    author="Artiprocher",
    author_email="zjduan@stu.ecnu.edu.cn",
    description="Optimal Action Space Search (OASS) is an algorithm for path planning problems on directed acyclic graphs (DAG) based on reinforcement learning (RL) theory.",
    url="https://github.com/ECNU-CILAB/OASS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages()
)
