import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rimu",
    version="11.3.0",
    author="Stuart Rackham",
    author_email="srackham@gmail.com",
    license="MIT",
    description="Rimu is a readable-text to HTML markup language inspired by AsciiDoc and Markdown.",
    keywords="rimu markdown asciidoc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/srackham/rimu-py",
    project_urls={
        'Documentation': 'https://srackham.github.io/rimu/',
        'Source': 'https://github.com/srackham/rimu-py',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    entry_points={
        'console_scripts': [
            'rimupy=rimuc.rimuc:main',
        ],
    },
)
