import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "aws_prototyping_sdk.identity",
    "version": "0.0.95",
    "description": "@aws-prototyping-sdk/identity",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-prototyping-sdk",
    "long_description_content_type": "text/markdown",
    "author": "AWS APJ COPE<apj-cope@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/aws/aws-prototyping-sdk"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_prototyping_sdk.identity",
        "aws_prototyping_sdk.identity._jsii"
    ],
    "package_data": {
        "aws_prototyping_sdk.identity._jsii": [
            "identity@0.0.95.jsii.tgz"
        ],
        "aws_prototyping_sdk.identity": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.28.1, <3.0.0",
        "aws-cdk.aws-cognito-identitypool-alpha>=2.28.1.a0, <3.0.0",
        "constructs>=10.1.42, <11.0.0",
        "jsii>=1.61.0, <2.0.0",
        "projen>=0.58.15, <0.59.0",
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
