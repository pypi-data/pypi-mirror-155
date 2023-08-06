import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdktg",
    "version": "0.0.15",
    "description": "Agile Threat Modeling as Code",
    "license": "MIT",
    "url": "https://github.com/hupe1980/cdk-threagile.git",
    "long_description_content_type": "text/markdown",
    "author": "hupe1980",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/hupe1980/cdk-threagile.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdktg",
        "cdktg._jsii"
    ],
    "package_data": {
        "cdktg._jsii": [
            "cdktg@0.0.15.jsii.tgz"
        ],
        "cdktg": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "constructs>=10.1.42, <11.0.0",
        "jsii>=1.61.0, <2.0.0",
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
    "scripts": [
        "src/cdktg/_jsii/bin/cdktg"
    ]
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
