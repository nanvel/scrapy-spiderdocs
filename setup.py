# -*- encoding: utf-8 -*-
from setuptools import setup, find_packages

try:
    with open('README.rst', encoding="utf-8") as readme:
        long_description=readme.read()
except:
    long_description=''


VERSION = '0.1.3'

setup(
    name='scrapy-spiderdocs',
    version=VERSION,
    url='https://github.com/nanvel/scrapy-spiderdocs',
    project_urls={
        'Documentation': 'https://github.com/nanvel/scrapy-spiderdocs',
        'Source': 'https://github.com/nanvel/scrapy-spiderdocs',
        'Tracker': 'https://github.com/nanvel/scrapy-spiderdocs/issues',
    },
    description='Generate spiders md documentation based on spider docstrings.',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Oleksandr Polieno',
    author_email='polyenoom@gmail.com',
    license='MIT License',
    platforms=['OS Independent'],
    python_requires=">=3.7",
    install_requires=['scrapy>=2.0'],
    py_modules=['scrapy-spiderdocs'],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'scrapy.commands': [
            'spiderdocs=documented.commands.spiderdocs:Command',
        ],
    },
    keywords='scrapy, spiders, documentation',
    classifiers=[
        'Framework :: Scrapy',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Documentation',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
