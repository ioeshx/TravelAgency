# 🛫 机票服务系统 (Flight Ticket System)

一个功能完整的基于Django REST Framework的机票服务系统，支持航班管理、查询、订座等核心功能，提供现代化的Web界面和完整的RESTful API。

## 📊 项目状态

- ✅ **数据库迁移完成** - 所有表结构已创建
- ✅ **示例数据已创建** - 包含多个示例航班
- ✅ **服务器运行正常** - Django开发服务器已启动
- ✅ **前端界面完整** - 现代化Web界面
- ✅ **API接口完整** - 支持RESTful API调用
- ✅ **用户系统完善** - 注册、登录、权限控制

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Django 4.1.7
- Django REST Framework
- SQLite3

### 一键启动

```bash
# 1. 进入项目目录
cd backend

# 2. 安装依赖
pip install Django==4.1.7 djangorestframework

# 3. 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 4. 创建超级用户（可选）
python manage.py createsuperuser

# 5. 启动服务器
python manage.py runserver

# 6. 访问系统
# 网站首页: http://127.0.0.1:8000/
# 管理后台: http://127.0.0.1:8000/admin/
```

## 🎯 功能特性

### ✈️ 航班管理

- **航班搜索** - 支持出发地、目的地、出发时间多条件搜索
- **航班列表** - 分页显示，支持排序和筛选
- **航班详情** - 详细的航班信息展示
- **实时更新** - 支持航班信息的实时更新

### 🎫 订座功能

- **在线订座** - 简单易用的订座流程
- **多舱位支持** - 经济舱、商务舱、头等舱
- **座位管理** - 实时座位数量统计
- **订座记录** - 完整的订座历史管理
- **取消订座** - 灵活的取消机制

### 👤 用户系统

- **用户注册** - 安全的用户注册流程
- **登录/登出** - 会话管理
- **权限控制** - 基于角色的访问控制
- **个人中心** - 订座记录查看和管理

### 🌐 Web界面

- **响应式设计** - 支持桌面和移动设备
- **现代化UI** - Bootstrap 5 + 自定义样式
- **用户友好** - 直观的导航和操作流程
- **实时反馈** - 消息提示和状态更新

## 🛠️ 技术栈

### 后端技术

- **Python 3.8+** - 核心开发语言
- **Django 4.1.7** - Web框架
- **Django REST Framework** - API开发框架
- **SQLite3** - 数据库

### 前端技术

- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **Bootstrap 5** - 响应式框架
- **JavaScript** - 交互功能
- **Font Awesome** - 图标库

### 开发工具

- **Django Admin** - 管理后台
- **Django Debug Toolbar** - 调试工具
- **Django REST Framework** - API文档

## 📁 项目结构

```
flight-ticket/
├── backend/                          # 后端代码
│   ├── manage.py                     # Django管理脚本
│   ├── db.sqlite3                    # SQLite数据库
│   ├── flight_service/               # Django项目配置
│   │   ├── __init__.py
│   │   ├── settings.py               # 项目设置
│   │   ├── urls.py                  # 主URL配置
│   │   ├── wsgi.py                  # WSGI配置
│   │   └── asgi.py                  # ASGI配置
│   ├── flights/                      # 航班应用
│   │   ├── __init__.py
│   │   ├── models.py                # 数据模型
│   │   ├── views.py                 # 视图函数
│   │   ├── serializers.py           # 序列化器
│   │   ├── urls.py                  # 应用URL配置
│   │   └── migrations/              # 数据库迁移文件
│   ├── templates/                    # 模板文件
│   │   ├── base.html                # 基础模板
│   │   ├── index.html               # 首页
│   │   ├── flight_search.html       # 航班搜索
│   │   ├── flight_list.html         # 航班列表
│   │   ├── flight_detail.html       # 航班详情
│   │   ├── booking_form.html        # 订座表单
│   │   ├── booking_list.html        # 订座列表
│   │   ├── booking_confirm_cancel.html # 取消订座确认
│   │   ├── login.html               # 登录页面
│   │   └── register.html            # 注册页面
│   └── static/                      # 静态文件
│       └── css/
│           └── custom.css           # 自定义样式
├── docker-compose.yml               # Docker编排文件
├── dockerfile                       # Docker镜像文件
├── requirementx.txt                 # 项目依赖
└── readme.md                        # 项目说明文档
```

## 🗄️ 数据模型

### Flight (航班模型)

```python
- flight_number: 航班号 (CharField)
- departure_city: 出发地 (CharField)
- arrival_city: 目的地 (CharField)
- departure_time: 出发时间 (DateTimeField)
- arrival_time: 到达时间 (DateTimeField)
- airline: 航空公司 (CharField)
- aircraft_type: 飞机机型 (CharField)
- economy_seats: 经济舱座位数 (IntegerField)
- business_seats: 商务舱座位数 (IntegerField)
- first_seats: 头等舱座位数 (IntegerField)
- economy_price: 经济舱价格 (DecimalField)
- business_price: 商务舱价格 (DecimalField)
- first_price: 头等舱价格 (DecimalField)
```

### Booking (订座模型)

```python
- user: 用户 (ForeignKey)
- flight: 航班 (ForeignKey)
- seat_class: 舱位等级 (CharField)
- seat_count: 订座数量 (IntegerField)
- passenger_name: 乘客姓名 (CharField)
- passenger_id: 身份证号 (CharField)
- phone: 联系电话 (CharField)
- status: 订座状态 (CharField)
- booking_time: 订座时间 (DateTimeField)
```

## 🔌 API接口

### 航班相关API

#### 1. 获取所有航班

```bash
GET /api/flights/
curl.exe "http://127.0.0.1:8000/api/flights/"
```

