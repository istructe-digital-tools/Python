from setuptools import setup, find_packages

setup(
    name="DesignCodes",
    version="0.1.0",
    author="IStructE",
    author_email="@",
    description="A Python project for engineering calculations and design equations.",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "EC0": ["definitions.csv"],
    },
    install_requires=[],
    license="Fair Source License",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
