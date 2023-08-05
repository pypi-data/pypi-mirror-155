import setuptools
import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join(path, filename).replace("src/andisdk/", ""))
    return paths

dlls = package_files('src/andisdk/dlls')
setuptools.setup(
    name="andisdk",
    version="0.0.42",
    author="Technica Engineering",
    description="ANDi python package to interact with ANDi scripting features from stand alone python package",
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    install_requires=[
        "pythonnet==2.5.2;python_version<'3.0'",
        "pythonnet==3.0.0a2;python_version>='3.0'",
        "udsoncan==1.14;python_version>='3.0'",
        "rich>=11.2"
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux"
    ],
    package_data={
        '': dlls + ['*.pyi', 'runtimeconfig.json', 'SmartBind-Server.WibuCmLif'],
    },
    py_modules=['andisdk'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
)
