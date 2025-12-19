
import csv
import re
from pprint import pprint

with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

for contact in contacts_list[1:]:
    full_name = ' '.join(contact[:3]).strip()
    name_parts = full_name.split()
    
    if len(name_parts) == 3:
        contact[0], contact[1], contact[2] = name_parts
    elif len(name_parts) == 2:
        contact[0], contact[1] = name_parts
        contact[2] = ''
    elif len(name_parts) == 1:
        contact[0] = name_parts[0]
        contact[1] = ''
        contact[2] = ''

def format_phone(phone):
    if not phone:
        return ''
    
    phone = phone.strip()
    extension = ''
    
    if 'доб.' in phone.lower():
        parts = re.split(r'доб\.?\s*', phone, flags=re.IGNORECASE)
        phone = parts[0]
        if len(parts) > 1:
            ext_digits = re.findall(r'\d+', parts[1])
            if ext_digits:
                extension = 'доб.' + ''.join(ext_digits)
    
    digits = re.findall(r'\d+', phone)
    phone_digits = ''.join(digits)
    
    if phone_digits:
        if phone_digits.startswith('8') or phone_digits.startswith('7'):
            phone_digits = phone_digits[1:] if len(phone_digits) > 10 else phone_digits
        elif len(phone_digits) == 10:
            pass
        else:
            return phone
        
        if len(phone_digits) == 10:
            formatted = f"+7({phone_digits[:3]}){phone_digits[3:6]}-{phone_digits[6:8]}-{phone_digits[8:]}"
            if extension:
                formatted += f" {extension}"
            return formatted
    
    return phone

for contact in contacts_list:
    if len(contact) > 5:
        contact[5] = format_phone(contact[5])

merged_contacts = {}
headers = contacts_list[0]

for contact in contacts_list[1:]:
    if len(contact) < 2:
        continue
    
    key = (contact[0], contact[1])
    
    if key not in merged_contacts:
        merged_contacts[key] = contact.copy()
    else:
        existing = merged_contacts[key]
        for i in range(len(contact)):
            if contact[i] and not existing[i]:
                existing[i] = contact[i]
        
        if contact[2] and not existing[2]:
            existing[2] = contact[2]

result_list = [headers]
result_list.extend(list(merged_contacts.values()))

with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result_list)
