import asyncio
import time

async def fetch_url(site_name, delay):
    print(f"Починаю завантаження {site_name}...")
    # Імітуємо мережеву затримку
    await asyncio.sleep(delay)
    print(f"{site_name} завантажено за {delay} сек.")
    return f"Дані з {site_name}"

async def main():
    start_time = time.time()
    
    # Створюємо список задач для одночасного виконання
    tasks = [
        fetch_url("Google", 2),
        fetch_url("GitHub", 3),
        fetch_url("StackOverflow", 1)
    ]
    
    # Чекаємо на всі результати разом
    results = await asyncio.gather(*tasks)
    
    print(f"\nОтримані дані: {results}")
    print(f"Загальний час: {time.time() - start_time:.2f} секунд")

asyncio.run(main())