# python-linked-list
Linked list implementation in Python

### Sample Usage
```python
ll = linked_list()
ll.add(2)
ll.add(1)
ll.add(0)
ll.add(5)
ll.add(6)
ll.add(30)
ll.add(1000)
print(ll) # 2,1,0,5,6,30,1000

ll.insert_at(300, 3)
print(ll) # 2,1,0,300,5,6,30,1000

# for searching
print(ll.search(2)) # 2 or None if not found

# create new linked list 
l2 = linked_list()
l2.add(900)

# add linked lists
l3 = ll + l2
print(l3) # combined list
```
