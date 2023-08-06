import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="drt-gui",
    version="0.0.2",
    author="Dmitry Trokhachev",
    author_email="dimiaa573@gmail.com",
    description="GUI for photo restoration app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dimiaa/drt-gui",
    project_urls={
        "Bug Tracker": "https://github.com/dimiaa/drt-gui/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    package_dir={"drt_gui": "drt_gui"},
    install_requires=[
       'numpy',
       'PySide2',
       'shiboken2',
       'drt-telea',
       'drt-unet'
    ],
    python_requires=">=3.6,<3.11",
)