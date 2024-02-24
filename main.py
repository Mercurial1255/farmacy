from functions import show_data, read, sold, bought, search_by_name, menu, search, statistika

print(search('fawoie'))

while True:
    menu()
    a = int(input())
    if(a == 1):   #ma'lumotni ekranga chiqarish done
        show_data()
    elif(a == 2):  #yangi maxsulot qo'shish
        bought()
    elif(a == 3):
        sold()
    elif(a == 4):
        search_by_name()
    elif(a == 5):
        statistika()
    else:
        break
