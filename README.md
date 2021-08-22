# Тестовое задание для ORBIS

Текст тестового задания:

> Есть база данных, содержащая таблицу “объектов”:
> - Объекты могут быть нескольких типов: "папка", "тип1", "тип2";
> - Каждый объект обязательно имеет не пустые поля `id` (число) и `name` (строка);
> - В рамках реализации задачи можно добавлять любое количество дополнительных полей;
> - Объект типа "папка" может содержать в себе (логически) другие объекты (посредством связи потомок-родитель);
> 
> Необходимо реализовать REST-сервис, принимающий запрос `GET` `/object/<id>/`;  
> Если `id`=0 или не задан - должны вывестись все объекты БД;  
> Если указанный объект имеет потомков - должны быть выведены все объекты-потомки указанного объекта, а также сам объект;  
> Реализовать обработку ошибок:
> - Если объекта не существует - должна вернуться ошибка `HTTP 404`;
> - Если `id` задан и не цифра - должна вернуться ошибка `HTTP 400`, с описанием проблемы;
> - Если при выполнении запроса возникла иная ошибка - `HTTP 500`;
> 
> Необязательные `GET`-параметры:
> - `filter=name` - фильтрация по имени объекта (нестрогое соответствие)
> - `format=json/xml` - формат выдаваемых данных (если не указан - `json`)
> Дополнительные задачи (будет плюсом):
> - Реализовать механизм прав доступа:
>     - аутентификация;
>     - отображение объектов согласно уровню прав доступа текущего пользователя;
> - Реализовать механизм кэширования ответов;
> - Реализовать локализацию объектов по имени. Добавить новый `GET`-параметр `lng`, в зависимости от значения которого выводить имя объекта на том или ином языке. Параметр также будет влиять на работу `filter`.