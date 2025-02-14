from setuptools import *


def after_install():
    try:
        import nltk
        nltk.download('vader_lexicon')
    except ModuleNotFoundError:
        print("nltk module not properly installed")


setup(
    name='Grace',
    version='2.2.0',
    author='Code Society Lab',
    description='The Code Society community Bot',
    url="https://github.com/Code-Society-Lab/grace",
    project_urls={
        "Documentation": "https://github.com/Code-Society-Lab/grace/wiki",
        "Issue tracker": "https://github.com/Code-Society-Lab/grace/issues",
        "Discord server": "https://discord.gg/code-society-823178343943897088",
    },
    license="GNU General Public License v3.0",
    python_requires='>=3.9.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-dotenv',
        'coloredlogs',
        'logger',
        'sqlalchemy',
        'sqlalchemy-utils',
        'discord>=2.0',
        'emoji>=2.1.0',
        'nltk',
        'discord-pretty-help==1.3.4',
        'requests',
        'pillow',
        'geopy',
        'pytz',
        'timezonefinder',
        'mypy',
        'alembic',
        'configparser',
        'pygithub',
        'googletrans==4.0.0-rc1'
    ],
    scripts=['bin/grace']
)

after_install()
