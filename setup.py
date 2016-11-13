from setuptools import setup

setup(
    name='leap',
    packages=['leap'],
    include_package_data=True,
    install_requires=[
        'flask',
        'werkzeug',
        'BeautifulSoup4',
        'PyPDF2',
        'nltk',
    ],
)
