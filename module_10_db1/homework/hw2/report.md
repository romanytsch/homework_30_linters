# Отчет по анализу продаж телефонов по цвету (hw_2_database.db)

### 1. Телефоны какого цвета чаще всего покупают?
SELECT p.colour, COUNT(*) as purchases_count
FROM main.table_checkout c
JOIN main.table_phones p ON c.phone_id = p.id
GROUP BY p.colour
ORDER BY purchases_count DESC
LIMIT 1;

### 2. Какие телефоны чаще покупают: красные или синие?
SELECT p.colour, COUNT(*) as purchases_count
FROM main.table_checkout c
JOIN main.table_phones p ON c.phone_id = p.id
WHERE p.colour IN ('red', 'blue', 'красный', 'синий')
GROUP BY p.colour
ORDER BY purchases_count DESC;

### 3. Какой самый непопулярный цвет телефона?
SELECT p.colour, COUNT(*) as purchases_count
FROM main.table_checkout c
JOIN main.table_phones p ON c.phone_id = p.id
GROUP BY p.colour
ORDER BY purchases_count ASC
LIMIT 1;


**Инструкция:** Выполните запросы в PyCharm (ПКМ на БД → Query Console)