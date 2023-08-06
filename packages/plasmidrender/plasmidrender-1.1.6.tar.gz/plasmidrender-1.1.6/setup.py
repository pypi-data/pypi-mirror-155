import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="plasmidrender",
    version="1.1.6",
    author="strelka",
    author_email="irohaprg@gmail.com",
    description="CLI tool to illustrate plasmids with a structure described by json.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/strelka145/Plasmid_render",
    install_requires=[
        "playwright",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
            'console_scripts':[
                'plasmidrender = plasmidrender.main:main_option',
            ],
        },
)
