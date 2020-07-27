class Node():
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

a = set(Node(str(i)) for i in range(10))
print(a)

print("2" in a)

for i in a:
    print(type(i),i)
