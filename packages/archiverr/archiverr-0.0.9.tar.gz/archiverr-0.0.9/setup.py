import setuptools, os

with open("README.md", "r") as fh:
    long_description = fh.read()

def get_packages(package):
    """Retourne les dossiers où un fichier __init__.py est présent
    
    Paramètres
        package(Str): le dossier à parcourir

    Retourne
        liste(list): liste des dossiers
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]
        
setuptools.setup(
     name='archiverr',  
     version='0.0.9', #0.4.4 test server
     scripts=['archiver'] ,
     author="Théo Hurlimann",
     author_email="theo.hrlmn@eduge.ch",
     description="Archiver is a tool to archive, search and extract files and folders based on his sha1",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/theohrlmnn/archiver",
     #packages=['src'],
     packages=get_packages("src"),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: BSD License",
         "Operating System :: POSIX :: Linux",
     ],
    #setup_requires=["numpy"],
    install_requires=[
        "setuptools>=62",
        "Flask>=2.1.1",
        "numpy>=1.22.3",
        "pandas>=1.4.2",
        "py7zr>=0.17.4",
        "toml>=0.10.0",
        "orjson>=3.6.7",
        "python-magic>=0.4.26",
        "progress>=1.6",
    ],
    python_requires='>=3.10',

 )