import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cod4-Rcon-sockets",
    version="0.0.2",
    author="Corey Koelewyn",
    author_email="Corey.koelewyn@gmail.com",
    description="Python Rcon handler for Cod4",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ckoelewyn/discon",
    project_urls={
        "Bug Tracker": "https://github.com/Ckoelewyn/discon/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)