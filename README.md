
# Документация по коду python для анализа данных о покемонах

## Описание
- Этот скрипт выполняет несколько задач по анализу данных о покемонах. Он включает загрузку данных из CSV-файла, сохранение данных в базу данных SQLite, выполнение различных запросов и вычислений, а также визуализацию данных между характеристиками покемонов.

### Установка зависимостей

``` bash
pip install pandas matplotlib seaborn sqlite3 scipy
```

## Структура кода

### Основная функция для выполнения всех заданий
#### Назначение 
- Основная функция, которая загружает данные из CSV файла, сохраняет их в базу данных, а затем выполняет серию аналитических задач и визуализаций, представленных в различных подфункциях.
#### Аргументы
- file_path (str): Путь к файлу CSV, содержащему данные о покемонах.
#### Описание:
1. Загружает данные из указанного файла CSV в DataFrame.
2. Создает подключение к базе данных SQLite.
3. Сохраняет данные DataFrame в базу данных.
4. Выполняет серию заданий по анализу данных:
       - Вопрос 2.1: Процент покемонов с двойным типом.
       - Вопрос 2.2: Все типы покемонов.
       - Вопрос 2.3: Средний показатель Total для покемонов одинарного и двойного типа.
       - Вопрос 2.4: Средний показатель Defense у покемонов типа Grass и Fairy.
       - Вопрос 2.5: Средний показатель Total у легендарных и нелегендарных покемонов.
       - Вопрос 2.6: Сравнение Total между легендарными и нелегендарными покемонами.
       - Вопрос 2.7: Статистика разницы Total между легендарными и нелегендарными покемонами.
       - Вопрос 2.8: Наименьшая корреляция между числовыми характеристиками.
       - Вопрос 2.9: Корреляционный анализ и визуализация.



### Функция double_type_percentage
#### Назначение
- Функция double_type_percentage предназначена для вычисления процента покемонов, имеющих двойной тип.
#### Аргументы
- df (pandas.DataFrame): DataFrame, содержащий данные о покемонах;
- conn (sqlite3.Connection): Соединение с базой данных SQLite, в которой хранятся данные о покемонах.

#### Возвращаемое значение
- Возвращает процент покемонов с двойным типом в виде числа с плавающей точкой (float).

#### Описание
1. Определение SQL-запроса:
``` python
query = 'SELECT COUNT(*) AS count FROM pokemon WHERE `Type 2` IS NOT NULL'
```
SQL-запрос выбирает количество записей в таблице pokemon, у которых столбец Type 2 не является NULL, покемонов у которых есть второй тип.

2. Выполнение SQL-запроса:
``` python
double_type_count = execute_query(query, conn)['count'][0]
```
Используя функцию execute_query, выполняется SQL-запрос. Результат запроса возвращается в виде DataFrame. В данной строке извлекается количество покемонов с двойным типом из первого элемента столбца count.

3. Вычисление общего количества покемонов:
``` python
total_pokemon_count = len(df)
```
Определяется общее количество покемонов в DataFrame df с помощью функции len.

4. Вычисление процента покемонов с двойным типом:
``` python
return (double_type_count / total_pokemon_count) * 100
```
Процент покемонов с двойным типом вычисляется как отношение количества покемонов с двойным типом к общему количеству покемонов, умноженное на 100.
### Функция all_pokemon_types
#### Назначение
Функция all_pokemon_types предназначена для получения всех уникальных типов покемонов из базы данных.
#### Аргументы
conn (sqlite3.Connection): Соединение с базой данных SQLite, в которой хранятся данные о покемонах.
#### Возвращаемое значение
Возвращает список (list) всех уникальных типов покемонов.
#### Описание
1. Определение SQL-запроса:
``` python
query = '''SELECT DISTINCT `Type 1` AS Types FROM pokemon 
UNION 
SELECT DISTINCT `Type 2`  FROM pokemon 
WHERE `Type 2` IS NOT NULL;'''
```
SQL-запрос выбирает все уникальные значения из столбца Type 1 и объединяет их с уникальными значениями из столбца Type 2 (при условии, что Type 2 не равен NULL). Этот запрос позволяет получить все уникальные типы покемонов, вне зависимости от того, являются ли они основным (Type 1) или вторичным (Type 2) типом.

