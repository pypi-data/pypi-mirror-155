import os
from setuptools import setup, find_packages

this_dir = os.path.abspath(os.getcwd())

with open(os.path.join(this_dir, "README.md"), "rb") as fo:
    long_description = fo.read().decode("utf8")

setup(
    name="django_posts_api",
    version="0.0.3",
    author="Fadi Ghattas",
    author_email="fadighattas100@outlook.com",
    description="A small example plugin package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fadighattas100/django_posts_api",
    project_urls={
        "Bug Tracker": "https://github.com/fadighattas100/django_posts_api/issues",
    },
    download_url="https://github.com/fadighattas100/django_posts_api/blob/master/dist/django_posts_api-0.0.3.tar.gz",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    include_package_data=True,
    install_requires=[],
    extras_require={
        'dev': []
    }
)
