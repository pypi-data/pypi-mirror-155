import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_info = {
    "name": "rodatabase.py",
    "version": "2.1.1",
    "author": "koen_1711",
    "description": "A Roblox Database API wrapper.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/koen1711/rodatabase.py",
    "packages": setuptools.find_packages(),
    "classifiers": [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development :: Libraries"
    ],
    "project_urls": {
        "Discord": "https://discord.gg/76kdgMd6h3",
        "GitHub": "https://github.com/koen1711/rodatabase.py",
    },
    "python_requires": '>=3.7',
    "install_requires": [
        "httpx>=0.21.0",
    ]
}


setuptools.setup(**setup_info)