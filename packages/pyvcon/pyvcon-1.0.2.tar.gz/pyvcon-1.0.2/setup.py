import os.path
import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, "README.md")) as f:
    README = f.read()

setuptools.setup(
    name="pyvcon",
    version="1.0.2",
    author="Olivier Mailhot",
    description="Python wrapper for Vcontacts",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/gregorpatof/pyvcon_package",
    packages=setuptools.find_packages('src'),
    package_dir={'':'src'},
    package_data={'pyvcon': ['vcontacts/*.c', 'vcontacts/*.h']},
    # test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)