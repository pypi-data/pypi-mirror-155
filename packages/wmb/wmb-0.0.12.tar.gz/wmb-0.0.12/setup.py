from setuptools import setup, find_packages

setup(
    name="wmb",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Hanqing Liu",
    author_email="hanliu@salk.edu",
    description="misc code for whole mouse brain analysis.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lhqing/whole_mouse_brain",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=find_packages(exclude=("docs", "test")),
    package_data={"": ["*.gz", "*.csv", "*.tsv", "*.hdf", '*.lib', '*.txt']},
    include_package_data=True,
    install_requires=[
        "numpy",
        "pandas",
        "xarray",
        "seaborn",
        "matplotlib",
        "ALLCools"
    ]
)
