from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'LDM package '
LONG_DESCRIPTION = "easy way to fix error with ldm not found"

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="ldm",
    version=VERSION,
    author="Anton Marchevskii",
    author_email="<avatarnarod@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'ldm'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities'
    ]
)