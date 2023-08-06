from importlib.metadata import entry_points
from gwfp import settings
from setuptools import setup,find_packages

setup(
    name = settings.name,
    version = settings.version,
    description = settings.description,
    author = settings.author,
    author_email = settings.author_email,
    packages = find_packages(exclude=settings.exclude_packages),
    url = settings.project_url,
    entry_points = settings.entry_points,
    classifiers = settings.classifiers,
    license = settings.license,
    license_files = settings.license_files,
    keywords = settings.keywords,
    install_requires = settings.install_requires,
    python_requires = settings.python_requires,
    include_package_data = settings.include_package_data,
)
