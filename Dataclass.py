import sqlite3

class Person:
    def __init__(self, number, first, last, age):
        self.number = number
        self.first = first
        self.last = last
        self.age = age
        self.connector = sqlite3.connect("mydata.db")
        self.cursor = self.connector.cursor()

    def findperson(self, person_id):
        self.cursor.execute("SELECT * FROM Person WHERE id=?", (person_id,))
        result = self.cursor.fetchone()
        print(result)

    def insertperson(self):
        self.cursor.execute("INSERT INTO Person (id, first_name, last_name, age) VALUES (?, ?, ?, ?)",
                            (self.number, self.first, self.last, self.age))
        self.connector.commit()

# Ensure the table is created (if not already created)
connection = sqlite3.connect("mydata.db")
cursor = connection.cursor()

# Insert a new person
# p1 = Person(5, "SHri Harish", "Saravanan", 12)
# p1.insertperson()

# Function to find a person by ID
def findtheguy(p_id):
    connection = sqlite3.connect("mydata.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Person WHERE id=?", (p_id,))
    print(cursor.fetchall())
    connection.close()

# Find the person with ID 4
findtheguy(5)

# Uncomment to print all rows in the table
# connection = sqlite3.connect("mydata.db")
# cursor = connection.cursor()
# cursor.execute("SELECT * FROM Person")
# rows = cursor.fetchall()
# for row in rows:
#     print(row)
# connection.close()
