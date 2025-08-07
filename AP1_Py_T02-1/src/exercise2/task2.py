import asyncio
import os
import aiohttp
from prettytable import PrettyTable

async def download_image(session, url, save_path):
    try:
        async with session.get(url) as response:
            # Проверим, успешно ли выполнен запрос
            if response.status == 200:
                file_name = os.path.join(save_path, url.split("/")[-1])
                with open(file_name, 'wb') as f:
                    f.write(await response.read())
                return url, "Успех"
            else:
                return url, "Ошибка"
    except Exception as e:
        return url, "Ошибка"

async def main():
    save_path = input("Введите путь для сохранения изображений: ")
    
    # Проверим доступность пути
    while not os.path.exists(save_path) or not os.access(save_path, os.W_OK):
        print("Некорректный путь или нет доступа к этому пути. Попробуйте снова.")
        save_path = input("Введите путь для сохранения изображений: ")

    urls = []
    while True:
        url = input("Введите ссылку на изображение (или пустую строку для завершения): ")
        if not url:
            break
        urls.append(url)

    print("\nЗагрузка...")

    # Создаем сессию aiohttp
    async with aiohttp.ClientSession() as session:
        tasks = [download_image(session, url, save_path) for url in urls]
        results = await asyncio.gather(*tasks)

    # Выводим сводку с помощью PrettyTable
    print("\nСводка об успешных и неуспешных загрузках")
    table = PrettyTable()
    table.field_names = ["Ссылка", "Статус"]
    
    for url, status in results:
        table.add_row([url, status])
    
    print(table)

if __name__ == "__main__":
    asyncio.run(main())
