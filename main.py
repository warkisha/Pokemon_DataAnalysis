import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
from scipy import stats

# Основная функция для выполнения всех заданий
def main(file_path):
    df = load_data(file_path)
    print("DataFrame загружен успешно")

    conn = create_connection()
    save_to_db(df, conn)
    print("Данные успешно сохранены в базу данных")

    # Вопрос 2.1
    print("\n\tВопрос 2.1")

    double_type_percentage_value = double_type_percentage(df, conn)
    print(f'{double_type_percentage_value:.2f}% покемонов имеют двойной тип')

    # Вопрос 2.2
    print("\n\tВопрос 2.2")

    all_types = all_pokemon_types(conn)
    print(f'Всего типов покемонов: {len(all_types)}')
    print(f'Типы покемонов: {all_types}')

    # Вопрос 2.3
    print("\n\tВопрос 2.3")

    single_type_total, double_type_total = average_total_single_double(df)
    print(f'Средний показатель Total у покемонов одинарного типа: {single_type_total}')
    print(f'Средний показатель Total у покемонов двойного типа: {double_type_total}')

    # Вопрос 2.4
    print("\n\tВопрос 2.4")

    grass_defense, fairy_defense = average_defense_grass_fairy(df)
    print(f'Средний показатель Defense у покемонов типа Grass: {grass_defense}')
    print(f'Средний показатель Defense у покемонов типа Fairy: {fairy_defense}')

    # Вопрос 2.5
    print("\n\tВопрос 2.5")

    legendary_mean_total, non_legendary_mean_total = average_total_legendary_non_legendary(df)
    print(f'Средний показатель Total у легендарных покемонов: {legendary_mean_total}')
    print(f'Средний показатель Total у нелегендарных покемонов: {non_legendary_mean_total}')

    # Вопрос 2.6
    print("\n\tВопрос 2.6")

    df_legendary_vs_nonlegendary = legendary_vs_nonlegendary(conn)
    print(f'Количество таких случаев: {len(df_legendary_vs_nonlegendary)}')
    print(df_legendary_vs_nonlegendary)

    # Вопрос 2.7
    print("\n\tВопрос 2.7")

    mean_diff, median_diff, mode_diff, differences = total_difference_stats(df_legendary_vs_nonlegendary)
    print(f'Среднее арифметическое: {mean_diff}')
    print(f'Медиана: {median_diff}')
    print(f"Мода: {mode_diff}")
    plot_histogram(differences)  # Вызов функции для построения гистограммы

    # Вопрос 2.8
    print("\n\tВопрос 2.8")

    least_corr = least_correlated_features(df)
    print("Наименьшая корреляция между числовыми характеристиками:")
    print(least_corr)

    # Вопрос 2.9
    print("\n\tВопрос 2.9")

    correlation_analysis_and_visualization(df)

# Вопрос 2.1: Процент покемонов с двойным типом
def double_type_percentage(df, conn):
    query = 'SELECT COUNT(*) AS count FROM pokemon WHERE `Type 2` IS NOT NULL'
    double_type_count = execute_query(query, conn)['count'][0]
    total_pokemon_count = len(df)
    return (double_type_count / total_pokemon_count) * 100

# Вопрос 2.2: Все типы покемонов
def all_pokemon_types(conn):
   query = '''SELECT DISTINCT `Type 1` AS Types FROM pokemon 
   UNION 
   SELECT DISTINCT `Type 2`  FROM pokemon 
   WHERE `Type 2` IS NOT NULL;'''
   types = execute_query(query, conn)['Types'].tolist()
   return types

# Вопрос 2.3: Средний показатель Total у покемонов одинарного и двойного типа
def average_total_single_double(df):
    single_type_total = df[df['Type 2'].isna()]['Total'].mean() 
    double_type_total = df[~df['Type 2'].isna()]['Total'].mean()
    return single_type_total, double_type_total

# Вопрос 2.4: Средний показатель Defense у покемонов типа Grass и Fairy
def average_defense_grass_fairy(df):
    grass_defense = df[(df['Type 1'] == 'Grass') | (df['Type 2'] == 'Grass')]['Defense'].mean()
    fairy_defense = df[(df['Type 1'] == 'Fairy') | (df['Type 2'] == 'Fairy')]['Defense'].mean()
    return grass_defense, fairy_defense

