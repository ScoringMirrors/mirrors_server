# mirrors_server

### 运行步骤
```
 1. pip install -r requirements.txt
 2. python manage.py migrate
 3. python manage.py runserver
```

### 登录API
```
curl POST --user username:password http://127.0.0.1/api/v1/accounts/login/ -v
```

### 登出API
```
curl http://127.0.0.1/api/v1/accounts/logout/  -v
```

### 获取验证码API
```
curl http://127.0.0.1/api/v1/accounts/get_check_code/ -v
```
