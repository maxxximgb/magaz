import os
import urllib.request
from pathlib import Path
import pip
from pkg_resources import working_set, Requirement, VersionConflict, DistributionNotFound

clear_console = lambda: os.system('cls' if os.name == 'nt' else 'clear')

class RequirementsInstaller:
    def __init__(self):
        self.requirements_file = Path(__file__).parent / 'requirements.txt'
        self.requirements = self._parse_requirements()

    def _parse_requirements(self):
        if not self.requirements_file.exists():
            raise FileNotFoundError("requirements.txt not found in module directory")

        requirements = []
        with open(self.requirements_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith(('#', '-')):
                    try:
                        Requirement.parse(line)  # Валидация синтаксиса
                        requirements.append(line)
                    except ValueError:
                        print(f"Ignoring invalid requirement: {line}")
        return requirements

    def check(self):
        """Проверяет соответствие версий пакетов"""
        missing = []
        for req in self.requirements:
            try:
                working_set.require(req)
            except (DistributionNotFound, VersionConflict):
                missing.append(req)
        return missing

    def install(self):
        """Устанавливает недостающие пакеты с учётом версий"""
        missing = self.check()
        if not missing:
            return True

        print(f'У вас не установлены нужные для работы сервера зависимости, такие как:\n'
               f'{'\n'.join(missing)}.'
               f'\nНажмите Enter, и программа попробует установить их вместо вас, или прервите её и установите их сами.')
        input()
        if not self._check_pypi_availability():
            print(f'PYPI недоступен. Попробуйте позже, или установите зависимости вручную.')
            return False

        try:
            for dep in missing:
                print(f'Устанавливаем зависимость {dep}...')
                pip.main(['install', '--quiet', dep])
                print(f'Зависимость {dep} установлена.')

            # subprocess.run(
            #     [sys.executable, '-m', 'pip', 'install', '--quiet'] + missing,
            #     check=True,
            #     stdout=subprocess.DEVNULL,
            #     stderr=subprocess.DEVNULL
            # )
            clear_console()
            return True
        except Exception as e:
            print(f"Ошибка установки: {e}")
            return False

    def _check_pypi_availability(self):
        try:
            urllib.request.urlopen('https://pypi.org', timeout=5)
            return True
        except Exception as e:
            print(f"Ошибка подключения к PyPI: {e}")
            return False


def install():
    installer = RequirementsInstaller()
    installer.install()


install()
