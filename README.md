# Игра Судоку

Игра представляет собой реализацию [классической игры в судоку](https://ru.wikipedia.org/wiki/%D0%A1%D1%83%D0%B4%D0%BE%D0%BA%D1%83) на базе blockchain.
# Что нужно для игры

- Python 3.5
- Pygame
```sh
$ pip install pygame
```
- Solidity compiler
```sh
$ sudo add-apt-repository ppa:ethereum/ethereum
$ sudo apt-get update
$ sudo apt-get install solc
```
- py-solc
```sh
$ pip install py-solc
```
- eth-testrpc
```sh
$ pip install eth-testrpc
```
- Web3.py
```sh
$ pip install web3
```
# Как запускать
- python PlaySudoku.py

# Как играть
- Запустить
- Подождать генерацию и запись задачи судоку и ее решения в blockchain
- Играть

# Управление
- Стрелками (←, →, ↑, ↓)
- Либо курсором, кликая по ячейкам поля судоку
- Удалять проставленные значения можно с помощью клавишь: Space, Backspace, 0
- Значения ячеек проставляются цифрами 1 - 9