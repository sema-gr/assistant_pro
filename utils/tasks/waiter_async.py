import asyncio
import time

# Це наша асинхронна функція "кухар"
async def cook_steak(table_number):
    print(f"Кухар отримав замовлення і почав готувати стейк для столика {table_number}...")
    # asyncio.sleep не блокує виконання всього коду, а "призупиняє" цю конкретну задачу
    await asyncio.sleep(3) 
    print(f"Стейк для столика {table_number} готовий!")
    return f"Стейк для столика {table_number}"

# Це наша основна функція "офіціант"
async def serve_table(table_number):
    print(f"Офіціант підходить до столика {table_number}")
    print(f"Офіціант приймає замовлення у столика {table_number}")
    
    print(f"Офіціант передає замовлення стейка для столика {table_number} на кухню.")
    # Офіціант запускає асинхронну задачу і йде далі, не чекаючи результату
    steak_task = asyncio.create_task(cook_steak(table_number))
    
    # Офіціант може робити щось інше, поки стейк готується.
    # Наприклад, підійти до іншого столика (це відбувається в main())
    
    # Офіціант "чекає" на готовність стейка тільки тоді, коли це дійсно потрібно
    steak = await steak_task
    
    print(f"Офіціант отримав {steak} і подає його столику {table_number}")
    print("-" * 20)

async def main():
    start_time = time.time()
    
    # Ми запускаємо обслуговування трьох столиків "одночасно"
    tasks = [
        asyncio.create_task(serve_table(1)),
        asyncio.create_task(serve_table(2)),
        asyncio.create_task(serve_table(3)),
    ]
    
    # Офіціант приймає замовлення в усіх трьох столиків майже миттєво,
    # і всі три стейки починають готуватися паралельно.
    
    # Чекаємо, поки всі столики будуть обслужені
    await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"Загальний час: {end_time - start_time:.2f} секунд")

asyncio.run(main())