from setuptools import setup, find_packages

long_description = """
Asynctlg is an asynchronous Python interface for the Telegram Bot API. It is tested with python 3.5.2.

you can install or upgrade with pypi:
pip install asynctlg
"""

setup(
    name='asynctlg',
    version='0.1.0',

    description='Asynchronous python interface for the Telegram Bot API',
    long_description=long_description,

    url='https://github.com/RevengeComing/asynctlg',
    author='Sepehr Hamzelooy',
    author_email='s.hamzelooy@gmail.com',
    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.5',
    ],
    install_requires=['requests', 'requests_toolbelt'],
    packages=find_packages(),

    keywords='telegram bot',
)