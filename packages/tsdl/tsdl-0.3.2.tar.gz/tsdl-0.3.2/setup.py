import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tsdl",
    version="0.3.2",
    py_modules=['testcase'],
    author="zhangyue",
    author_email="zhangyue@techen.cn",
    description="Test Script Development Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/henry9000/tsdl",
    project_urls={
        "Bug Tracker": "https://gitee.com/henry9000/tsdl/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.9",
    install_requires=["requests"],
    package_data={
        'tsdl.config': ['config.ini'],
    },
)
