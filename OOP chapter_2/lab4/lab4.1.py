import sqlite3
import pandas as pd
import os
import re


# ЗАВДАННЯ 1: КЛАС ДЛЯ РОБОТИ З БАЗОЮ ДАНИХ ТА ПІДГОТОВКИ
class DatabaseManager:
    def __init__(self, db_name):
        # 1.2 Підключення до бази даних
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def load_csv_to_sql(self, csv_path, table_name):
        # 1.3 Завантаження CSV
        df = pd.read_csv(csv_path)

        # Попередня обробка: перетворюємо текстову зарплату в число для розрахунків
        # (Витягуємо перше число з рядка типу "£40,000 - £60,000")
        df['Salary_Numeric'] = df['Salary Range'].str.replace('£', '').str.replace(',', '').str.extract(
            r'(\d+)').astype(float)

        # 1.4 Завантаження в SQLite
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        print(f"Дані успішно завантажено в таблицю '{table_name}'")
        return df

    def execute_query(self, sql_query):
        # Виконання запиту через Pandas
        return pd.read_sql(sql_query, self.conn)

    def close_connection(self):
        # ЗАВДАННЯ 7: Закриття з'єднання
        self.conn.close()
        print("\nЗ'єднання з базою даних закрито.")


# ЗАВДАННЯ 2-6: КЛАС ДЛЯ АНАЛІТИКИ ТА ЗАПИТІВ
class JobAnalytics:
    def __init__(self, db_manager):
        self.db = db_manager

    def run_all_tasks(self):
        # ЗАВДАННЯ 2: Основні запити
        print("\n--- Завдання 2.1: Перші 10 вакансій ---")
        print(self.db.execute_query("SELECT * FROM jobs LIMIT 10"))

        print("\n--- Завдання 2.2: Вакансії, що вимагають SQL ---")
        print(self.db.execute_query("SELECT * FROM jobs WHERE \"Required Skills\" LIKE '%SQL%';"))

        print("\n--- Завдання 2.3: Унікальні локації та компанії ---")
        print(self.db.execute_query("SELECT DISTINCT Location, Company FROM jobs;"))

        # ЗАВДАННЯ 3-4: Агрегатні функції
        print("\n--- Завдання 3.1: Середня зарплата за рівнем досвіду ---")
        query_avg = "SELECT \"Experience Level\", AVG(Salary_Numeric) as Avg_Salary FROM jobs GROUP BY \"Experience Level\";"
        print(self.db.execute_query(query_avg))

        # Завдання 3.2
        print("\n ---Завдання 3.2: кількість вакансій для кожного рівня досвіду  ")
        query_count = """
        SELECT "Experience Level", COUNT(*) as Count 
        FROM jobs 
        GROUP BY "Experience Level";
        """
        print(self.db.execute_query(query_count))

        # Завдання 3.3
        print("\n ---Завдання 3.3 мінімальну та максимальну зарплату серед усіх вакансій.")
        query_max_salary = """
        SELECT "Job Title",
        MAX(Salary_Numeric) as Max_Salary,
        MIN(Salary_Numeric) as Min_Salary
        FROM jobs 
        GROUP BY "Job Title"
        ORDER BY MAX_Salary DESC;
        """
        print(self.db.execute_query(query_max_salary))



        print("\n--- Завдання 4.1: Кількість вакансій в індустріях із зарплатою > £50,000 ---")
        query_ind = "SELECT Industry, COUNT(*) as Count FROM jobs WHERE Salary_Numeric > 50000 GROUP BY Industry;"
        print(self.db.execute_query(query_ind))

        print("\n--- Завдання 4.2: середню зарплату для кожної індустрії.")
        query_salary = """
        SELECT "Job Title",
        AVG(Salary_Numeric) as Avg_Salary
        FROM jobs 
        GROUP BY "Job Title"
        ORDER BY Avg_Salary DESC;
        """
        print(self.db.execute_query(query_salary))



        # ЗАВДАННЯ 5: Складніші запити
        print("\n--- Завдання 5.1: Кількість вакансій за Location та Experience Level ---")
        query_complex = """
        SELECT Location, "Experience Level", COUNT(*) as Count 
        FROM jobs 
        GROUP BY Location, "Experience Level"
        ORDER BY Location;
        """
        print(self.db.execute_query(query_complex))

        print("\n --- Завдання 5.2:Загальну кількість вакансій у кожній індустрії  ")
        query_complex = """
        SELECT Industry, "Job Type", COUNT(*) as Count 
        FROM jobs 
        GROUP BY Industry, "Job Type"
        ORDER BY Industry;
        """
        print(self.db.execute_query(query_complex))
        
        print("\n --- Завдання 5.3: середню зарплату для вакансій за Location та Experience Level.")
        query_complex = """
        SELECT Location, "Experience Level", COUNT(*) as Count,
        AVG(Salary_Numeric) as Avg_Salary 
        FROM jobs 
        GROUP BY Location, "Experience Level"
        ORDER BY Location
        """
        print(self.db.execute_query(query_complex))

        
        # ЗАВДАННЯ 6*: Додаткові запити
        print("\n--- Завдання 6.1*: ТОП-5 вакансій з найвищою зарплатою ---")
        print(self.db.execute_query(
            "SELECT \"Job Title\", Company, Salary_Numeric FROM jobs ORDER BY Salary_Numeric DESC LIMIT 5;"))

# ОСНОВНИЙ БЛОК ЗАПУСКУ
if __name__ == "__main__":
    # Шлях до файлу (автоматичне визначення)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, 'Job opportunities.csv')

    if os.path.exists(csv_file):
        # Створюємо менеджера бази даних
        db_man = DatabaseManager('it_jobs_v2.db')

        # Завантажуємо дані
        db_man.load_csv_to_sql(csv_file, 'jobs')

        # Запускаємо аналітику
        analytics = JobAnalytics(db_man)
        analytics.run_all_tasks()

        # Закриваємо базу
        db_man.close_connection()
    else:
        print(f"Помилка: Файл {csv_file} не знайдено у папці зі скриптом!")