import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
f = open("requirements.txt","w")
f.write('requests\nos\nsys\nuser_agent\nsecrets\njson')

fr = open("requirements.txt",'r')
requires = fr.read().split('\n')
    
setuptools.setup(
    name="GDO_Email",
    version="0.1.0",
    author="GDOTools",
    author_email="GDOTools@gmail.com",
    description="• Script To Check Email .",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GDOTools/GDO-Email",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=requires,
)
