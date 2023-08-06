import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="AutoKS",
    version="0.0.27",
    author="Wei Zi-Qian",
    author_email="weiziqian1996@163.com",
    description="An easy-to-used Python package to process knowledge structure data automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/weiziqian1996/AutoKS",
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=['numpy', 'pywebview', 'networkx'],
    packages=setuptools.find_packages(include=['d3v3', 'example', 'AutoKS'])
)
