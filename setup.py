import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="walmart_store_scraper", # Replace with your own username
    version="0.0.1",
    author="Kushagra Pandey",
    author_email="kushagra.pandey@gmail.com",
    description="A basic scraper to find walmart stores nearby all pincodes in USA",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kushagra2240/wmstorescraper.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)