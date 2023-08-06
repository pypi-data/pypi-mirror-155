from setuptools import setup, Extension, find_packages


VERSION = '0.0.6'
DESCRIPTION = 'The Tipo Library consists of great AI tools'

# Setting up
setup(
    name="Tipo",
    version=VERSION,
    author="Liam Nordvall",
    author_email="<liam_nordvall@hotmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['numpy', 'gs'],
    keywords=['python', 'deeplearning', 'AI', 'machine learning'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
