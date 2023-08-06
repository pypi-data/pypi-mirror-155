from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='acdh-cfts-pyutils',
    version='0.1',
    description='Python Package to interact with a dedicated Typesense Server and Collection',
    url='https://github.com/acdh-oeaw/acdh-cfts-pyutils',
    author='Peter Andorfer',
    author_email='peter.andorfer@oeaw.ac.at',
    license='MIT',
    packages=['acdh_cfts_pyutils'],
    zip_safe=False,
    install_requires=[
        'typesense==0.14.0'
    ],
    long_description=readme,
    long_description_content_type='text/markdown',
)
