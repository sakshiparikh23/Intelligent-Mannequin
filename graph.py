import numpy as np
import matplotlib.pyplot as plt
import pymysql

connection = pymysql.connect(host='localhost',
                                user='root',
                                password='',
                                db='intelligent_mannequin',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor)
	
try:
    with connection.cursor() as cursor:
    	sql = "SELECT  * FROM user_response"
    	cursor.execute(sql)
    	result = cursor.fetchall()

finally:
    connection.close()

Users = result[-1]['id']

Colours = list()

Sizes = list()

for elements in result:

	Colours.append(elements['colour'])
	Sizes.append(elements['size'])

my_dict1 = {i:Colours.count(i) for i in Colours}
Frequency_Colours = my_dict1.values();
Name_Colours = my_dict1.keys();

my_dict2 = {i:Sizes.count(i) for i in Sizes}
Frequency_Sizes = my_dict2.values();
Name_Sizes = my_dict2.keys();

print("Number of users showed intrest in buying the dress are {0}".format(Users))

index = np.arange(len(Name_Colours))
fig = plt.figure('Colours')
plt.bar(index, Frequency_Colours)
plt.xlabel('Colour', fontsize=10)
plt.ylabel('Number of colours sold', fontsize=10)
plt.xticks(index, Name_Colours, fontsize=10, rotation=30)
plt.title('Colour in demand')

index = np.arange(len(Name_Sizes))
fig2 = plt.figure('Sizes')
plt.bar(index, Frequency_Sizes)
plt.xlabel('Sizes', fontsize=10)
plt.ylabel('Number of Sizes sold', fontsize=10)
plt.xticks(index, Name_Sizes, fontsize=10, rotation=30)
plt.title('Sizes in demand')
plt.show()

