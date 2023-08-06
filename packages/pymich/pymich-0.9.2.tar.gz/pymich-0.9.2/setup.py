from setuptools import setup


setup(
    name='pymich',
    version='0.9.2',
    setup_requires='setupmeta',
    install_requires=['pytezos>=3.5.1', 'cli2', 'pygments'],
    extras_require=dict(
        test=[
            'freezegun',
            'pytest',
            'pytest-cov',
        ],
    ),
    author='Thomas Binetruy',
    author_email='tbinetruy@gmail.com',
    url='https://yourlabs.io/piratzlabs/pymich',
    include_package_data=True,
    license='MIT',
    keywords='cli',
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'pymich = pymich.pymich:cli.entry_point',
        ],
    },
)
