import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "kong-control-plane",
    "version": "2.0.11",
    "description": "Kong CDK Construct Library to deploy Kong Control Plane on AWS",
    "license": "Apache-2.0",
    "url": "https://github.com/anshrma/kong-control-plane.git",
    "long_description_content_type": "text/markdown",
    "author": "Anuj Sharma<anshrma@amazon.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/anshrma/kong-control-plane.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "kong_control_plane",
        "kong_control_plane._jsii"
    ],
    "package_data": {
        "kong_control_plane._jsii": [
            "kong-control-plane@2.0.11.jsii.tgz"
        ],
        "kong_control_plane": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.13.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.61.0, <2.0.0",
        "kong-core>=2.0.16, <3.0.0",
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
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
