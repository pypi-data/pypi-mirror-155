
from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="navigate-json",
    version="1.0.8",
    description="A Python package to inpsect/manage json objects.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://https://github.com/70Shubham07/json_navigator",
    author="70Shubham07",
    author_email="shubhamkwwr5@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["navJson"],
    include_package_data=True
    # install_requires=["requests"]
    # entry_points={
    #     "console_scripts": [
    #         "weather-reporter=weather_reporter.cli:main",
    #     ]
    # },
)