2. Выполнение SQL-запроса:
``` python
types = execute_query(query, conn)['Types'].tolist()
```
Используя функцию execute_query, выполняется SQL-запрос. Результат запроса возвращается в виде DataFrame. В данной строке извлекаются все уникальные типы покемонов из столбца Types и преобразуются в список.

3. Возвращение списка типов покемонов:
``` python
return types
```
Список всех уникальных типов покемонов возвращается в качестве результата функции.

### Функция average_total_single_double
#### Назначение
- Функция average_total_single_double вычисляет среднее значение показателя Total для покемонов с одинарным и двойным типами.
#### Аргументы
- df (pandas.DataFrame): DataFrame, содержащий данные о покемонах.
#### Возвращаемые значения
- single_type_total (float): Среднее значение показателя Total для покемонов с одинарным типом;
- double_type_total (float): Среднее значение показателя Total для покемонов с двойным типом.
#### Описание
1. Фильтрация покемонов с одинарным типом:
``` python 
single_type_total = df[df['Type 2'].isna()]['Total'].mean()
```
- df['Type 2'].isna(): Выбирает строки, где столбец Type 2 имеет значение NaN (отсутствует второй тип);
- df[df['Type 2'].isna()]['Total']: Выбирает столбец Total для строк с одинарным типом;
- .mean(): Вычисляет среднее значение для этих строк.
2. Фильтрация покемонов с двойным типом:
``` python
double_type_total = df[~df['Type 2'].isna()]['Total'].mean()
```
    - ~df['Type 2'].isna(): Выбирает строки, где столбец Type 2 не имеет значение NaN (присутствует второй тип);
    - df[~df['Type 2'].isna()]['Total']: Выбирает столбец Total для строк с двойным типом;
    - .mean(): Вычисляет среднее значение для этих строк.
