fibonacci(10)
134
+++++
def fibonacci(n):
    # Base cases
    if n <= 0:
        return "Input should be a positive integer"
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        # Using iteration for better performance
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        return b
fibonacci(10)