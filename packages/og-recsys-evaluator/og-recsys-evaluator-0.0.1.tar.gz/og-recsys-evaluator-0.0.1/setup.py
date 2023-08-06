import setuptools

setuptools.setup(
    name="og-recsys-evaluator",
    version="0.0.1",
    author="OG",
    author_email="blogphp.biz@gmail.com",
    description="A small evaluator package",
    long_description="Evaluator for recommendation system algorithm",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.0",
)