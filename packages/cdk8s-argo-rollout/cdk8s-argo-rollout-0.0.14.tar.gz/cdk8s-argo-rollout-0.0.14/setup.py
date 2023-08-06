import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-argo-rollout",
    "version": "0.0.14",
    "description": "@opencdk8s/cdk8s-argo-rollout",
    "license": "Apache-2.0",
    "url": "https://github.com/opencdk8s/cdk8s-argo-rollout",
    "long_description_content_type": "text/markdown",
    "author": "Sumit Agarwal<sa.sumit@outlook.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/opencdk8s/cdk8s-argo-rollout"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_argo_rollout",
        "cdk8s_argo_rollout._jsii",
        "cdk8s_argo_rollout.k8s"
    ],
    "package_data": {
        "cdk8s_argo_rollout._jsii": [
            "cdk8s-argo-rollout@0.0.14.jsii.tgz"
        ],
        "cdk8s_argo_rollout": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "cdk8s>=2.2.74, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.46.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
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
