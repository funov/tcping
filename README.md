# TCPing

Автор: `@s_vanyaa`

## Описание

Аналог консольной утилиты ping. Отправляет Echo запросы по протоколу ICMP. По завершении строит статистику

## Состав

* Точка входа, передача ключей `tcping.py`
* Связующий узел `ping_process.py`
* Тесты `tests/tests.py`
* Вывод информации на консоль `utils/printer.py`
* Работа с замерами времени `utils/timer.py`
* Формирование ICMP запроса `network/icmp_echo_request.py`
* Класс ICMP ответа `network/icmp_echo_reply.py`
* Конфигурация и работа с RAW socket `network/icmp_socket.py`

## Требования

* RAW socket
* ICMP протокол

## Реализация

Структура ICMP Echo сообщения:

```
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Type      |     Code      |          Checksum             |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |           Identifier          |        Sequence Number        |
   +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   |     Data ...
   +-+-+-+-+-
```

Алгоритм нахождения checksum:

```
The checksum is the 16-bit ones's complement of the one's
complement sum of the ICMP message starting with the ICMP Type.
For computing the checksum , the checksum field should be zero.
If the total length is odd, the received data is padded with one
octet of zeros for computing the checksum.  This checksum may be
replaced in the future.
```

Вроде все уже написано, но есть нюанс...

## Тесты

Частично протестированы:

* `utils/printer.py`
* `network/icmp_echo_request.py`
* `network/icmp_echo_reply.py`

## Запуск

Реализован подробный и понятный help

`sudo python3 tcping.py -h`

Вот он:

```
TODO
```
