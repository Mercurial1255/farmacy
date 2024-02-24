from tabulate import tabulate
import psycopg2
from datetime import datetime


def connect():   #done
    db_con = psycopg2.connect(
        database='dorixona',
        user='postgres',
        password='12551935',
        host='localhost',
        port=5432
    )
    return db_con


def menu():   #done
    print("\n1. Hamma bor maxsulotlarni ko'rish")
    print("2. Yangi maxsulot qo'shish")
    print("3. Maxsulotlarni o'chirish")
    print("4. Maxsulotlarni qidirish")
    print("5. Oylik statistikalar")
    print("6. Dasturdan chiqish")


def show_data(dori=None):  #done
    if(dori is None):
        dori = read()

    header = ('ID', 'name', 'price', 'count', 'date of import', 'validity period')
    table = tabulate(dori, header, tablefmt='grid')
    print(table)


def search_by_name(name=None):
    if(name is None):
        name = input("Maxsulot nomini kiriting: ")

    con = connect()
    cur = con.cursor()
    query = '''
        select * from dori where name=%s 
    '''
    values = (name,)
    cur.execute(query, values)
    res = []
    res.append(cur.fetchone())
    con.close()
    show_data(res)


def search(name):
    con = connect()
    cur = con.cursor()
    query = '''
        select * from dori where name=%s 
    '''
    values = (name,)
    cur.execute(query, values)
    res = cur.fetchone()
    con.close()
    if(res):
        return True
    else:
        return False


def bought(): #yangi maxsulot keldi
    nomi = input("Maxsulot nomi kiriting: ")
    if(search(nomi)):
        coo = int(input("Maxsulot sonini kiriting: "))
        con = connect()
        cur = con.cursor()

        s = read_one(id)
        count = s[3] + coo
        query = '''
            update dori set count=(%s)
            where id=%s
        '''

        values = (count, id)
        cur.execute(query, values)
        con.commit()
        con.close()
    else:
        create(nomi)


def create(name=None):
    if(name is None):
        name = input("Maxsulot nomini kiriting: ")
    price = float(input("Narxini kiriting: "))
    count = int(input("Sonini kiriting: "))
    now = datetime.now()
    arrived = now.strftime('%Y-%m-%d')
    validity = input("Amal qilish muddati: 'YYYY-MM-DD': ")

    con = connect()
    cur = con.cursor()
    query = f'''
    insert into dori(name, price, count, arrived, validity) values (%s, %s, %s, %s, %s);
    '''
    values = (name, price, count, arrived, validity,)
    cur.execute(query, values)
    con.commit()
    con.close()


def read():
    con = connect()
    cur = con.cursor()
    query = '''
        select * from dori
        where count > 0; 
    '''
    cur.execute(query)
    result = cur.fetchall()
    con.close()
    return result


def read_one(id):
    con = connect()
    cur = con.cursor()
    query = '''
        select * from dori where id=%s
    '''
    values = (id,)
    cur.execute(query, values)
    result = cur.fetchone()
    con.close()
    return result


def sold(id=None, coo=None):
    id = int(input("Idni kiriting: "))
    coo = int(input("Sonini kiriting: "))
    con = connect()
    cur = con.cursor()

    s = read_one(id)
    if(s):
        count = s[3] - coo

        query = '''
            update dori set count=(%s)
            where id=%s
        '''

        values = (count, id)
        cur.execute(query, values)
        con.commit()
        con.close()



def monthly_statistics(year, month):
    con = connect()
    cur = con.cursor()
    #sotib olingan
    query = """
        SELECT SUM(miqdori) AS jami_miqdor
        FROM oylik_harakatlar
        WHERE qaysi_yil = %s AND qaysi_oy = %s AND harakat_turi = 'sotib_olindi'
    """
    values=(year, month)
    cur.execute(query, values)
    sotib_olingan = cur.fetchone()[0] or 0
    print("Sotib olingan maxsulotlar: ", sotib_olingan)
    # Sotilgan mahsulotlar soni
    query = """
        SELECT SUM(miqdori) AS jami_miqdor
        FROM oylik_harakatlar
        WHERE qaysi_yil = %s AND qaysi_oy = %s AND harakat_turi = 'sotilgan'
    """
    values = (year, month)
    cur.execute(query, values)
    sotilgan = cur.fetchone()[0] or 0
    print(sotilgan)
    con.commit()
    con.close()

def statistika():
    year = int(input("Yilni kiriting (2024): "))
    month = int(input("Oyni kiriting (1-12): "))

    a = monthly_statistics(year, month)
    print(a)