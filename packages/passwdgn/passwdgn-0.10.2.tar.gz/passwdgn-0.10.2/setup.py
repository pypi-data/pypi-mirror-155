import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name = 'passwdgn',
                 version = '0.10.2',
                 author = 'Amirreza Soltani',
                 author_email = 'charleswestmorelandPB1@gmail.com',
                 description = 'A library to generate a password for registering on a website.',
                 long_description = long_description,
                 long_description_content_type = 'text/markdown',
                 packages = setuptools.find_packages(where = "src"),
                 classifiers = ['Programming Language :: Python :: 3', 
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows'],
                 package_dir = {"" : "src"},
                 python_requires = '>=3.6',
                 install_requires=[])