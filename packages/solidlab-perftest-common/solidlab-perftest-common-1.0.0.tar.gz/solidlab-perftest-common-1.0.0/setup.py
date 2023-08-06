from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="solidlab-perftest-common",
    version="1.0.0",
    description="SolidLab PerfTest Common",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.ilabt.imec.be/ilabt/solidlab-perftest-common",
    author="Wim Van de Meerssche",
    author_email="wim.vandemeerssche@imec.be",
    license="EUPL-1.2",
    classifiers=[
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=["solidlab_perftest_common"],
    install_requires=[
        "python-dateutil",
        "requests",
    ],
    python_requires=">=3.7",
    entry_points={
    },
    # Zipped eggs don't play nicely with namespace packaging,
    # and may be implicitly installed by commands like python setup.py install.
    # To prevent this, it is recommended that you set zip_safe=False in setup.py
    zip_safe=False,
)
