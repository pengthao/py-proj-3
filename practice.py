

def equalsZero(lis):
    numbers = set()

    for num in lis:
        inv = -num
        if inv in numbers:
            return True
        numbers.add(num)
    return False


nums = [1, 2, 3, 5, 8, 1, 6, 10, -5, -7, -22, -15]
print(equalsZero(nums))  # Output: True

nums1 = [2, 3, 4, 8, 20, -15, 27, 46]
print(equalsZero(nums1))  # Output: False