import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-qa",
    version="0.0.4",
    author="Starkov E.G.",
    author_email="Starkov.Ev.Ge@gmail.com",
    license="Apache 2.0",
    description="Simplify the QA of your product",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Starkov-EG/python-qa",
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
