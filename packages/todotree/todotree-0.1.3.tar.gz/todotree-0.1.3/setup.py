import setuptools

with open("README.md", "r", encoding="utf-8" ) as f:
    long_description = f.read()

setuptools.setup(
    name = "todotree",
    version = "0.1.3",
    author = "Folkert Jansen",
    author_email = "fkjansen@protonmail.com",
    description = "A todo CLI application with tree display modes", 
    long_description=long_description,
    long_description_content_type="text/markdown",
    url = "https://gitlab.com/chim1aap/todotree",
    project_urls={
        "Bug Tracker": "https://gitlab.com/chim1aap/todotree/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
	python_requires = ">=3.9",
)

