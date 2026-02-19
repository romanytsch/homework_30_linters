## Типы связей между таблицами в схеме

![](../img/cinema_schema_diagram.png)

| Тип связи | Таблица 1 | Таблица 2 |
|:---------:|-----------|-----------|
|           |           |           |

Тип связи      | Таблица 1            | Таблица 2         
---------------|----------------------|-------------------
One-to-Many    | director             | movie_direction   
One-to-Many    | movie                | movie_direction   
One-to-Many    | actors               | movie_cast        
One-to-Many    | movie                | movie_cast        
One-to-One     | movie                | oscar_awarded     
