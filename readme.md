
### 项目技术栈
后端 python+django 
数据库 sqlite3
前端

### 安装 SQLite
要在 Windows 上安装 SQLite，可以按照以下步骤操作：
2. 从 [SQLite官网](https://sqlite.org/download.html) 官网下载两个安装包[DLL](https://sqlite.org/2025/sqlite-dll-win-arm64-3500400.zip) 
和[exe](https://sqlite.org/2025/sqlite-tools-win-arm64-3500400.zip)。
3. 将两个压缩包解压到 C:\sqlite3 目录。
4. 右键点击“此电脑”，选择“属性”，然后点击“高级系统设置”。
5. 在“环境变量”中，编辑 Path 变量，添加 C:\sqlite3 路径，并将其移动到第一位。
6. 打开命令提示符（Win + R，输入 cmd），进入 C:\sqlite3 目录，输入 sqlite3 以验证安装是否成功。