from setuptools import setup, find_packages

setup(
    name='plagiarism_detector',
    version='0.1',
    packages=find_packages(),
    description='A simple plagiarism detector',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Godson Ajodo',
    author_email='godsonajodo2020@gmail.com'
    url='https://github.com/Ajodo-Godson/Plagiarism-Detector-with-CBF',
    # requirements here
    install_requires=[
        'requests',
        
    ],
)
