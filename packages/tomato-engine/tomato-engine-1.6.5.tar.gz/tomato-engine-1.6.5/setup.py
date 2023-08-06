import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tomato-engine",
    version="1.6.5",
    author="Eduardo Lopes Dias, Murilo Melhem",
    author_email="eduardosprp@usp.br",
    description="Engine for prototyping and playing with cellular automata",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://codeberg.org/eduardotogpi/tomato-engine",
    project_urls={
        "Bug Tracker": "https://codeberg.org/eduardotogpi/tomato-engine/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "numpy",
        "pygame",
        "pillow",
        "ipython",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)
