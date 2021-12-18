import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pysintegra',
    version='0.8',
    author='Felipe Correa',
    author_email='eu@felps.dev',
    description='Gerador do arquivo magnético Sintegra',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/felps-dev/pysintegra',
    project_urls={
        "Bug Tracker": "https://github.com/felps-dev/pysintegra/issues"
    },
    license='LGPL',
    packages=['pysintegra'],
)
