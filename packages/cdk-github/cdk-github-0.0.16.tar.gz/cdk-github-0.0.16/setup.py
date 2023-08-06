import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-github",
    "version": "0.0.16",
    "description": "AWS CDK Construct Library to interact with GitHub's API.",
    "license": "MIT",
    "url": "https://github.com/WtfJoke/cdk-github",
    "long_description_content_type": "text/markdown",
    "author": "Manuel",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/WtfJoke/cdk-github"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdkgithub",
        "cdkgithub._jsii"
    ],
    "package_data": {
        "cdkgithub._jsii": [
            "cdk-github@0.0.16.jsii.tgz"
        ],
        "cdkgithub": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.25.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.60.1, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
