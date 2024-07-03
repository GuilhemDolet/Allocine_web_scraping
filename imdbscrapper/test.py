# dirty_list =  ['De', 'Christopher Nolan', 'Par', 'Christopher Nolan']

# start = True
# stop = False
# liste_propre = []

# for item in dirty_list:
#     if item.lower() == 'de':
#         start = True
#     elif item.lower() == 'par':
#         stop = True
#     elif start and not stop:
#         liste_propre.append(item)
# print(liste_propre)

# item = ', '.join(liste_propre)
# print(item)
# print(type(item))

# one_element_list = ['Russie']

# one_string = ''.join(one_element_list)
# other = one_element_list[0]
# print(len(one_element_list))
# print(type(other))
# print(one_string)

# un_string = "3,4"
# un_float = un_string.replace(',', '.')
# print(un_float)
# un_float_bon = float(un_float)
# print(type(un_float_bon), un_float_bon)

# un_string = "8 Saisons"


# un_integer = int(un_string.split()[0])

# print(type(un_integer))



une_liste= ['Avec', 'Masahiro Motoki', 'Tsutomu Yamazaki', 'Ryoko Hirosue']
une_liste.pop()
print(une_liste)
