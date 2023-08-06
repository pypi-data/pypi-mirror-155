from setuptools import setup

string = """
    A modmail for interactions.py\n\n
    Use with `bot.load("interactions.ext.modmail")`\n
    """

setup(
    name="interactions-modmail",
    version="1.0.0",
    description="Modmail for interactions.py",
    long_description=string,
    long_description_content_type="text/markdown",
    url="https://github.com/EdVraz/interactions-modmail",
    author="EdVraz",
    author_email="edvraz12@gmail.com",
    packages=["interactions.ext.modmail"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "discord-py-interactions>=4.1.2",
        "isodate",
        "python-dateutil",
        "dinteractions-Paginator",
        "interactions-get",
    ],
)
