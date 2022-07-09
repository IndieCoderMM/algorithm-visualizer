def bubble_sort(array: list, ascending: bool=True) -> tuple[list, bool]:
	for i in range(len(array)-1):
		for j in range(len(array)-1-i):
			num1 = array[j]
			num2 = array[j+1]

			if(num1>num2 and ascending) or (num1<num2 and not ascending):
				array[j], array[j+1] = array[j+1], array[j]
				return array, False
	return array, True


def insertion_sort(array: list, ascending: bool=True) -> tuple[list, bool]:
	for i in range(1, len(array)):
		current = array[i]

		while True:
			ascending_sort = i > 0 and array[i-1] > current and ascending
			descending_sort = i > 0 and array[i-1] < current and not ascending

			if not ascending_sort and not descending_sort:
				break

			array[i] = array[i-1]
			i = i - 1
			array[i] = current
			return array, False
	return array, True

def selection_sort(array: list, ascending: bool=True) -> tuple[list, bool]:
	for i in range(0, len(array)-1):
		selected = i
		for j in range(i+1, len(array)):
			if (array[j] < array[selected] and ascending) or (array[j] > array[selected] and not ascending):
				selected = j
				array[i], array[selected] = array[selected], array[i]
				return array, False
	return array, True

def quick_sort(array: list, ascending: bool=True) -> tuple[list, bool]:
	if len(array) <= 1:
		return array, False
	pivot = array[-1]
	for i in range(len(array)-1):
		smaller = []
		larger = []
		if array[i] < pivot:
			smaller.append(array[i])
		else:
			larger.append(array[i])
	array = quick_sort(smaller, ascending)[0] + [pivot] + quick_sort(larger, ascending)[0]

	return array, True