3. Возврат результатов:
``` python
return single_type_total, double_type_total
```
Функция возвращает два значения: среднее значение показателя Total для покемонов с одинарным типом и среднее значение показателя Total для покемонов с двойным типом.
### Функция average_defense_grass_fairy
#### Назначение
- Функция average_defense_grass_fairy вычисляет среднее значение показателя Defense для покемонов типов Grass и Fairy.
#### Аргументы
- df (pandas.DataFrame): DataFrame, содержащий данные о покемонах. Ожидается, что в DataFrame есть столбцы Type 1, Type 2 и Defense.
#### Возвращаемые значения
- grass_defense (float): Среднее значение показателя Defense для покемонов типа Grass.
- fairy_defense (float): Среднее значение показателя Defense для покемонов типа Fairy.
#### Описание 
1. Фильтрация покемонов типа Grass:
``` python
grass_defense = df[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Grass')]['Defense'].mean()
```
- df[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Grass')]: Выбирает строки, где столбец Type 1 или Type 2 имеет значение Grass.
- df[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Grass')]['Defense']: Выбирает столбец Defense для строк с типом Grass.
- .mean(): Вычисляет среднее значение для этих строк.
2. Фильтрация покемонов типа Fairy:
``` python
fairy_defense = df[(df['Type 1'] == 'Fairy') | (df['Type 2'] == 'Fairy')]['Defense'].mean()
```
- df[(df['Type 1'] == 'Fairy') | (df['Type 2'] == 'Fairy')]: Выбирает строки, где столбец Type 1 или Type 2 имеет значение Fairy.
- df[(df['Type 1'] == 'Fairy') | (df['Type 2'] == 'Fairy')]['Defense']: Выбирает столбец Defense для строк с типом Fairy.
- .mean(): Вычисляет среднее значение для этих строк.
3. Возврат результатов:
``` python
return grass_defense, fairy_defense
```
Функция возвращает два значения: среднее значение показателя Defense для покемонов типа Grass и среднее значение показателя Defense для покемонов типа Fairy.

### Функция average_total_legendary_non_legendary
#### Назначение
- Функция average_total_legendary_non_legendary вычисляет среднее значение показателя Total для легендарных и нелегендарных покемонов.
#### Аргументы
- df (pandas.DataFrame): DataFrame, содержащий данные о покемонах. Ожидается, что в DataFrame есть столбцы Legendary и Total.
#### Возвращаемые значения 
- legendary_mean_total (float): Среднее значение показателя Total для легендарных покемонов.
- non_legendary_mean_total (float): Среднее значение показателя Total для нелегендарных покемонов.
#### Описание 
1. Вычисление среднего значения показателя Total для легендарных покемонов:
```  python
legendary_mean_total = df[df['Legendary']]['Total'].mean()
```
- df[df['Legendary']]: Выбирает строки, где столбец Legendary имеет значение True.
- df[df['Legendary']]['Total']: Выбирает столбец Total для этих строк.
- .mean(): Вычисляет среднее значение для этих строк.
2. Вычисление среднего значения показателя Total для нелегендарных покемонов:
``` python
non_legendary_mean_total = df[~df['Legendary']]['Total'].mean()
```
- df[~df['Legendary']]: Выбирает строки, где столбец Legendary имеет значение False.
- df[~df['Legendary']]['Total']: Выбирает столбец Total для этих строк.
- .mean(): Вычисляет среднее значение для этих строк.
3. Возврат результатов:
``` python
return legendary_mean_total, non_legendary_mean_total
```
- Функция возвращает два значения: среднее значение показателя Total для легендарных покемонов и среднее значение показателя Total для нелегендарных покемонов.

### Функция legendary_vs_nonlegendary
#### Назначение
- Функция legendary_vs_nonlegendary выполняет SQL-запрос для получения списка пар легендарных и нелегендарных покемонов, у которых показатель Total у нелегендарного покемона больше, чем у легендарного. Результаты сохраняются в CSV файл и возвращаются в виде DataFrame.
#### Аргументы
- conn (sqlite3.Connection): Подключение к базе данных SQLite, содержащей таблицу pokemon.
#### Возвращаемые значения
- result_df (pandas.DataFrame): DataFrame, содержащий результат запроса. Включает пары легендарных и нелегендарных покемонов, у которых показатель Total у нелегендарного покемона больше, чем у легендарного.
#### Описание 
1. Определение SQL-запроса:
``` python
query = ''' SELECT l.Name AS LegendaryPokemon, 
l.Total AS LegendaryTotal, 
n.Name AS NonLegendaryPokemon, 
n.Total AS NonLegendaryTotal, 
n.Total - l.Total AS Difference
FROM pokemon l
JOIN pokemon n ON l.Total < n.Total
WHERE l.Legendary = 1 AND n.Legendary = 0 '''
```
- SELECT l.Name AS LegendaryPokemon, l.Total AS LegendaryTotal, n.Name AS NonLegendaryPokemon, n.Total AS NonLegendaryTotal, n.Total - l.Total AS Difference: Выбирает имя и показатель Total для легендарных и нелегендарных покемонов, а также разницу в показателях Total.
- FROM pokemon l JOIN pokemon n ON l.Total < n.Total: Объединяет таблицу pokemon саму с собой, выбирая пары, где показатель Total у нелегендарного покемона больше, чем у легендарного.
- WHERE l.Legendary = 1 AND n.Legendary = 0: Фильтрует только те пары, где l — легендарный покемон, а n — нелегендарный.
2. Выполнение SQL-запроса: 
``` python
result_df = execute_query(query, conn)
```
- Выполняет SQL-запрос с использованием подключения к базе данных и возвращает результат в виде DataFrame.
3. Сохранение результата в CSV файл:
``` python
result_df.to_csv('legendary_vs_nonlegendary_comparisons.csv', index=False)
``` 
- result_df.to_csv('legendary_vs_nonlegendary_comparisons.csv', index=False): Сохраняет DataFrame в CSV файл без записи индексов.
4. Возврат результата:
``` python
return result_df
```
- Функция возвращает DataFrame, содержащий результат SQL-запроса.

### Функция total_difference_stats
#### Назначение 
- Функция total_difference_stats вычисляет статистические показатели разницы в показателях Total между легендарными и нелегендарными покемонами. Возвращает среднее, медиану, моду и сами разницы показателей Total.
#### Аргументы
- df_legendary_vs_nonlegendary (pandas.DataFrame): DataFrame, содержащий данные о парах легендарных и нелегендарных покемонов, включая их показатели Total.
#### Возвращаемые значения
- mean_diff (float): Среднее значение разницы в показателях Total между легендарными и нелегендарными покемонам;
- median_diff (float): Медианное значение разницы в показателях Total между легендарными и нелегендарными покемонами;
- mode_diff (float или str): Модальное значение разницы в показателях Total между легендарными и нелегендарными покемонами. Если мода отсутствует, возвращает строку "Нет моды";
- differences (pandas.Series): Серия, содержащая разницу в показателях Total между легендарными и нелегендарными покемонами.
#### Описание 
1. Вычисление разницы в показателях Total:
``` python
differences = df_legendary_vs_nonlegendary['NonLegendaryTotal'] - df_legendary_vs_nonlegendary['LegendaryTotal']
```
- Высчитывает разницу между показателями Total нелегендарных и легендарных покемонов.
2. Вычисление среднего значения разницы:
``` python
mean_diff = differences.mean()
``` 
- Высчитывает Среднее значение разницы в показателях Total.
3. Вычисление медианного значения разницы:
``` python
median_diff = differences.median()
```
- Высчитывает медианное значение разницы в показателях Total
4. Вычисление модального значения разницы:
``` python
mode_result = stats.mode(differences)
mode_diff = mode_result.mode[0] if hasattr(mode_result.mode, '__len__') and len(mode_result.mode) > 0 else "Нет моды"
```
- mode_result: Результат функции stats.mode, возвращающий объект, содержащий моду.
- mode_diff: Если мода существует, берется первое значение из mode_result.mode; если нет, возвращается строка "Нет моды".
5. Возврат результатов: 
``` python
return mean_diff, median_diff, mode_diff, differences
```

### Функция plot_histogram
#### Назначение 
- Функция plot_histogram создает и отображает гистограмму для визуализации распределения разницы показателей Total между легендарными и нелегендарными покемонами.
#### Аргументы
- differences (pandas.Series): Серия, содержащая разницы в показателях Total между легендарными и нелегендарными покемонами.
#### Возвращаемые значения
- Функция ничего не возвращает. Она отображает гистограмму.
#### Описание 
1. Создание гистограммы:
``` python
plt.hist(differences, bins=10, edgecolor='black')
```
- plt.hist: Функция из библиотеки Matplotlib для построения гистограммы.
- differences: Серия данных, которую необходимо визуализировать.
- bins=10: Определяет количество бинов (интервалов) для гистограммы.
- edgecolor='black': Устанавливает черный цвет для границ каждого бина, чтобы визуально отделить их друг от друга.
2. Добавление заголовка к гистограмме:
``` python
plt.title('Гистограмма разницы Total между легендарными и нелегендарными покемонами')
```
- plt.title: Функция для добавления заголовка к графику.
3. Установка меток по оси X и Y
``` python
plt.xlabel('Разница Total')
plt.ylabel('Частота')
```
- plt.xlabel: Функция для добавления метки к оси X.
- 'Разница Total': Текст метки оси X.
- plt.ylabel: Функция для добавления метки к оси Y.
- 'Частота': Текст метки оси Y.
4. Отображение графика:
```  python
plt.show()
```

### Функция least_correlated_features
#### Назначение 
- Функция least_correlated_features вычисляет корреляции между различными числовыми характеристиками покемонов и возвращает пару характеристик с наименьшей корреляцией.
#### Аргументы
- df (pandas.DataFrame): DataFrame, содержащий данные о покемонах, включая их числовые характеристики.
#### Возвращаемые значения
- least_corr (pandas.Series) Пара характеристик и их значения корреляции с наименьшей корреляцией.
#### Описание 
1. Определение списка числовых характеристик:
``` python
numeric_features = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']
```
- numeric_features: Список числовых характеристик покемонов, которые будут использоваться для вычисления корреляций.
2. Вычисление корреляционной матрицы:
``` python
correlations = df[numeric_features].corr()
```
- df[numeric_features]: DataFrame, содержащий только столбцы с числовыми характеристиками.
- .corr(): Метод для вычисления корреляционной матрицы, где каждая ячейка показывает коэффициент корреляции Пирсона между двумя характеристиками.
3. Преобразование корреляционной матрицы в Series и сортировка значений:
``` python
min_corr = correlations.unstack().sort_values().drop_duplicates()
```
- min_corr = correlations.unstack().sort_values().drop_duplicates()
- correlations.unstack(): Преобразует DataFrame в Series, где индекс представляет пару характеристик, а значения - коэффициенты корреляции.
- sort_values(): Сортирует Series по значениям корреляции в порядке возрастания.
- drop_duplicates(): Убирает дублирующиеся значения, оставляя только уникальные пары характерист
4. Извлечение пары характеристик с наименьшей корреляцией:
``` python
least_corr = min_corr.head(2)
```
- min_corr.head(2): Извлекает первые две пары характеристик с наименьшими значениями корреляции.
5. Возврат результата:
``` python
return least_corr
```

### Функция correlation_analysis_and_visualization
#### Назначение 
- Функция correlation_analysis_and_visualization выполняет корреляционный анализ между характеристиками покемонов и визуализирует полученные данные. В частности, она исследует корреляцию различных характеристик с параметром "Legendary" (легендарность).
#### Аргументы
- df (pandas.DataFrame): DataFrame, содержащий данные о покемонах, включая их числовые характеристики и информацию о легендарности.
#### Возвращаемые значения
- Функция ничего не возвращает, но отображает графики.
#### Описание 
1. Преобразование столбца Legendary в числовой формат:
``` python
df['Legendary'] = df['Legendary'].astype(int)
```
- astype(int): Преобразует булевы значения в целочисленные (0 и 1), что необходимо для расчета корреляции.
2. Вычисление корреляционной матрицы для выбранных характеристик:
``` python
correlation_matrix = df[['Legendary', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']].corr()
```
- corr(): Метод для вычисления корреляционной матрицы, где каждая ячейка показывает коэффициент корреляции Пирсона между двумя характеристиками.
3. Отображение корреляционной матрицы:
``` python
print(correlation_matrix)
```
- print(correlation_matrix): Выводит на экран вычисленную корреляционную матрицу.
4. Визуализация корреляционной матрицы с помощью тепловой карты:
    ``` python
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Корреляционная матрица характеристик покемонов')
    plt.show()
    ```
    - plt.figure(figsize=(10, 8)): Устанавливает размер фигуры для графика.
    - sns.heatmap(...): Создает тепловую карту на основе корреляционной матрицы.
    - annot=True: Отображает числовые значения корреляций внутри ячеек тепловой карты.
    - cmap='coolwarm': Устанавливает цветовую палитру.
    - center=0: Центрирует цветовую шкалу на нуле.
    - plt.title(...): Устанавливает заголовок для графика.
    - plt.show(): Отображает график.
5. Вычисление и визуализация корреляции характеристик с легендарностью:
``` python
correlation_with_legendary = correlation_matrix['Legendary'].drop('Legendary')
plt.figure(figsize=(10, 6))
correlation_with_legendary.sort_values(ascending=False).plot(kind='bar', color='skyblue')
plt.title('Корреляция характеристик с легендарностью покемона')
plt.ylabel('Коэффициент корреляции')
plt.show()
```
- correlation_with_legendary = correlation_matrix['Legendary'].drop('Legendary'): Извлекает столбец корреляций с параметром "Legendary", исключая сам параметр "Legendary".
- plt.figure(figsize=(10, 6)): Устанавливает размер фигуры для графика.
- correlation_with_legendary.sort_values(ascending=False).plot(kind='bar', color='skyblue'): Создает столбчатую диаграмму, сортируя значения корреляций в порядке убывания.
- plt.title(...): Устанавливает заголовок для графика.
- plt.ylabel('Коэффициент корреляции'): Устанавливает метку для оси Y.
- plt.show(): Отображает график.

### Вспомогательные функции для работы с данными и базой данных SQLite
#### Назначение 
- Эти функции обеспечивают базовую функциональность для работы с данными покемонов в формате CSV и взаимодействия с базой данных.
#### Функция load_data(file_path)
``` python
    def load_data(file_path):
    return pd.read_csv(file_path)
```
- Использует функцию read_csv из библиотеки pandas для чтения данных из указанного файла CSV и возвращает DataFrame.
- Аргументы file_path (str): Путь к файлу CSV.
- Возвращаемое значение df (pandas.DataFrame): DataFrame, содержащий загруженные данные.
#### Функция create_connection(db_name='pokemon.db')
``` python
def create_connection(db_name='pokemon.db'):
    return sqlite3.connect(db_name)
```
- sqlite3.connect(db_name): Использует функцию connect из библиотеки sqlite3 для создания подключения к указанной базе данных и возвращает объект подключения.
- Аргументы db_name (str, по умолчанию 'pokemon.db'): Имя файла базы данных SQLite.
- Возвращаемое значение conn (sqlite3.Connection): Объект подключения к базе данных SQLite.
#### Функция save_to_db(df, conn, table_name='pokemon')
``` python
def save_to_db(df, conn, table_name='pokemon'):
    df.to_sql(table_name, conn, if_exists='replace', index=False)

```
- Использует метод to_sql из библиотеки pandas для сохранения данных DataFrame в таблицу базы данных SQLite. Если таблица уже существует, она будет заменена. Индексы DataFrame не сохраняются.
- Аргументы:
    - df (pandas.DataFrame): DataFrame, содержащий данные для сохранения.
    - conn (sqlite3.Connection): Подключение к базе данных SQLite.
    - table_name (str, по умолчанию 'pokemon'): Имя таблицы для сохранения данных.
#### Функция execute_query(query, conn)
- Выполняет SQL запрос к базе данных и возвращает результат в виде DataFrame.
- Аргументы:
    - query (str): SQL запрос. 
    - conn (sqlite3.Connection): Подключение к базе данных SQLite.
- Возвращаемое значение result_df (pandas.DataFrame): DataFrame, содержащий результаты выполнения SQL запроса.
``` python
def execute_query(query, conn):
    with conn:
        result = conn.execute(query).fetchall()
    return pd.DataFrame(result, columns=[desc[0] for desc in conn.execute(query).description])
``` 
- with conn:: Открывает контекстный менеджер для безопасного выполнения SQL запросов.
- result = conn.execute(query).fetchall(): Выполняет SQL запрос и извлекает все результаты.
- pd.DataFrame(result, columns=[desc[0] for desc in conn.execute(query).description]): Создает DataFrame из результатов выполнения запроса, используя названия столбцов из описания запроса.
- 


### Импорт библиотек
``` python
import pandas as pd
```
**Используется для:**
- Загрузки данных из CSV файла в DataFrame;
- Манипуляции данными и выполнения различных операций с ними
- Сохранения данных в базу данных SQLite
- Выполнения SQL запросов и преобразования их результатов в DataFrame

``` python
import matplotlib.pyplot as plt
```
**Используется для:**
- Построения гистограммы
- Визуализации корреляционной матрицы и корреляции характеристик

``` python
import seaborn as sns
```
**Используется для:**
- Визуализации корреляционной матрицы с использованием тепловой карты 

``` python
import sqlite3
```
**Используется для:**
- Создания соединения с базой данных SQLite
- Сохранения данных в таблицу базы данных SQLite
- Выполнения SQL запросов к базе данных SQLite

``` python
from scipy import stats
```
**Используется для:**
- Вычисления моды


