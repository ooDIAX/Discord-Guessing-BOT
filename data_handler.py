import psycopg2
import sys
import os
import random
import dotenv

dotenv.load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv('POSTGRES_HOST_EXTERNAL'),
        database=os.getenv('POSTGRES_DB'),
        user=os.getenv('POSTGRES_USER'),
        password=os.getenv('POSTGRES_PASSWORD')
    )
    return conn


def generate_players():
    customers = []
    names = ['John', 'Mary', 'Peter', 'Kate', 'Bob', 'Alice', 'Jack', 'Jane', 'Mike', 'Ann']
    # last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez']

    for i in range(10):
        id = os.urandom(4).hex()
        discordid = random.randint(1000,9999)
        name = names[i % 10] + '#' + str(discordid)
        customers.append((id, name, random.randint(1,23)))

    return customers

def create_leaderboard_table():
    players = generate_players()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS leaderboard")
    cur.execute("CREATE TABLE leaderboard (ID varchar(255), player varchar(255), score int)")

    for player in players:
        cur.execute("INSERT INTO leaderboard VALUES (%s, %s, %s)", player)

    conn.commit()
    cur.close()
    conn.close()

def create_history():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS history")
    cur.execute("CREATE TABLE history (score int)")

    val = 9
    cur.execute("INSERT INTO history VALUES (%s)", (val,))

    conn.commit()
    cur.close()
    conn.close()

def add_history(val):
    conn = get_db_connection()
    cur = conn.cursor()
   
    cur.execute("INSERT INTO history VALUES (%s)", (val,))

    conn.commit()
    cur.close()
    conn.close()


def get_history():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT score FROM history")
    rows = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return rows


def add_score(name):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # cur.execute("SELECT SCORE FROM leaderboard WHERE player=%s", name)    
    cur.execute("SELECT score FROM leaderboard WHERE player=%s",(name,))
    rows = cur.fetchall()
    print(rows)
    if rows == []:
        val = (os.urandom(8).hex(), name, 1)
        cur.execute("INSERT INTO leaderboard VALUES (%s, %s, %s)", val)
    else:
        cur.execute("UPDATE leaderboard SET score=%s WHERE player=%s", (rows[0][0] + 1, name))

    conn.commit()
    cur.close()
    conn.close()

def get_leaderboard():
    # connect to the PostgreSQL server
    conn = psycopg2.connect(host=os.getenv('POSTGRES_HOST_EXTERNAL'),
                            database=os.getenv('POSTGRES_DB'),
                            user=os.getenv('POSTGRES_USER'),
                            password=os.getenv('POSTGRES_PASSWORD'))

    # read products from database
    cur = conn.cursor()
    cur.execute('SELECT * FROM leaderboard ORDER BY score DESC')
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    # render products template

    return rows
    


if __name__ == '__main__':
    create_history()
    create_leaderboard_table()
