import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="denemesonuc",
    version="0.0.5",
    author="insanolanbiri",
    description="orbim ölçme değerlendirme şeyi için bir modül",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/insanolanbiri/denemesonuc",
    project_urls={
        "Bug Tracker": "https://github.com/insanolanbiri/denemesonuc/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "selenium",
    ],
)
