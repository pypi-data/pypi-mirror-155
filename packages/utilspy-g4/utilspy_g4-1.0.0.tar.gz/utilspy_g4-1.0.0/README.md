![Language](https://img.shields.io/badge/English-brigthgreen)

# utilspy

![PyPI](https://img.shields.io/pypi/v/utilspy-g4)
![PyPI - License](https://img.shields.io/pypi/l/utilspy-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utilspy-g4)


Small utils for python

***

## Installation

### Package Installation from PyPi

```bash
$ pip install utilspy-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/utilspy).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/utilspy
$ cd utilspy
$ pip install .
```

***

## Utils

- ### addExt
Add ext to path.

Support Windows and Linux paths.

```python
from utilspy_g4 import addExt

path = '/test/test.png'
ext = '2'
newPath = addExt(path, ext)     # newPath = '/test/test.2.png'
```

***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# utilspy

![PyPI](https://img.shields.io/pypi/v/utilspy-g4)
![PyPI - License](https://img.shields.io/pypi/l/utilspy-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/utilspy-g4)

Небольшие утилитки для Python.

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install utilspy-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/utilspy).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/utilspy
$ cd utilspy
$ pip install .
```

***

## Утилиты

- ### addExt
Добавляет дополнительное расширение файла перед его последним расширением.

Обрабатывает как Windows пути, так и Linux.

```python
from utilspy_g4 import addExt

path = '/test/test.png'
ext = '2'
newPath = addExt(path, ext)     # newPath = '/test/test.2.png'
```
