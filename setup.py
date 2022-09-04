from setuptools import find_packages, setup

description = 'Flask Swagger generator for Schematics models.'

try:
    long_description = open('readme.md', 'r', encoding='utf8').read()
except Exception:
    long_description = description

setup(
    name='flask-schematics-swagger',
    version='0.0.6',
    author='Tarik Yilmaz',
    author_email='tarikyilmaz.54@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/trk54ylmz/flask-schematics-swagger',
    packages=find_packages(exclude=['example*', 'test*']),
    include_package_data=True,
    python_requires='>=3.7',
    install_requires=[
        'schematics>=2.1.1',
        'flask>=2.0.0',
        'wtforms>=2.2',
        'typing-extensions>=3.7.4.3'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
