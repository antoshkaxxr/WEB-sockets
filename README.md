# WEB-sockets

## Запуск веб-сервера
Склонируйте репозиторий и из папки с проектом в командной строке введите команду:

```python chat.py```

Будет выведено сообщение о том, что веб-сервер запущен:

======== Running on http://0.0.0.0:8080 ========

(Press CTRL+C to quit)

Откройте в браузере ```http://0.0.0.0:8080``` или ```http://localhost:8080/```. Кнопка ```Send``` должна стать активной.

## Особенности реализации
- Доступны **отправка и приём сообщений всем пользователям**, есть возможность отправить **direct message**: ```@имя_пользователя: текст_сообщения```. Соответствующие функции расположены в ```messenger.py```.
- Приходят сообщения о том, что **пользователь вошёл в чат/вышел из чата**. Для этого был написан класс оповещателя, который сигнализирует о входе/выходе (см. функции в ```annunciator.py```).

## Некоторые детали
- Отправленное пользователем сообщение **не** показывается дважды. Для этого при рассылке сообщений всем пользователям исключается ip отправителя. А direct message в формате ```[DM || имя_пользователя]: текст_сообщения``` появляется только у получателя, у отправителя же - стандартное сообщение от первого лица.
- Когда пользователь заходит в чат, появляются только приветственные слова, а сообщения о входе/выходе приходят от других пользователей.
