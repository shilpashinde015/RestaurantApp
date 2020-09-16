import sqlalchemy as db
import pandas as pd

engine = db.create_engine('sqlite:///restaurantmenu.db')
connection = engine.connect()
metadata = db.MetaData()

restaurant = db.Table('restaurant', metadata, autoload=True, autoload_with=engine)

query = db.select([restaurant])
ResultProxy = connection.execute(query)

ResultSet = ResultProxy.fetchall()
print(ResultSet)

query = db.delete(restaurant).where(restaurant.columns.name =='None')
results = connection.execute(query)
results = connection.execute(db.select([restaurant])).fetchall()
df = pd.DataFrame(results)
df.columns = results[0].keys()
df.head(4)
print(results)
