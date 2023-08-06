import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='slack-oauth-store',
    version='0.0.3',
    author='Ghawady Ehmaid',
    author_email='ghawady.ehmaid@gmail.com',
    description='Implementing Encrypted FileInstallationStore for Slack OAuth flow',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/morningcloud/slack_installation_store',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'slack_sdk>=3.17.0',
        'pyAesCrypt==6.0.0',
    ],
    python_requires='>=3.6',
)
