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

### 校验验证码API
```
curl -X POST -d image_id=image_id -d image_value=image_value http://127.0.0.1/api/v1/accounts/get_check_code/ -v
```

### 用户注册API
```
culr -X POST -d nikename=nikename -d email=email -d password=password -d password2=password2 -d image_id=image_id -d register_token=register_token http://127.0.0.1/api/v1/accounts/register -v
```
