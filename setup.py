from setuptools import setup, find_packages

setup(
    name='site-mapper',
    version='0.5.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'site-mapper = site-mapper.sitemapper:main'
        ]
    },
    install_requires=[],
    author='Your Name',
    author_email='quantamstudios@gmail.com',
    description='A highly customizable tool to generate XML sitemaps for websites.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bob-el-bot/site-mapper',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
