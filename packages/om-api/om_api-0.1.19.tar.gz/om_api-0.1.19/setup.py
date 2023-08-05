import setuptools

version = '0.1.19'
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name= 'om_api',
    version= version,
    author= 'Matvey Scherbakov',
    author_email= 'l89851175735@gmail.com',
    description= 'Functions to work with Optimacros API',
    long_description= long_description,
    long_description_content_type= 'text/markdown',
    url= 'https://github.com/pahMelnik/om_api',license= 'MIT see LICESE file',
    packages= ['om_api'],
    install_requires= ['requests', 'pandas'],
    classifiers=["Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent"]
)