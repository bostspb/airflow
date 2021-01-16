## Урок 1. Планирование задач. Введение Apache AirFlow

1. Какой из флагов утилиты crontab покажет список существующих кронов?<br>
**Ответ:** для текущего пользователя - `crontab -l`, а для определенного пользователя - `crontab -u username -l`

2. Напишите крон, который будет запускаться каждую пятницу в 9 часов вечера.<br>
**Ответ:** `0 21 * * 5`

3. Напишите крон, который будет запускаться каждое воскресенье марта месяца 
на протяжении всего дня с интервалом в 4 часа 
(т.е. запуск будет в 2021-03-07 00:00:00, затем 2021-03-07 04:00:00 и т.д.)<br>
**Ответ:** `0 */4 * 3 0`

4. Отметьте [все картинки](https://prnt.sc/wsjfr3), где изображен направленный ациклический граф.<br>
**Ответ:** 1 - направленный ациклический граф, 2 - нет направлений у связей, 
3 - не у всех связей есть направление, 4 - есть циклы в связях 

5. Опишите своими словами, как Вы поняли, чем отличается `task` от `operator`?<br>
**Ответ:** `task` более широкое понятие, при помощи которого решается определенная задача - например, 
специально написанный скрипт под определенную задачу.
А `operator` больше похож на какой-то готовый инструмент для использования в процессе решения однотипных задач - 
например, как модуль или пакет в языке программирования. 