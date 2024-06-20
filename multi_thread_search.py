import os
import threading
import time
from queue import Queue

# Пошукові ключові слова
KEYWORDS = ["keyword1", "keyword2", "keyword3"]

# Директорія з текстовими файлами
DIRECTORY = "test_files"

def search_in_file(file_path, results):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            for keyword in KEYWORDS:
                if keyword in text:
                    results[keyword].append(file_path)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def worker(files_queue, results):
    while True:
        file_path = files_queue.get()
        if file_path is None:
            break
        search_in_file(file_path, results)
        files_queue.task_done()

def main():
    files_queue = Queue()
    results = {keyword: [] for keyword in KEYWORDS}

    # Додавання файлів у чергу
    try:
        for file_name in os.listdir(DIRECTORY):
            file_path = os.path.join(DIRECTORY, file_name)
            if os.path.isfile(file_path):
                files_queue.put(file_path)
    except Exception as e:
        print(f"Error reading directory {DIRECTORY}: {e}")
        return

    # Створення та запуск потоків
    num_threads = 4
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(files_queue, results))
        thread.start()
        threads.append(thread)

    # Очікування завершення черги
    files_queue.join()

    # Завершення потоків
    for _ in threads:
        files_queue.put(None)
    for thread in threads:
        thread.join()

    return results

if __name__ == "__main__":
    start_time = time.time()
    results = main()
    end_time = time.time()

    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time} seconds")
