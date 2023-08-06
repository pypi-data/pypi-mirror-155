![Language](https://img.shields.io/badge/English-brigthgreen)

# PolyFiller

![PyPI](https://img.shields.io/pypi/v/polyfiller-g4)
![PyPI - License](https://img.shields.io/pypi/l/polyfiller-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/polyfiller-g4)

Python module for polygon filling on images.

***

## Installation

### Package Installation from PyPi

```bash
$ pip install polyfiller-g4
```

### Package Installation from Source Code

The source code is available on [GitHub](https://github.com/Genzo4/polyfiller).  
Download and install the package:

```bash
$ git clone https://github.com/Genzo4/polyfiller
$ cd polyfiller
$ pip install -r requirements.txt
$ pip install .
```

***

## Basic usage

- ###Import:
```python
from polyfiller_g4 import PolyFiller
```

- ### Create instance:
Create an instance of the PolyFiller. You can specify additional options:
- ext - extension to add to the output file.
  Default value: fill.
- color - filling color.
  Default value: 0 (black).

```python
pf = PolyFiller(ext='add_ext', color=(255, 0, 0))
```

- ### Add filling polygons (0 or many)
```python
pf.addPolygon([[0, 0], [1919, 0], [1919, 682], [1277, 385], [951, 374], [0, 615]])
pf.addPolygon([[100, 100], [200, 100], [150, 150]])
```

- ### Filling frame
```python
pf.fill('frame_1.png')
pf.fill('frame_2.png')
...
pf.fill('frame_n.png')
```
Output files are created with the extension added.

![Input frame](https://github.com/Genzo4/polyfiller/raw/main/images/frame_1.png "Input frame")
![Output frame](https://github.com/Genzo4/polyfiller/raw/main/images/frame_1.fill.png "Output frame")

See the example.py file for an example of usage.

***

![Language](https://img.shields.io/badge/Русский-brigthgreen)

# PolyFiller

![PyPI](https://img.shields.io/pypi/v/polyfiller-g4)
![PyPI - License](https://img.shields.io/pypi/l/polyfiller-g4)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/polyfiller-g4)

Python модуль для заливки многоугольника\ов на изображении однотонным цветом. 

***

## Установка

### Установка пакета с PyPi

```bash
$ pip install polyfiller-g4
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/polyfiller).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/polyfiller
$ cd polyfiller
$ pip install -r requirements.txt
$ pip install .
```

***

## Использование

Подключаем:
```python
from polyfiller_g4 import PolyFiller
```

Создаём экземпляр PolyFiller. Можно указать дополнительные параметры:
- ext - расширение, добавляемое к выходному файлу.
  Значение по умолчанию: fill.
- color - цвет заливки.
  Значение по умолчанию: 0 (чёрный цвет).

```python
pf = PolyFiller(ext='add_ext', color=(255, 0, 0))
```

- ### Добавляем полигоны для заливки (0 или много)
```python
pf.addPolygon([[0, 0], [1919, 0], [1919, 682], [1277, 385], [951, 374], [0, 615]])
pf.addPolygon([[100, 100], [200, 100], [150, 150]])
```

- ### Заливка изображений
```python
pf.fill('frame_1.png')
pf.fill('frame_2.png')
...
pf.fill('frame_n.png')
```
Создаются выходные файлы с добавленным расширением.

![Input frame](https://github.com/Genzo4/polyfiller/raw/main/images/frame_1.png "Input frame")
![Output frame](https://github.com/Genzo4/polyfiller/raw/main/images/frame_1.fill.png "Output frame")

Пример использования см. в файле example.py
