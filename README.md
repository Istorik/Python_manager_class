# Python_manager_class

Язык Python 3

Библиотеки threading, time, tkinter, subprocess, colored

Данный скрипт позволяет управлять несколькими компьтерами (компьютер ученика) с одно (компьютер учителя) по с помощью ssh протокола.
Данный скрипт не рекомендуется для использования на продакшен серверах в силу своей не секьюрности.
Делаю на ubuntu и для ubuntu
Незабудь везде заменить Istorik на своего пользователя.

1. Генерируем себе ssh ключ на компьютере учителя
>ssh-keygen -t rsa
2. Копируем этот ключ на каждый компьютер ученика
> ssh-copy-id istorik@192.168.10.51
> ssh-copy-id istorik@192.168.10.52
 ...
> ssh-copy-id istorik@192.168.10.60

3. В скрипте редактируем ip в списке ip_list_all

4. На компьютере ученика позволяем выполнения команд sudo без ввода пароля из учетной записис учителя.
> sudo visudo

в конец дописать

> istorik ALL=(ALL) NOPASSWD:ALL
