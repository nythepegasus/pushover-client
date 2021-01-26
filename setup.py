import setuptools

with open("README.md", "r", encoding="utf-8") as r:
    readme = r.read()

setuptools.setup(
    name="pushover-nythepegasus",
    version="1.0.0",
    author="Nythepegasus",
    author_email="nythepegasus84@gmail.com",
    description="A simple Pushover client written in Python.",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only"
    ],
    keywords="pushover, api, client",
    project_urls={
        'Source': 'https://github.com/Nythepegasus/pushover-client/',
        'Tracker': 'https://github.com/Nythepegasus/pushover-client/issues',
        'Say Thanks!': 'https://saythanks.io/to/nythepegasus84%40gmail.com'
    },
    install_requires=["requests"],
    python_requires=">=3",
)
