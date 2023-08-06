import setuptools, os

readme_path = os.path.join(os.getcwd(), "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r") as f:
        long_description = f.read()
else:
    long_description = 'kstopit'

setuptools.setup(
    name="kstopit",
    version="0.0.11",
    author="Kristof",
    description="kstopit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kkristof200/py_kstopit",
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp>=3.7.4.post0',
        'setuptools>=62.4.0',
        'stopit>=1.1.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)