from setuptools import setup

setup(
    name='trueway_geocoding_rapidapi',
    version='0.2.3',
    description='TrueWay Geocoding API on RapidAPI',
    packages=['trueway_geocoding_rapidapi', 'trueway_geocoding_rapidapi.schemas'],
    author_email='dshvedov@kotspin.ru',
    zip_safe=False,
    author='Daniil Shvedov',
    keywords=['rapidapi', 'trueway', 'geocoding'],
    classifiers=[],
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/dankaprogg/trueway_geocoding_rapidapi',
)
