from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Mojec core package'
LONG_DESCRIPTION = 'Package that holds all models and common ' \
                   'functions/classes of Mojec project'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="mojec_core",
    version=VERSION,
    author="Folayemi Bello",
    author_email="<bello.folayemi.az@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["django", "djangorestframework",
                      "djangorestframework-simplejwt", "drf-yasg",
                      "python-dotenv", "django-safedelete"],
    # add any
    # additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'mojec'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",

    ]
)
