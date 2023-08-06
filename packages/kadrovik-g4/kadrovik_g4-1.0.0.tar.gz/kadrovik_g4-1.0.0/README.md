![Language](https://img.shields.io/badge/English-brigthgreen)

# kadrovik

![PyPI](https://img.shields.io/pypi/v/kadrovik-g4)
![PyPI - License](https://img.shields.io/pypi/l/kadrovik-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kadrovik-g4)

Python module for take frames from video

***

## Installation

### Package Installation from PyPi

```bash
$ pip install kadrovik-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/kadrovik).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/kadrovik
$ cd kadrovik
$ pip install -r requirements.txt
$ pip install .
```

***

## Basic usage

- ### Import:
```python
from kadrovik_g4 import Kadrovik
```

- ### Create instance:
Create an instance of the Kadrovik. You can specify additional options:
- video - input video.
  Default value: ''
- frameN - extract frame number.
  Default value: 5
- outPath - Path to output frames.
  Default value: 'frame_%d.png'

```python
kadrovik = Kadrovik(frameN = 5, outPath = 'frames/frame_%d.png')
```

- ### Extract frames

```python
kadrovik.process('input.ts')
```

See the example.py file for an example of usage.

[Changelog](https://github.com/Genzo4/kadrovik/blob/main/CHANGELOG.md)
***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# kadrovik

![PyPI](https://img.shields.io/pypi/v/kadrovik-g4)
![PyPI - License](https://img.shields.io/pypi/l/kadrovik-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kadrovik-g4)

Python модуль для извлечения кадров из видео. 

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install kadrovik-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/kadrovik).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/kadrovik
$ cd kadrovik
$ pip install -r requirements.txt
$ pip install .
```

***

## Использование

- ### Подключаем:
```python
from kadrovik_g4 import Kadrovik
```

- ### Создаём экземпляр
Создаём экземпляр Kadrovik. Можно указать дополнительные параметры:
- video - входное видео.
  Значение по умолчанию: ''
- frameN - номер извлекаемых кадров.
  Значение по умолчанию: 5
- outPath - имя (и путь) извлекаемых кадров. Используется подстановка %d.
  Значение по умолчанию: 'frame_%d.png'

```python
kadrovik = Kadrovik(frameN = 5, outPath = 'frames/frame_%d.png')
```

- ### Извлекаем кадры

```python
kadrovik.process('input.ts')
```

Пример использования см. в файле example.py

[Changelog](https://github.com/Genzo4/kadrovik/blob/main/CHANGELOG.md)
