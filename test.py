from pgrestpy.client import *
x = pg("local")
print(x.sql("show sources;"))


