# requirements_installer.py
import sys
import urllib.request
from pathlib import Path
from importlib.metadata import distributions, PackageNotFoundError
from setuptools import setup
from pkg_resources import working_set, Requirement


class RequirementsInstaller:
    def __init__(self):
        self.requirements_file = Path(__file__).parent / 'requirements.txt'
        self.requirements = self._parse_requirements()

    def _parse_requirements(self):
        if not self.requirements_file.exists():
            raise FileNotFoundError("requirements.txt not found in module directory")

        with open(self.requirements_file, 'r') as f:
            return [
                line.strip() for line in f
                if line.strip() and not line.startswith(('#', '-'))
            ]

    def check(self):
        """Проверяет установленные пакеты"""
        installed = set()
        for dist in distributions():
            try:
                installed.add(dist.metadata['Name'].lower())
            except PackageNotFoundError:
                continue

        missing = []
        for req in self.requirements:
            try:
                working_set.require(req)
            except Exception:
                pkg_name = Requirement.parse(req).key
                missing.append(pkg_name)

        return missing

    def install(self):
        """Устанавливает недостающие пакеты"""
        if not self._check_pypi_availability():
            return False

        missing = self.check()
        if not missing:
            print("All requirements already satisfied")
            return True

        try:
            setup(
                name='_temp_requirements_install',
                version='0.0',
                install_requires=missing,
                script_args=['-q', 'bdist_wheel'],
                options={'bdist_wheel': {'universal': True}}
            )
        except Exception as e:
            print(f"Installation failed: {e}")
            return False

        return True

    def _check_pypi_availability(self):
        try:
            urllib.request.urlopen('https://pypi.org', timeout=5)
            return True
        except Exception as e:
            print(f"PyPI connection error: {e}")
            return False


def install():
    installer = RequirementsInstaller()
    return installer.install()


def check():
    return RequirementsInstaller().check()
