#!/usr/bin/env python3
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='section9_tools',
    version='0.0.2',
    author='sunyi00',
    author_email='sunyi00@gmail.com',
    description='section9 daily tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/T-G-Family/section9-lib-tools',
    project_urls={
        "Bug Tracker": "https://github.com/T-G-Family/section9-lib-tools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "arrow",
        "requests",
        "EbookLib",
        "Faker",
        "arrow",
        "requests",
        "pillow",
        "streamlit",
        "watchdog",
        "colorthief",
        "opencv-python",
        "imagehash",
        "fire",
    ],
    extras_require={
        'dev': [
            "pip-tools",
            "build",
            "twine",
        ],
        'test': [
            "pytest",
            "pytest-mock",
            "pytest-cov",
            "black",
            "coverage",
            "flake8",
            "mypy",
            "ipython",
            "pynvim",
            "pylint",
            "isort",
            "pipdeptree",
            "pep8",
            "autopep8",
        ],
    },
    entry_points={'console_scripts': [
        'section9-epub-maker = section9.epub_maker:main',
        'section9-pic-maker = section9.pic_maker:main',
    ]},
    namespace_packages=['section9'],
    zip_safe=False,
)
