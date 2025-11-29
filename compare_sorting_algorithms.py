import timeit
import random
from typing import Callable

from merge_sort import merge_sort
from insertion_sort import insertion_sort


def generate_random_array(size: int) -> list[int]:
    return [random.randint(1, 10000) for _ in range(size)]


def generate_sorted_array(size: int) -> list[int]:
    return list(range(1, size + 1))


def generate_reverse_sorted_array(size: int) -> list[int]:
    return list(range(size, 0, -1))


def generate_partially_sorted_array(size: int) -> list[int]:
    arr = list(range(1, size + 1))
    num_swaps = size // 10
    for _ in range(num_swaps):
        i = random.randint(0, size - 1)
        j = random.randint(0, size - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


def measure_time(
    func: Callable[[list[int]], list[int]], arr: list[int], number: int = 1
) -> float:
    def wrapper():
        return func(arr.copy())

    times = timeit.repeat(wrapper, repeat=3, number=number)
    return min(times) / number


def run_comparison() -> dict[str, dict[int, dict[str, float]]]:
    sizes = [100, 500, 1000, 5000, 10000]

    algorithms = {
        "Merge Sort": merge_sort,
        "Insertion Sort": insertion_sort,
        "Timsort": sorted,
    }

    data_types = {
        "Random data": generate_random_array,
        "Sorted data": generate_sorted_array,
        "Reverse sorted": generate_reverse_sorted_array,
        "Partially sorted": generate_partially_sorted_array,
    }

    results = {}

    print("Comparative analysis of sorting algorithms\n")

    for data_type_name, data_generator in data_types.items():
        print(f"Data type: {data_type_name}")

        results[data_type_name] = {}

        for size in sizes:
            arr = data_generator(size)

            times = {}

            for algo_name, algo_func in algorithms.items():
                try:
                    number = 1 if size >= 5000 else 5
                    time_taken = measure_time(algo_func, arr, number=number)
                    times[algo_name] = time_taken
                except Exception as e:
                    print(f"Error executing {algo_name}: {e}")
                    times[algo_name] = float("inf")

            results[data_type_name][size] = times

            merge_time = times.get("Merge Sort", 0)
            insertion_time = times.get("Insertion Sort", 0)
            timsort_time = times.get("Timsort", 0)
            best_algo = min(times, key=times.get)

            output = f"""Size: {size}
  Merge Sort: {merge_time*1000:.3f} ms
  Insertion Sort: {insertion_time*1000:.3f} ms
  Timsort: {timsort_time*1000:.3f} ms
  Fastest: {best_algo}
"""
            print(output)

    return results


def analyze_complexity(results: dict[str, dict[int, dict[str, float]]]) -> None:
    print("Complexity analysis of algorithms\n")

    random_data = results.get("Random data", {})

    if random_data:
        print("Analysis on random data:\n")

        prev_merge = None
        prev_insertion = None
        prev_timsort = None

        for size in sorted(random_data.keys()):
            times = random_data[size]
            merge_time = times.get("Merge Sort", 0)
            insertion_time = times.get("Insertion Sort", 0)
            timsort_time = times.get("Timsort", 0)

            merge_ratio = ""
            if prev_merge:
                ratio = merge_time / prev_merge if prev_merge > 0 else 0
                merge_ratio = f" (x{ratio:.2f})"

            insertion_ratio = ""
            if prev_insertion:
                ratio = insertion_time / prev_insertion if prev_insertion > 0 else 0
                insertion_ratio = f" (x{ratio:.2f})"

            timsort_ratio = ""
            if prev_timsort:
                ratio = timsort_time / prev_timsort if prev_timsort > 0 else 0
                timsort_ratio = f" (x{ratio:.2f})"

            output = f"""Array size: {size}
Merge Sort: {merge_time*1000:.3f} ms{merge_ratio}
Insertion Sort: {insertion_time*1000:.3f} ms{insertion_ratio}
Timsort: {timsort_time*1000:.3f} ms{timsort_ratio}
"""
            print(output)

            prev_merge = merge_time
            prev_insertion = insertion_time
            prev_timsort = timsort_time


if __name__ == "__main__":
    comparison_results = run_comparison()
    analyze_complexity(comparison_results)
