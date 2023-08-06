from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="discord-ext-better-options-description",
    version="1.0",
    description="Discord.py extension to keep your slash commands options neat and tidy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nohet/discord-ext-better-options-description",
    author="Nohet",
    author_email="igorczupryniak503@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    keywords=["discord", "discord extension", "discord.py", "slashcommands"],
    packages=["discord.ext.better_options_description"],
    install_requires=["discord.py", "PyYAML"],
    dependency_links=["https://github.com/Rapptz/discord.py"],
)
