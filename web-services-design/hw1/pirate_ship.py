capacity, m = map(int, input().split())

items = []

for _ in range(m):
    name, weight, value = input().split()
    weight = float(weight)
    value = float(value)
    density = value / weight
    items.append((name, weight, value, density))

items.sort(key=lambda x: x[3], reverse=True)

result = []

for name, weight, value, density in items:

    if capacity <= 0:
        break

    if weight <= capacity:
        result.append((name, weight, value))
        capacity -= weight
    else:
        fraction = capacity / weight
        taken_weight = capacity
        taken_value = value * fraction
        result.append((name, taken_weight, taken_value))
        capacity = 0

for name, weight, value in result:
    print(f"{name} {weight:.2f} {value:.2f}")
