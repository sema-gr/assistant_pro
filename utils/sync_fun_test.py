import time

def serve_table(table_number):
    print(f"Офіціант підходить до столика {table_number}")
    print(f"Офіціант приймає замовлення у столика {table_number}")
    
    print(f"Офіціант іде на кухню і починає готувати стейк для столика {table_number}...")
    # Це блокуюча операція. Офіціант нічого іншого не може робити.
    time.sleep(3) 
    print(f"Стейк для столика {table_number} готовий!")
    
    print(f"Офіціант подає стейк столику {table_number}")
    print("-" * 20)

start_time = time.time()

# Обслуговуємо 3 столики послідовно
serve_table(1)
serve_table(2)
serve_table(3)

end_time = time.time()
print(f"Загальний час: {end_time - start_time:.2f} секунд")

