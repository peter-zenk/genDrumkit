ERROR SETUP DOES NOT WORK
import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="genDrumkit",
    scripts=["src/genDrumkit",],
    version="0.1.3",
    author="Peter Zenk",
    author_email="email@peterzenk.de",
    description="Small tool to convert drum kits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/peter-zenk/genDrumkit",
    package_dir = { '': "src" },
    packages = [ "gen_drum_kit" , 
                  os.path.join( "gen_drum_kit", "builder"),
                  os.path.join( "gen_drum_kit", "drum_kit"),
                  os.path.join( "gen_drum_kit", "exporter"),
                  os.path.join( "gen_drum_kit", "importer"),
               ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires='>=3.8',
)
