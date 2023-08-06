import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mca-projen-jsii-example",
    "version": "1.10.1",
    "description": "mca-projen-jsii-example",
    "license": "Apache-2.0",
    "url": "https://github.com/marciocadev/mca-projen-jsii-example.git",
    "long_description_content_type": "text/markdown",
    "author": "Marcio Cruz<marciocadev@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/marciocadev/mca-projen-jsii-example.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mca_projen_jsii_example",
        "mca_projen_jsii_example._jsii"
    ],
    "package_data": {
        "mca_projen_jsii_example._jsii": [
            "mca-projen-jsii-example@1.10.1.jsii.tgz"
        ],
        "mca_projen_jsii_example": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "jsii>=1.50.0, <2.0.0",
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
