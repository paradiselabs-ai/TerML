from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="terml",
    version="0.2.0",
    author="Paradise Labs",
    author_email="developers@paradiselabs.co",
    description="TerML - AI-powered Terminal Assistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pryh4ck/terml",
    packages=find_packages(),
    install_requires=[
        "anthropic==0.7.2",
        "click==8.1.3",
        "python-dotenv==1.0.0",
    ],
    entry_points={
        'console_scripts': [
            'terml=terml.main:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    include_package_data=True,
    package_data={
        'terml': ['config.py'],
    },
)