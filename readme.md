Мухаметов Ильнур Фаваризович 11-909, 4 курс, ИТИС

Схема черновая, могут быть неточности, строилась для понимания
![image](https://user-images.githubusercontent.com/24254731/211376422-2b04499d-84f7-4222-b34a-5ecc08f1bec0.png)


Как запустить:

В конце должно выглядеть примерно так: 

![image](https://user-images.githubusercontent.com/24254731/211377099-a0af5112-42c3-4bb4-88f7-911fe4599fb0.png)



1)Что нужно для определения лиц на фото

	a) Создать бакет itis-2022-2023-vvot04-photos
	
	b) Поместить код из папки finder в функцию. В моём случае vvot04-face-detection
	
	c) Создать триггер vvot04-photo-trigger, связать с функцией из (b). Настроить так, чтобы триггер активировался
		при загрузке .jpg
		
		
2)Что нужно для обработки лиц

	a) Создать бакет itis-2022-2023-vvot04-faces
	
	b) Создать очередь vvot04-tasks
	
	c) Создать Serverless Containers контейнер vvot04-face-cut
	
	d) Создание реестра: Создать образ config.py из папки cutter. Запушить с помощью docker push
	
	e) Связываем vvot04-face-cut с образом
	
	f) Создаём триггер vvot04-task-trigger с типом Message Queue и связываем с vvot04-tasks
	
	g) Создать DB vvot04-db-photo-face и создать таблицу на основе скрипта script.txt
	
	
3)Gateway

	a) Создать API GATEWAY на основе gateway.txt
	
4)Что нужно для работы ТГ бота

	a) Создать публичную функцию на основе main/index.py
	
	b) Получить токен бота ТГ
	
	c) Зарегистрировать функцию как вебхуку для вашего бота

Мой бот: https://t.me/ilnur_vvot04_bot
Команды для бота: /getface, /find

![image](https://user-images.githubusercontent.com/24254731/211376104-fdc6e913-3dcf-4d14-97d5-eee1bbb9e1bd.png)

