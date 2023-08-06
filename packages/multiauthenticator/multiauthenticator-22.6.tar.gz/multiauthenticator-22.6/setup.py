from setuptools import setup


# Read version and other metadata from file
__version__ = '22.06'

with open('README.md') as f:
    long_description = f.read()

setup(
    name='multiauthenticator',
    py_modules=['multiauthenticator'],
    version=__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='An authenticator plugin for JupyterHub that allows you to configure several authentication services.',
    author='Thorin Tabor',
    author_email='tmtabor@cloud.ucsd.edu',
    url='https://github.com/g2nb/multiauthenticator',
    download_url='https://github.com/g2nb/multiauthenticator/archive/' + __version__ + '.tar.gz',
    keywords=['Jupyter', 'Authenticator'],
    python_requires=">=3.6",
    license='BSD',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
    ],
)
