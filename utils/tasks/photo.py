import asyncio

async def resize_image(img_id):
    print(f"Зменшуємо фото {img_id}...")
    await asyncio.sleep(1)
    return f"Small_{img_id}"

async def apply_filter(img_name):
    print(f"Накладаємо фільтр на {img_name}...")
    await asyncio.sleep(1)
    return f"Filtered_{img_name}"

async def upload_to_cloud(img_name):
    print(f"Завантажуємо {img_name} на сервер...")
    await asyncio.sleep(1.5)
    print(f"Фото {img_name} доступне за посиланням!")

async def process_user_upload(img_id):
    # Ланцюжок дій для одного фото (одна за одною, але асинхронно)
    img_small = await resize_image(img_id)
    img_filtered = await apply_filter(img_small)
    await upload_to_cloud(img_filtered)

async def main():
    # Уявіть, що два користувачі завантажили фото одночасно
    print("--- Початок обробки черги фото ---")
    await asyncio.gather(
        process_user_upload("user_1_photo.jpg"),
        process_user_upload("user_2_photo.jpg")
    )

asyncio.run(main())