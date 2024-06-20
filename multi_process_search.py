import os
import multiprocessing
import time

# Пошукові ключові слова
KEYWORDS = ["keyword1", "keyword2", "keyword3"]

# Директорія з текстовими файлами
DIRECTORY = "test_files"

def search_in_files(file_paths, results_queue):
    results = {keyword: [] for keyword in KEYWORDS}
    for file_path in file_paths:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
                for keyword in KEYWORDS:
                    if keyword in text:
                        results[keyword].append(file_path)
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
    results_queue.put(results)

def main():
    manager = multiprocessing.Manager()
    results_queue = manager.Queue()

    # Додавання файлів у список
    files = []
    try:
        for file_name in os.listdir(DIRECTORY):
            file_path = os.path.join(DIRECTORY, file_name)
            if os.path.isfile(file_path):
                files.append(file_path)
    except Exception as e:
        print(f"Error reading directory {DIRECTORY}: {e}")
        return

    # Розподіл файлів на підсписки
    num_processes = os.cpu_count()
    file_chunks = [files[i::num_processes] for i in range(num_processes)]

    # Створення та запуск процесів
    processes = []
    for chunk in file_chunks:
        process = multiprocessing.Process(target=search_in_files, args=(chunk, results_queue))
        process.start()
        processes.append(process)

    # Очікування завершення процесів
    for process in processes:
        process.join()

    # Збирання результатів
    results = {keyword: [] for keyword in KEYWORDS}
    while not results_queue.empty():
        file_results = results_queue.get()
        for keyword, file_paths in file_results.items():
            results[keyword].extend(file_paths)

    return results

if __name__ == "__main__":
    start_time = time.time()
    results = main()
    end_time = time.time()

    print(f"Results: {results}")
    print(f"Time taken: {end_time - start_time} seconds")
