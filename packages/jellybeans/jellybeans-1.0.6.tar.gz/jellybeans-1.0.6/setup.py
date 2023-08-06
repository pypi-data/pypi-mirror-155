from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='jellybeans',
    version='1.0.6',
    license='MIT',
    author='Lee Jia Jun',
    author_email='jiajunlee2@gmail.com',
    description="A Data Structure Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(exclude=['tests']),
    url='https://github.com/Jcheez/Jellybeans',
    keywords='Data-Structures',
    install_requires=[
        'matplotlib'
    ],
    python_requires=">=3.7"
)