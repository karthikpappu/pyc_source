from setuptools import setup, find_packages

setup(name="slack_zendesker",
    version="1.1",
    description="Slack Zendesk URL expander",
    classifiers=[
        "Programming Language :: Python",
    ],
    author="Nikola Kotur",
    author_email="kotnick@gmail.com",
    url="https://github.com/kotnik/slack-zendesker",
    download_url="https://github.com/kotnik/slack-zendesker/archive/1.1.zip",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "slackbot",
    ],
    entry_points={
        "console_scripts": [
            'slack_zendesker = slack_zendesker.main:main',
        ],
    },
)
