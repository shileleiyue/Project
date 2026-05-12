# 第五、六题统一代码（需安装 Flask, Flask-SQLAlchemy, PyMySQL）
# 文件名: app.py

from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

# ========== 初始化应用 ==========
app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 用于 session 保持登录状态
# 配置数据库（请修改为实际地址）
app.json.ensure_ascii = False   # 让 jsonify 不转义非 ASCII 字符
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hanlei.20060412@localhost/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== 实体类（Entity） ==========
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)   # 实际应加密，此处简化

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)

# 创建表（若不存在）
with app.app_context():
    db.create_all()
    # 插入一个测试用户（密码为明文，演示用）
    if not User.query.filter_by(username='admin').first():
        test_user = User(username='admin', password='admin')
        db.session.add(test_user)
        db.session.commit()
    # 插入一本测试书籍
    if not Book.query.filter_by(name='重生之这一次我一定要加入蓝旭').first():
        test_book = Book(name='重生之这一次我一定要加入蓝旭', author='bluemsun')
        db.session.add(test_book)
        db.session.commit()

# ========== 数据交互层（DAO） ==========
class UserDao:
    @staticmethod
    def get_user_by_username(username):
        """根据用户名查询用户"""
        return User.query.filter_by(username=username).first()

class BookDao:
    @staticmethod
    def get_book_by_id(book_id):
        """根据id查询书籍"""
        return Book.query.get(book_id)

# ========== 业务逻辑层（Service） ==========
class UserService:
    @staticmethod
    def login(username, password):
        """
        登录业务逻辑
        :return: (success: bool, message: str, user: User or None)
        """
        if not username or not password:
            return False, "用户名或密码不能为空", None
        user = UserDao.get_user_by_username(username)
        if not user:
            return False, "用户不存在", None
        if user.password != password:   # 实际应比较哈希值
            return False, "密码错误", None
        return True, "登录成功", user

# ========== 网络层（Controller / Route） ==========
@app.route('/user/login', methods=['POST'])
def login():
    """
    登录接口，接收 JSON 格式：
    {"username": "admin", "password": "admin"}
    返回 JSON：
    {"code": 200, "msg": "success"} 或 {"code": 500, "msg": "error"}
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"code": 500, "msg": "请求体必须是JSON格式"}), 400
        username = data.get('username')
        password = data.get('password')
        success, msg, user = UserService.login(username, password)
        if success:
            # 保持登录状态（进阶要求）：使用 Flask session
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({"code": 200, "msg": msg})
        else:
            return jsonify({"code": 500, "msg": msg})
    except Exception as e:
        return jsonify({"code": 500, "msg": f"服务器错误：{str(e)}"}), 500

# ========== 第六题：检索书籍接口 ==========
@app.route('/book/search', methods=['GET'])
def search_book():
    """
    根据 id 查找书籍，参数：id（query string）
    返回 JSON：
    {"code": 0, "msg": "检索成功", "data": {"id": "1", "name": "...", "author": "..."}}
    若失败，code非0，msg说明错误
    """
    book_id = request.args.get('id')
    if not book_id:
        return jsonify({"code": 1, "msg": "缺少参数 id"}), 400
    try:
        book_id = int(book_id)
    except ValueError:
        return jsonify({"code": 1, "msg": "id 必须是整数"}), 400

    book = BookDao.get_book_by_id(book_id)
    if not book:
        return jsonify({"code": 1, "msg": "书籍不存在"}), 404

    return jsonify({
        "code": 0,
        "msg": "检索成功",
        "data": {
            "id": str(book.id),
            "name": book.name,
            "author": book.author
        }
    })

# ========== 启动应用 ==========
if __name__ == '__main__':
    app.run(debug=True)