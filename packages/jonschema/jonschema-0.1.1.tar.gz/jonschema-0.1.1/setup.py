from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='jonschema',
    version='0.1.1',
    description='jonschema is a dependency allowing you to validate multiple data types in a precise and fast way',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='BILOG NTOUBA Célestin',
    author_email='ntoubacelestin98@gmail.com',
    keywords=['schema', 'validator', 'json', 'hivi'],
    url='https://ntouba98@bitbucket.org/ntouba98/jonschema.git',
    download_url='https://pypi.org/project/jonschema/'
)

install_requires = [
    'python>2.0',
    'Django>1.0',
]

if __name__ == '__main__':
    setup(
        **setup_args,
        install_requires=install_requires,
        include_package_data=True,
    )