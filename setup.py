from setuptools import find_packages, setup

setup(
    name='spotitag',
    version='0.1',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'spotipy',
    ],
)
