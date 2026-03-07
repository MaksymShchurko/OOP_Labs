import pandas as pd


# КЛАС 1: Завантаження та первинний огляд даних
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None

    def load_data(self):
        try:
            # Завантаження CSV файлу
            self.df = pd.read_csv(self.file_path)
            print(f"--- Файл '{self.file_path}' успішно завантажено ---")
            return self.df
        except FileNotFoundError:
            print("Помилка: Файл не знайдено. Перевірте шлях до файлу.")
            return None

    def show_info(self):
        if self.df is not None:
            print("\nПерші 5 рядків даних:")
            print(self.df.head())
            print(f"\nЗагальна кількість записів: {self.df.shape[0]}")
            print(f"Кількість стовпців: {self.df.shape[1]}")
        else:
            print("Дані не завантажені.")


# КЛАС 2: Фільтрація та сортування
class DataProcessor:
    @staticmethod
    def filter_by_experience(df, level):
        """Фільтрація за рівнем досвіду (наприклад, 'Senior', 'Junior')"""
        filtered_df = df[df['Experience Level'] == level]
        return filtered_df

    @staticmethod
    def sort_by_date(df):
        """Сортування за датою публікації (від нових до старих)"""
        # Копіюємо DataFrame, щоб не змінювати оригінал напряму
        temp_df = df.copy()
        # Перетворюємо текст у формат дати
        temp_df['Date Posted'] = pd.to_datetime(temp_df['Date Posted'])
        # Сортуємо
        return temp_df.sort_values(by='Date Posted', ascending=False)


# КЛАС 3: Аналітика та групування
class DataAnalytics:
    @staticmethod
    def analyze_yearly_activity(df):
        """Аналіз кількості вакансій за роками"""
        temp_df = df.copy()
        # Перетворюємо дату та витягуємо тільки рік
        temp_df['Date Posted'] = pd.to_datetime(temp_df['Date Posted'])
        temp_df['Year'] = temp_df['Date Posted'].dt.year

        # Групування за роком та підрахунок кількості через agg()
        yearly_report = temp_df.groupby('Year').agg({'Job Title': 'count'})

        # Перейменовуємо колонку для зручності
        yearly_report.columns = ['Vacancies Count']
        return yearly_report


# --- ОСНОВНА ЧАСТИНА ПРОГРАМИ (Execution) ---

if __name__ == "__main__":
    # 1. Створюємо об'єкт для завантаження
    loader = DataLoader('Job opportunities.csv')
    data = loader.load_data()

    if data is not None:
        # Виводимо базову інформацію
        loader.show_info()

        # 2. Фільтрація: виберемо вакансії тільки рівня 'Senior'
        print("\n--- Фільтрація: Вакансії рівня 'Senior' ---")
        senior_jobs = DataProcessor.filter_by_experience(data, 'Senior')
        print(senior_jobs[['Job Title', 'Company', 'Experience Level']].head())

        # 3. Сортування: за датою публікації
        print("\n--- Сортування за датою (останні вакансії) ---")
        sorted_jobs = DataProcessor.sort_by_date(data)
        print(sorted_jobs[['Job Title', 'Date Posted']].head())

        # 4. Аналітика: активність за роками
        print("\n--- Аналіз активності ринку за роками ---")
        analytics = DataAnalytics()
        report = analytics.analyze_yearly_activity(data)
        print(report)

        # Висновок про найбільш активний рік
        most_active_year = report['Vacancies Count'].idxmax()
        print(f"\nВисновок: Найбільш активним роком для пошуку роботи був {most_active_year}.")