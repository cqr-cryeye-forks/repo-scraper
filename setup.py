from setuptools import setup

setup(
      name='repo-scraper',
      version='0.2',
      description='Search for potential passwords/data leaks in a folder or git repo',
      url='https://github.com/zeinlol/repo-scraper',
      author='Mykola Borshchov & Eduardo Blancas Reyes',
      author_email='edu.blancas@gmail.com',
      license='MIT',
      packages=['repo_scraper', 'repo_scraper/constants', 'bin'],
      scripts=['bin/check_dir.py', 'bin/check_repo.py', 'repo-scraper'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False
      )
