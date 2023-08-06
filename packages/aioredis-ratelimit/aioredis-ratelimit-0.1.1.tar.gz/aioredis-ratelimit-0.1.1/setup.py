import sys
from pathlib import Path

sys.path.append(str(Path('src').absolute()))

from setuptools import setup, find_packages

import aioredis_ratelimit


setup(
    name='aioredis-ratelimit',
    version=aioredis_ratelimit.__version__,
    description='An asyncio coroutine decorator for limiting calls\' rate based on Redis backend and aioredis library.',
    long_description=Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    author='Konstantin Tolstikhin',
    author_email='k.tolstikhin@gmail.com',
    url='https://github.com/ktolstikhin/aioredis-ratelimit.git',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.6',
    install_requires=[
        'aioredis>=2,<3',
    ],
    keywords=[
        'decorator',
        'ratelimit',
        'aioredis',
        'redis',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
    ],
    zip_safe=False,
)
