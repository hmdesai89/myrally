#from distutils.core import setup
from glob import glob
from setuptools import find_packages
from setuptools import setup
from os.path import splitext
from os.path import basename

#from pip.req import parse_requirements

#install_reqs = parse_requirements('requirements.txt', session=False)
#reqs = [str(ir.req) for ir in install_reqs]


reqs = ['python_jcsclient == 1.0',
        'requests == 2.10.0',
        'setuptools == 20.7.0',
        'six == 1.10.0',
        'xmltodict == 0.9.0',
        'pycrypto == 2.6.1',
        'posix_ipc == 1.0.0',
        'PyYAML == 3.11']



#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.
files = ["myrally/*"]

setup(name = "myrally",
    version = "0.1.0",
    description = "Custom framework for concurrent testing with multiple users",
    author = "Harsh Desai",
    author_email = "harsh1.desai@ril.com",
    #Name the folder where your packages live:
    #(If you have other packages (dirs) or modules (py files) then
    #put them into the package directory - they will be found 
    #recursively.)
    packages=find_packages('.'),
    #package_dir={'': '.'},
    #py_modules=['myrally/test_client/'+splitext(basename(path))[0] for path in glob('myrally/test_client/*.py')],
    #packages = ['myrally'],
    #'package' package must contain files (see list above)
    #I called the package 'package' thus cleverly confusing the whole issue...
    #This dict maps the package name =to=> directories
    #It says, package *needs* these files.
    package_data = {'myrally' : files },
    #'runner' is in the root.
    scripts = ["bin/myrally"],
    long_description = """Really long text here.""" ,
    install_requires=reqs
    #
    #This next part it for the Cheese Shop, look a little down the page.
    #classifiers = []     

) 
