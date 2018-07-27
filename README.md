# FlaskCodeTemplate
python flask code template

# test
正确例子：
```
curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "name":"222"
}' \
 'http://localhost:5000/invoke/w3/user'
 ```
 
 异常例子：
 ```
 curl -i -X POST \
   -H "Content-Type:application/json" \
   -d \
'{
  "name":""
}' \
 'http://localhost:5000/invoke/w3/user'
 ```