# Вопрос 2.5: Средний показатель Total у легендарных и нелегендарных покемонов
def average_total_legendary_non_legendary(df):
    legendary_mean_total = df[df['Legendary']]['Total'].mean()
    non_legendary_mean_total = df[~df['Legendary']]['Total'].mean()
    return legendary_mean_total, non_legendary_mean_total

# Вопрос 2.6: Легендарные покемоны с Total меньше, чем у нелегендарных 
def legendary_vs_nonlegendary(conn):
    query = '''
    SELECT l.Name AS LegendaryPokemon, 
    l.Total AS LegendaryTotal, 
    n.Name AS NonLegendaryPokemon, 
    n.Total AS NonLegendaryTotal, 
    n.Total - l.Total AS Difference
    FROM pokemon l
    JOIN pokemon n ON l.Total < n.Total
    WHERE l.Legendary = 1 AND n.Legendary = 0
    '''
    result_df = execute_query(query, conn)
    
    # Сохранение в CSV файл
    result_df.to_csv('legendary_vs_nonlegendary_comparisons.csv', index=False)
    
    return result_df

# Вопрос 2.7: Разница Total между легендарными и нелегендарными покемонами
def total_difference_stats(df_legendary_vs_nonlegendary):
    differences =  df_legendary_vs_nonlegendary['NonLegendaryTotal'] - df_legendary_vs_nonlegendary['LegendaryTotal']
    mean_diff = differences.mean()
    median_diff = differences.median()
    mode_result = stats.mode(differences)
    mode_diff = mode_result.mode[0] if hasattr(mode_result.mode, '__len__') and len(mode_result.mode) > 0 else "Нет моды"
    return mean_diff, median_diff, mode_diff, differences

def plot_histogram(differences):
    plt.hist(differences, bins=10, edgecolor='black')
    plt.title('Гистограмма разницы Total между легендарными и нелегендарными покемонами')
    plt.xlabel('Разница Total')
    plt.ylabel('Частота')
    plt.show()

# Вопрос 2.8: Наименьшая корреляция между числовыми характеристиками
def least_correlated_features(df):
    numeric_features = ['Total', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Generation']
    correlations = df[numeric_features].corr()
    min_corr = correlations.unstack().sort_values().drop_duplicates()
    least_corr = min_corr.head(1)
    return least_corr

# Вопрос 2.9: Логистическая регрессия
def correlation_analysis_and_visualization(df):
    df['Legendary'] = df['Legendary'].astype(int)
    correlation_matrix = df[['Legendary', 'HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed', 'Total']].corr()

    # Отображение корреляционной матрицы
    print(correlation_matrix)

    # Визуализация корреляционной матрицы
    plt.figure(figsize=(8, 5))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
    plt.title('Корреляционная матрица характеристик покемонов')
    plt.show()

    # Визуализация корреляции характеристик с легендарностью
    correlation_with_legendary = correlation_matrix['Legendary'].drop('Legendary')
    plt.figure(figsize=(8, 5))
    correlation_with_legendary.sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.title('Корреляция характеристик с легендарностью покемона')
    plt.ylabel('Коэффициент корреляции')
    plt.show()

# Функция для загрузки данных из файла CSV
def load_data(file_path):
    return pd.read_csv(file_path)

# Функция для создания и подключения к базе данных SQLite
def create_connection(db_name='pokemon.db'):
    return sqlite3.connect(db_name)

# Функция для сохранения данных в таблицу базы данных
def save_to_db(df, conn, table_name='pokemon'):
    df.to_sql(table_name, conn, if_exists='replace', index=False)

# Функция для выполнения SQL запросов
def execute_query(query, conn):
    with conn:
        result = conn.execute(query).fetchall()
    return pd.DataFrame(result, columns=[desc[0] for desc in conn.execute(query).description])


# Запуск основной функции
if __name__ == "__main__":
    main('Pokemon.csv')
