import setuptools

with open("README.md",'r') as f:
    long_description = f.read()
    
setuptools.setup(
    name="halfbrick_app_demo",
    version="0.1",
    scripts=[],
    author="Rachel Wu",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rachelwu21/halfbrick_app/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
    
