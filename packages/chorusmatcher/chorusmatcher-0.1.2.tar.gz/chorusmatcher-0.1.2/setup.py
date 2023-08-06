from setuptools import setup, find_packages

setup(
    name='chorusmatcher',
    version='0.1.2',
    install_requires=['requests'],
    packages=['chorusmatcher'],
    entry_points={
        'console_scripts': [
            'chorusmatcher = chorusmatcher.main:main'
        ]
    },
    python_requires='>=3.6'
)
