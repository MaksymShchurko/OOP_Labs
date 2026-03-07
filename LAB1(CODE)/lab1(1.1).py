class CallReport:
    def generate_report(self, call_data):
        return f"Звіт по дзвінку: {call_data} "

class ReportSaver:
    def save_to_file(self, report_content, filename):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report_content)
            print(f"Звіт успішно    збереженно у файл: {filename}")


reporter = CallReport()
saver = ReportSaver()

my_report = reporter.generate_report("Абонент +380685377518, тривалість 5 хв")

saver.save_to_file(my_report, "report.txt")