from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cronexpr-validator',
    version='1.0.2',
    license='MIT',
    author="poliambro",
    author_email='poliana.ambrosio.campos@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/poliambro/cronexpr-validator',
    keywords='cron expression validator',
    install_requires=[],
)
