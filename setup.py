from setuptools import setup


setup(
    name='pystatsd',
    version='1.0.0',
    description='Python statsd server.',
    long_description="Python statsd server",
    url="https://github.com/bdastur/utils",
    author="Behzad Dastur",
    author_email="bdastur@gmail.com",
    license='Apache Software License',
    install_requires=[
            'kafka-python',
            'PyYAML'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'License :: Apache Software License',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
    ],
    entry_points={
        'console_scripts': [
            'pystatsd = pystatsd.stats_server:main'
        ]
    },
    keywords='statsd',
    packages=["pystatsd"],
    data_files=[('/etc/pystatsd', ['pystatsd/etc/pystats/pystatsd.conf']),
                ('/etc/init', ['pystatsd/etc/init/pystatsd.conf'])]
)
