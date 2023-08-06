from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solidlab-perftest-upload",
    version="1.0.0",
    description="SolidLab Perftest Upload",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SolidLabResearch/solidlab-perftest-upload",
    author="Wim Van de Meerssche",
    author_email="wim.vandemeerssche@imec.be",
    license="EUPL-1.2",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["solidlab_perftest_upload"],
    install_requires=[
        "requests",
        "click",
        "solidlab-perftest-common",
    ],
    setup_requires=["pytest-runner", "black"],
    tests_require=["pytest"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "solidlab-perftest-upload=solidlab_perftest_upload.main:main",
        ],
    },
    # Zipped eggs don't play nicely with namespace packaging,
    # and may be implicitly installed by commands like python setup.py install.
    # To prevent this, it is recommended that you set zip_safe=False in setup.py
    zip_safe=False,
)
