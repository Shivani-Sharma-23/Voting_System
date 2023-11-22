conn = sqlite3.connect('databaza.db')
c = conn.cursor()
conn.text_factory = str    
data3 = str(input('Please enter name: '))
query = "DELETE FROM Zoznam WHERE Name = '%s';" % data3.strip()
print(query)
mydata = c.execute(query)
