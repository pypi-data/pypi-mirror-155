import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name = "autopysta",
    version = "0.0.3.2",

    #namespace_packages = ['autopysta'],
    packages = ['autopysta'],
    #py_modules = ['autopysta'],
    #data_files = { 'autopysta': ['_autopysta.so', '_autopysta.pyd']} ,
    package_data = { 'autopysta':['*.so', '*.pyd']},
    include_package_data = True,
    #use2to3 >> Transformar codigo de python2 a python3

    #metadata to display on PyPi:
    author = "Rafael Delpiano",
    description = "2D traffic modeling.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://bitbucket.org/rdelpiano/autopysta/",

    classifiers = [
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix'
    ],

    python_requires = '==3.8.*',
)