#### 2. 航班搜索

```bash
GET /api/flights/search/?departure_city=北京&arrival_city=上海&departure_date=2025-10-01
curl.exe "http://127.0.0.1:8000/api/flights/search/?departure_city=北京&arrival_city=上海"
```

#### 3. 航班详情

```bash
GET /api/flights/{id}/
curl.exe "http://127.0.0.1:8000/api/flights/1/"
```

#### 4. 创建航班

```bash
POST /api/flights/
Content-Type: application/json

{
    "flight_number": "CA123",
    "departure_city": "Beijing",
    "arrival_city": "Shanghai",
    "departure_time": "2025-10-01T10:00:00Z",
    "arrival_time": "2025-10-01T12:00:00Z",
    "airline": "Air China",
    "aircraft_type": "Boeing 737",
    "economy_seats": 150,
    "economy_price": "800.00",
    "business_seats": 20,
    "business_price": "1600.00",
    "first_seats": 10,
    "first_price": "3200.00"
}
```

### 订座相关API

#### 1. 创建订座

```bash
POST /api/bookings/create/
Content-Type: application/json

{
    "flight_id": 1,
    "seat_class": "economy",
    "seat_count": 2,
    "passenger_name": "张三",
    "passenger_id": "123456789012345678",
    "phone": "13800138000"
}
```

#### 2. 获取订座记录

```bash
GET /api/bookings/
curl.exe "http://127.0.0.1:8000/api/bookings/"
```

## 💻 使用说明

### Web界面使用

#### 1. 首页功能

- **快速搜索** - 在首页直接搜索航班
- **功能导航** - 快速访问各个功能模块
- **系统介绍** - 了解系统功能特色

#### 2. 航班查询

- **多条件搜索** - 支持出发地、目的地、出发时间组合查询
- **结果展示** - 清晰的航班信息展示
- **价格对比** - 不同舱位价格对比

#### 3. 订座流程

- **选择航班** - 从搜索结果或列表中选择航班
- **填写信息** - 填写乘客信息和舱位选择
- **确认订座** - 确认订座信息并完成订座
- **管理订座** - 查看订座记录，取消不需要的订座

### 管理员功能

1. **访问管理后台**: http://127.0.0.1:8000/admin/
2. **添加航班信息**: 在管理后台添加新的航班
3. **管理用户**: 查看和管理用户账户
4. **订座记录**: 查看所有订座记录和统计信息

## 🧪 测试示例

### 使用PowerShell测试API

#### 1. 获取所有航班

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/flights/" -Method GET
```

#### 2. 搜索航班

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/flights/search/?departure_city=北京" -Method GET
```

#### 3. 创建航班

```powershell
$flightData = @{
    flight_number = "CA123"
    departure_city = "Beijing"
    arrival_city = "Shanghai"
    departure_time = "2025-10-01T10:00:00Z"
    arrival_time = "2025-10-01T12:00:00Z"
    airline = "Air China"
    aircraft_type = "Boeing 737"
    economy_seats = 150
    economy_price = "800.00"
    business_seats = 20
    business_price = "1600.00"
    first_seats = 10
    first_price = "3200.00"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/flights/" -Method POST -ContentType "application/json" -Body $flightData
```

#### 4. 创建订座

```powershell
$bookingData = @{
    flight_id = 1
    seat_class = "economy"
    seat_count = 2
    passenger_name = "张三"
    passenger_id = "123456789012345678"
    phone = "13800138000"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/bookings/create/" -Method POST -ContentType "application/json" -Body $bookingData
```

## 🐳 Docker支持

### 使用Docker运行

```bash
# 构建镜像
docker build -t flight-ticket .

# 运行容器
docker run -p 8000:8000 flight-ticket

# 使用docker-compose
docker-compose up -d
```

## 🔧 开发说明

### 代码结构

- **MVC架构** - 清晰的模型-视图-控制器分离
- **RESTful API** - 符合REST规范的API设计
- **响应式设计** - 支持多种设备访问
- **模块化开发** - 功能模块独立，易于维护

### 安全特性

- **CSRF保护** - 防止跨站请求伪造
- **用户认证** - 安全的用户登录系统
- **权限控制** - 基于角色的访问控制
- **数据验证** - 完整的输入数据验证

### 性能优化

- **数据库索引** - 优化查询性能
- **静态文件** - 静态资源优化
- **缓存机制** - 减少数据库查询
- **分页显示** - 大数据量分页处理

## 📝 更新日志

### v1.0.0 (2025-09-29)

- ✅ 完成基础功能开发
- ✅ 实现航班管理功能
- ✅ 实现订座功能
- ✅ 实现用户系统
- ✅ 完成API接口开发
- ✅ 完成前端界面开发
- ✅ 代码优化和清理

## 🚀 部署建议

### 生产环境配置

1. **数据库升级** - 使用PostgreSQL或MySQL
2. **安全加固** - 配置HTTPS、防火墙
3. **性能优化** - 使用Redis缓存、CDN加速
4. **监控告警** - 添加日志记录和错误监控
5. **负载均衡** - 使用Nginx反向代理
6. **容器化** - 使用Docker容器化部署

### 扩展功能

1. **支付集成** - 集成支付网关
2. **邮件通知** - 订座确认邮件
3. **短信通知** - 重要信息短信提醒
4. **移动端** - 开发移动端应用
5. **数据分析** - 用户行为分析
6. **多语言** - 国际化支持

![1759150869506](image/readme/1759150869506.pdf)**🎉 感谢使用机票服务系统！**

*专业的机票预订服务平台，为您提供便捷的航班查询和订座服务。*
