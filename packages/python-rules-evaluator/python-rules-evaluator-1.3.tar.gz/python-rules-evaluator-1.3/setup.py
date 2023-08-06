import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-rules-evaluator',
    version=1.3,
    author='David Meyer',
    author_email='dameyerdave@gmail.com',
    description='Python Rules Evaluator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    url='https://github.com/dameyerdave/python-rules-evaluator',
    packages=setuptools.find_packages(exclude='test'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    install_requires=[
        'pyyaml',
        'friendlylog'
    ]
)
