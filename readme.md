
## 项目技术栈
前端待定
后端 python+django 
数据库 sqlite3

## 环境配置
1.  安装 Django 和 Django REST Framework
    ```bash
    pip install django djangorestframework
    ```
2.  数据库
    Python 自带 `sqlite3` 模块，无需额外安装。

## 如何启动项目

1.  进入后端项目目录
    ```bash
    cd backend
    ```

2.  应用数据库迁移
    首次启动或模型有变动时，需要执行此命令来创建或更新数据库表结构。
    ```bash
    python manage.py migrate
    ```

3.  （可选）创建管理员用户
    如果需要访问后台管理或测试需要认证的接口，请创建一个超级用户。
    ```bash
    python manage.py createsuperuser
    ```
    然后根据提示输入用户名和密码。

4.  启动开发服务器
    ```bash
    python manage.py runserver
    ```
    服务将默认运行在 `http://127.0.0.1:8000/`。

## API 接口测试

API 的根路径为 `/api/`。

**注意**: 当前项目配置为允许任何用户访问所有接口（包括增删改），无需身份验证，方便开发和测试。

### 航班管理

#### 1. 新增航班
-   URL: `/api/flights/`
-   Method: `POST`
-   Body (JSON):
    ```json
    {
        "flight_number": "CA123",
        "departure_city": "Beijing",
        "destination_city": "Shanghai",
        "departure_time": "2025-10-01T10:00:00Z",
        "arrival_time": "2025-10-01T12:00:00Z",
        "airline": "Air China",
        "aircraft_type": "Boeing 737",
        "economy_seats": 150,
        "economy_price": "800.00",
        "first_class_seats": 10,
        "first_class_price": "2000.00"
    }
    ```
-   Curl 示例:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"flight_number": "CA123", "departure_city": "Beijing", "destination_city": "Shanghai", "departure_time": "2025-10-01T10:00:00Z", "arrival_time": "2025-10-01T12:00:00Z", "airline": "Air China", "aircraft_type": "Boeing 737", "economy_seats": 150, "economy_price": "800.00", "first_class_seats": 10, "first_class_price": "2000.00"}' http://127.0.0.1:8000/api/flights/
    ```

#### 2. 查看航班列表
-   URL: `/api/flights/`
-   Method: `GET`
-   Curl 示例:
    ```bash
    curl http://127.0.0.1:8000/api/flights/
    ```

#### 3. 修改航班信息
- URL: `/api/flights/{id}/`

  -   Method: `PATCH`

- Curl 示例 (修改 id 为 1 的航班):
  ```bash
  curl -X PUT -H "Content-Type: application/json" -d '{"economy_seats": 140}' http://127.0.0.1:8000/api/flights/1/
  ```

#### 4. 删除航班
-   URL: `/api/flights/{id}/`
-   Method: `DELETE`
-   Curl 示例 (删除 id 为 1 的航班):
    ```bash
    curl -X DELETE http://127.0.0.1:8000/api/flights/1/
    ```

### 航班查询

#### 1. 按条件搜索航班
-   URL: `/api/flights/search/`
-   Method: `GET`
-   Query Parameters:
    -   `departure_city` (string)
    -   `destination_city` (string)
    -   `departure_date` (string, 格式: YYYY-MM-DD)
-   Curl 示例:
    ```bash
    curl "http://127.0.0.1:8000/api/flights/search/?departure_city=Beijing&destination_city=Shanghai&departure_date=2025-10-01"
    ```

### 订座功能

#### 1. 创建订座
-   URL: `/api/bookings/`
-   Method: `POST`
-   Body (JSON):
    ```json
    {
        "user": 1,
        "flight": 1,
        "seat_class": "economy",
        "seat_count": 2
    }
    ```
    **注意**: `user` 字段需要一个有效的用户 ID。您可以通过 Django Admin 创建用户后获得。
-   Curl 示例:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"user": 1, "flight": 1, "seat_class": "economy", "seat_count": 2}' http://127.0.0.1:8000/api/bookings/
    ```

#### 2. 取消订座
-   URL: `/api/bookings/{id}/cancel/`
-   Method: `POST`
-   Curl 示例 (取消 id 为 1 的订单):
    ```bash
    curl -X POST http://127.0.0.1:8000/api/bookings/1/cancel/
    ```

#### 3. 查看所有订票记录（管理员权限）
- URL: `/booking/all_bookings/`
- Method: `POST`
- Body (JSON):
    ```json
    {
        "username": "admin",
        "password": "123456"
    }
    ```
    此时应给出一个管理员账号和密码才能读取全部用户的信息
- Curl 示例:
    ```bash
    curl -X POST  -H "Content-Type: application/json" -d '{"username": "admin","password": "123456"}' http://127.0.0.1:8000/booking/all_bookings/
    ```

#### 4. 根据多个属性值搜索订票记录（管理员权限）
- URL: `/booking/search/`
- Method: `POST`
- Body (JSON):
    ```json
    {
        "username": "admin",
        "password": "123456",
        "user": 1,
        "flight": 2,
        "seat_class": "economy",
        "seat_count": 2
    }
    ```
    此时应给出一个管理员账号和密码才能检索多个用户的订票信息
- Curl 示例:
    ```bash
    curl -X POST  -H "Content-Type: application/json" -d '{"username": "admin","password": "123456","user": 1,"flight": 2,"seat_class": "economy","seat_count": 2}' http://127.0.0.1:8000/booking/search/
