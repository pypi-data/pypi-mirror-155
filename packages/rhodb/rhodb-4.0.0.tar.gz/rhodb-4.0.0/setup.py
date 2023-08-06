import re
import ast
import os
import sys
import shutil

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import coverage
        import pytest

        if self.pytest_args and len(self.pytest_args) > 0:
            self.test_args.extend(self.pytest_args.strip().split(' '))
            self.test_args.append('tests/')

        cov = coverage.Coverage()
        cov.start()
        errno = pytest.main(self.test_args)
        cov.stop()
        cov.report()
        cov.html_report()
        print("Wrote coverage report to htmlcov directory")
        sys.exit(errno)


do_cythonize = os.getenv('CYTHONIZE', 'false').lower() == 'true'
ext_modules = []
cmdclass = {'test': PyTest}
packages = find_packages(exclude=["tests"])

if do_cythonize:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext

        class MyBuildExt(build_ext):
            def run(self):
                build_ext.run(self)
                build_dir = os.path.realpath(self.build_lib)
                root_dir = os.path.dirname(os.path.realpath(__file__))
                target_dir = build_dir if not self.inplace else root_dir
                self.copy_file('rhodb/__init__.py', root_dir, target_dir)

            def copy_file(self, path, source_dir, destination_dir):
                if os.path.exists(os.path.join(source_dir, path)):
                    shutil.copyfile(os.path.join(source_dir, path),
                                  os.path.join(destination_dir, path))

        cmdclass['build_ext'] = MyBuildExt
        ext_modules = cythonize("rhodb/*.py")
        packages = []

    except ImportError:
        pass


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('rhodb/__init__.py', 'rb') as f:
    __version__ = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

setup(
    name='rhodb',
    version=__version__,
    description="Pit Rho Generic Database Helpers",
    long_description=open('README.md', 'r').read(),
    maintainer="Pit Rho Corporation",
    license="Commercial",
    url="https://bitbucket.org/pitrho/rhodb",
    packages=packages,
    include_package_data=True,
    install_requires=[],
    ext_modules=ext_modules,
    extras_require={
        'sqlalchemy': [
            'SQLAlchemy>=0.9.2,<1',
            'python-dateutil==2.4.2'
        ],
        'flask_sqlalchemy': [
            'SQLAlchemy>=0.9.2,<1',
            'Flask>=0.10.1,<1.0',
            'Flask-SQLAlchemy>=2.1,<3.0',
            'python-dateutil==2.4.2'
        ],
        'redis': ['redis>=2.9.1'],
        'cassandra': ['cassandra-driver>=3.1.1,<4'],
        'cassandra_redis': [
            'cassandra-driver>=3.1.1,<4',
            'redis>=2.9.1'
        ],
        'aws': [
            'boto3>=1.2.3,<2'
        ],
        'elasticsearch': [
            'elasticsearch>=6.3,<7.0',
            'requests-aws4auth>=0.9,<1.0',
            'elasticsearch-dsl>=6.2,<7.0',
        ],
        'arangodb': [
            'python-arango >=3.12.1, < 4'
        ],
        'test': [
            'tox==2.6.0'
        ],
        'dev': [
            'cython'
        ]
    },
    cmdclass=cmdclass
)
