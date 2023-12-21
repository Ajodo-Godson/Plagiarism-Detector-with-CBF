from setuptools import setup, find_packages

setup(
    name='plagiarism_detector',
    version='0.1',
    packages=find_packages(),
    description='A simple plagiarism detector',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/Ajodo-Godson/Plagiarism-Detector-with-CBF',
    # requirements here
    install_requires=[
        'requests',
        
    ],
)
