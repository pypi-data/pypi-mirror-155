from setuptools import setup, find_packages

VERSION = '0.1.4' 
DESCRIPTION = 'Fensterbemaßung'
LONG_DESCRIPTION = 'Programm zum automatisierten Bemaßen von Fenster- und Rahmenteilen die als XML formatiert vorliegen'


setup(
       # the name must match the folder name 'STcreateFigure'
        name="STcreateFigure", 
        version=VERSION,
        author="Richard Oberreitecr",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        package_data = {'':['utils/fonts/*.ttf'],'utils':['utils']},
        # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        install_requires=['matplotlib','numpy','pandas','PyQt5','setuptools-changelog','python-barcode'],
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)