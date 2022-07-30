# Super_resolution_with_SRGan_mdrbot

Захосчен на heroku  
Для локального запуска:  
1. В директории tg_bot создать файл .env, в котором прописать апи-токен бота (см. .env.template)  
2. Ввести следующие команды в корневой директории:  
```
pip install -r requirements.txt
py main.py
```

# Общая информация:
Бот предоставляет возможность воспользоваться моделями для super-resolution  
На данный момент:
1. SRGan https://github.com/Lornatang/SRGAN-PyTorch
2. SwinIR https://github.com/JingyunLiang/SwinIR

Скрины использования:  
https://docs.google.com/document/d/1OC7KRV1TnzaV9t8m_3wLhIT1OLtUvFE8t3jWH0I1MWk/edit?usp=sharing

# Документация:  
При запуске бота запускаются два потока (для каждой модели соответственно, см. tg_bot/model_loops.py), которые периодически проверяют выделенные им директории на появление картинки для обработки. При обнаружении картинки, она обрабатывается той или иной моделью и удаляется из исходного директория, результат сохраняется в другом, общем для всех моделей директории.

Работа бота реализована через машину состояний (см. tg_bot/bot.py):  
1. /start -> вывод клавиатуры с вариантами моделей, ожидание выбора
2. /sr_gan(или другая модель из списка) -> вывод сообщения об ожидании фото, ожидание фото для обработки
3. *прислано фото* -> сохранение фото в директорию соответствующую выбранной модели, вывод сообщения с просьбой подождать окончания работы алгоритма ожидание конца работы модели
4. *в директории с обработанными картинками появилась картинка для данного пользователя* -> отправка результата работы с небольшим текстовым сообщением, вывод клавиатуры '/start' для повтора сценария работы, выход из машины состояний
