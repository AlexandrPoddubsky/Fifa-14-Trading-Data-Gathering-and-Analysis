from setuptools import setup

setup(name='fut14analysis',
      version='1.0',
      packages=['fut14analysis', 'fut14gathering', 'fifa14search'],
      install_requires = ['fut14', 'pandas', 'google', 'beautifulsoup4'],
      package_data = {'fut14gathering': ['*.txt']},
      test_suite="nose.collector",
      tests_require="nose",
      author='Mateusz Khalil',
      author_email='mateuszk87@gmail.com',
      description='Using this library it is very simple to collect and analyze trading data coming from Fifa 14 Ultimate Team.'
)
