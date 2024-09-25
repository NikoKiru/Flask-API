import sqlite3
from data_dict import random_users

def create():
    with sqlite3.connect('school.db') as conn:
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                birth_date TEXT,
                gender TEXT,
                email TEXT,
                phonenumber TEXT,
                address TEXT,
                nationality TEXT,
                active BOOLEAN,
                github_username TEXT
            )
        ''')

        members_data = [
            (
                user["first_name"], 
                user["last_name"], 
                user["birth_date"], 
                user["gender"], 
                user["email"], 
                user["phonenumber"], 
                user["address"], 
                user["nationality"], 
                user["active"], 
                user["github_username"]
            ) 
            for user in random_users
        ]

        cur.executemany('''
            INSERT INTO members (
                first_name, last_name, birth_date, gender, email, phonenumber, address, nationality, active, github_username
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', members_data)



def read():
    members = []

    with sqlite3.connect('school.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM members')

        for row in cur.fetchall():
            members.append({
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'birth_date': row[3],
                'gender': row[4],
                'email': row[5],
                'phonenumber': row[6],
                'address': row[7],
                'nationality': row[8],
                'active': row[9],
                'github_username': row[10]
            })

    return members



if __name__ == '__main__':
    create()  
    members = read()  
    print(members)  