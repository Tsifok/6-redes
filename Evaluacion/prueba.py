array = [
    ("Tsifok","hola"),
    ("Herman","alo22"),
    ("Matias","herman")
]

online_users = []

for usuario, password in array:    
    online_users.append([usuario, password])    
        
online_users.remove(online_users[0])        




print(online_users)
    
    




