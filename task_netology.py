import csv
import re
from collections import defaultdict

# Функция для нормализации ФИО
def normalize_name(name_parts):
    full_name = " ".join(name_parts[:3]).split()  # Объединяем и разделяем
    return full_name[0], full_name[1], full_name[2] if len(full_name) > 2 else ""

# Функция для нормализации телефона
def normalize_phone(phone):
    pattern = re.compile(r"\+?7?[\s\-\(]*(\d{3})[\s\-\)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})(?:\s*\(?доб\.\s*(\d+)\)?)?")
    match = pattern.search(phone)
    if match:
        phone_normalized = f"+7({match[1]}){match[2]}-{match[3]}-{match[4]}"
        if match[5]:
            phone_normalized += f" доб.{match[5]}"
        return phone_normalized
    return phone

# Функция для объединения дублей
def merge_contacts(contacts):
    contacts_dict = defaultdict(lambda: ["", "", "", "", "", "", ""])

    for contact in contacts:
        last_name, first_name, surname = normalize_name(contact[:3])
        key = (last_name, first_name)

        existing = contacts_dict[key]

        contacts_dict[key] = [
            last_name,
            first_name,
            surname if existing[2] == "" else existing[2],
            contact[3] if existing[3] == "" else existing[3],
            contact[4] if existing[4] == "" else existing[4],
            normalize_phone(contact[5]) if existing[5] == "" else existing[5],
            contact[6] if existing[6] == "" else existing[6],
        ]
    return list(contacts_dict.values())

# Чтение данных
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    header = next(rows)  # Заголовки
    contacts_list = list(rows)

# Обрабатываем контакты
cleaned_contacts = merge_contacts(contacts_list)

# Записываем результат
with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
    datawriter = csv.writer(f, delimiter=",")
    datawriter.writerow(header)  # Заголовки
    datawriter.writerows(cleaned_contacts)

print("Файл phonebook.csv успешно создан!")
