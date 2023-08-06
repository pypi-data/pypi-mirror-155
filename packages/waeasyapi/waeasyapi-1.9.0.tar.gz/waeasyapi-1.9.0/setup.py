from setuptools import setup

with open('README.md') as readme:
    readme_content = readme.read()

setup(
    name="waeasyapi",
    version="1.9.0",
    description="WA Easy API Python Client",
    long_description=readme_content,
    long_description_content_type='text/markdown',
    url="https://github.com/waeasyapi/waeasyapi-python",
    author="WA Easy API",
    license="MIT",
    install_requires=["requests"],
    include_package_data=True,
    package_dir={'waeasyapi': 'waeasyapi', 'waeasyapi.resources': 'waeasyapi/resources'},
    packages=['waeasyapi', 'waeasyapi.resources'],
    keywords=['waeasyapi', 'whatsapp business apis', 'waba', 'whatsapp'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",

        # List of supported Python versions
        # Make sure that this is reflected in .github/workflows/python.yml as well
        "Programming Language :: Python",
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
