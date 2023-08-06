from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

with open('HISTORY.md') as history_file:
    HISTORY = history_file.read()

setup_args = dict(
    name='Fliicoin',
    version='0.1.7',
    description='Useful API commands to interact with the fliicoin network.',
    long_description_content_type="text/markdown",
    long_description=README + '\n\n' + HISTORY,
    license='MIT',
    packages=find_packages(),
    author='Fliicoin',
    author_email='admin@fliicoin.com',
    keywords=['Fliicoin', 'Flii', 'Fliic', 'Fliicoin.com', 'Fliicoin api', 'Flii api'],
    url='https://github.com/Fliicoin/Fliicoin-API',
    download_url='https://pypi.org/project/Fliicoin-API/'
)

install_requires = [
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)