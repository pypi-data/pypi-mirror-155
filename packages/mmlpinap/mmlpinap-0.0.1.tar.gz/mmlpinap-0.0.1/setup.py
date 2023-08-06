import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mmlpinap",
    version="0.0.1",
    author="Akash Sonowal",
    author_email="akashsonowal.cheme@gmail.com",
    description="Modern Machine Learning Practices in Asset Pricing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akashsonowal/modern-ml-in-asset-pricing",
    project_urls={
        "Bug Tracker": "https://github.com/akashsonowal/modern-ml-in-asset-pricing/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)