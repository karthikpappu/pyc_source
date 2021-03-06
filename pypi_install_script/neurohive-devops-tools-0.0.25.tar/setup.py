import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="neurohive-devops-tools",
    version="0.0.25",
    author="Dmitriy Shelestovskiy",
    author_email="one@sonhador.ru",
    description="Neurohive devops tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    #url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'bb-trigger=neurohive.integration.bitbucket:main',
            'bb-check-prs-branch=neurohive.integration.bitbucket:check_branch',
            'jira-add-comment=neurohive.integration.jirawrap:main',
            'uc-run-build=neurohive.integration.unitycloud:run_build',
            'uc-clone-build-from-branch=neurohive.cli.commands:create_and_build_from_prs',
            "ac-cleanup-builds=neurohive.cli.commands:cleanup_old_appcenter_build",
            "deploy-ecs-task=neurohive.cli.commands:deploy_ecs_task"
        ]
    },
    install_requires=[
        "requests==2.22.0",
        "jira==2.0.0",
        "boto3==1.12.28"
    ]
)
