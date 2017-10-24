import numpy as np
manifest_file = open("data/streetstyle27k.manifest", "r")
lines = manifest_file.readline().split(",")
cities = ['Bangkok', 'Beijing', 'Bogot\xc3\x83\xc2\xa1', 'Buenos Aires', 'Cairo', 'Delhi', 'Dhaka', 'Guangzhou', 'Istanbul', 'Jakarta', 'Karachi', 'Kolkata', 'Lagos', 'London', 'Los Angeles', 'Manila', 'Mexico City', 'Mumbai', 'New York City', 'Osaka', 'Rio de Janeiro', 'S\xc3\x83\xc2\xa3o Paulo', 'Seoul', 'Shanghai', 'Tianjin', 'Tokyo', 'Paris', 'Berlin', 'Madrid', 'Kiev', 'Rome', 'Budapest', 'Milan', 'Sofia', 'Nairobi', 'Sydney', 'Moscow', 'Johannesburg', 'Toronto', 'Vancouver', 'Chicago', 'Austin', 'Seattle', 'Singapore']
counts = dict()
print("index, item")
for i, item in enumerate(lines):
    print("{}, {}".format(i, item))
for lines in manifest_file:
    split = lines.split(',')
    if len(split) > 3:
        city = split[3]
        if city in counts:
             counts[city] += 1
        else:
             counts[city] = 1
print("The number of images for each city")
print("City id, City Name, Count")
total = 0
for i in range(1, 45):
    current_count = 0
    if str(i) in counts:    
        current_count = counts[str(i)]
    total += current_count
    print("{}, {}, {}".format(i, cities[i - 1], current_count))
print("The total number of images in the dataset is {}".format(total))
