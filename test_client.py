from pgrestpy.client import *
#
p = pg("local")
print(p.sql("show sources;"))


