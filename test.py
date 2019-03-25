src = '10.0.0.1'
print("\'src\'")
test = '10.0.0.2,10.0.0.3,,10.0.0.4'
t1 = test.split(',')
for t in t1:
    print(type(t))
    print(t)
