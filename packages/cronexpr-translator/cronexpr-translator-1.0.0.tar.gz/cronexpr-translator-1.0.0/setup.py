from setuptools import setup, find_packages


setup(
    name='cronexpr-translator',
    version='1.0.0',
    license='MIT',
    author="poliambro",
    author_email='poliana.ambrosio.campos@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/poliambro/cronexpr-translator',
    keywords='cron expression translator',
    install_requires=[
          'cronexpr-validator',
      ],
)
