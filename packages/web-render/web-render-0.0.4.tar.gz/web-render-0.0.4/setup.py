"""
Импорт недавно установленного пакета setuptools.
Upload package to PyPi.
python3 setup.py sdist старый способ
python3 setup.py bdist_wheel оптимальный

https://packaging.python.org/en/latest/tutorials/packaging-projects/
python3 -m build

### Установить локально
pip install ..web-render-0.0.1.tar.gz

### Установка в репозиторий
python3 -m twine upload --repository testpypi dist/*
python3 -m twine upload --repository pypi dist/*
python3 -m twine upload --skip-existing --repository pypi dist/*
"""
from setuptools import setup, find_packages
# from subprocess import Popen, PIPE


# with Popen("./develop/test.sh", shell=True, stdout=PIPE, stderr=PIPE) as proc:
#     proc.wait()
#     stdout = proc.stdout.read().decode("utf8")
#     stderr = proc.stderr.read().decode("utf8")
#     if proc.returncode != 0:
#         raise ValueError("Bad test")

# Открытие README.md и присвоение его long_description.
with open("README.md", "r") as fh:
    long_description = fh.read()

# Функция, которая принимает несколько аргументов. Она присваивает эти значения пакету.
setup(
    # Имя дистрибутива пакета. Оно должно быть уникальным, поэтому добавление вашего имени пользователя в конце является обычным делом.
    name="web-render",
    # Номер версии вашего пакета. Обычно используется семантическое управление версиями.
    version="0.0.4",
    # Имя автора.
    author="Andrey Plugin",
    # Его почта.
    author_email="9keepa@gmail.com",
    # Краткое описание, которое будет показано на странице PyPi.
    description="Web sites render.",
    # Длинное описание, которое будет отображаться на странице PyPi. Использует README.md репозитория для заполнения.
    long_description=long_description,
    # Определяет тип контента, используемый в long_description.
    long_description_content_type="text/markdown",
    # URL-адрес, представляющий домашнюю страницу проекта. Большинство проектов ссылаются на репозиторий.
    url="",
    # Находит все пакеты внутри проекта и объединяет их в дистрибутив.
    packages=["pyrender",
              "pyrender.http_service",
              "pyrender.http_service.api", "pyrender.selenium_service"],
    # requirements или dependencies, которые будут установлены вместе с пакетом, когда пользователь установит его через pip.
    install_requires=["Flask", "selenium", "selenium-stealth", "webdriver-manager", "waitress"],
    # Требуемая версия Python.
    python_requires='>=3.8',
    # лицензия
    license='Apache 2.0',
)