# 第四题：MySQL 事务操作，演示提交和回滚

import pymysql
from pymysql import Error

# 数据库连接配置（请根据实际情况修改）
DB_CONFIG = {
    'host': 'localhost',
    'user': 'shileleiyue',
    'password': 'hanlei.20060412',
    'database': 'test_db',
    'charset': 'utf8mb4'
}

def create_table_if_not_exists(connection):
    """创建 products 表（如果不存在）"""
    create_sql = """
    CREATE TABLE IF NOT EXISTS products (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(100),
        price DECIMAL(10,2),
        stock INT
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(create_sql)
    connection.commit()

def insert_three_records_with_transaction(connection):
    """
    开启事务，插入三条记录，故意插入第四条重复主键导致失败，验证回滚。
    如果全部成功则提交，否则回滚。
    """
    try:
        connection.begin()   # 开启事务

        with connection.cursor() as cursor:
            # 插入三条正常记录
            cursor.execute("INSERT INTO products (name, price, stock) VALUES ('商品A', 49.90, 100)")
            cursor.execute("INSERT INTO products (name, price, stock) VALUES ('商品B', 88.00, 50)")
            cursor.execute("INSERT INTO products (name, price, stock) VALUES ('商品C', 120.00, 30)")

            # 故意插入一条主键重复的记录（id=1，可能已经存在或自增后冲突）
            # 为了确保失败，我们直接指定一个已经存在的 id（比如99，但为了确定，先查询最大id）
            cursor.execute("SELECT MAX(id) FROM products")
            max_id = cursor.fetchone()[0] or 0
            # 插入一个重复的主键（新插入的自增id不会重复，但手动指定已存在的id就会失败）
            # 下面这行会引发 IntegrityError（如果 max_id+1 不存在，我们就用 max_id 本身）
            duplicate_id = max_id if max_id > 0 else 1
            cursor.execute(f"INSERT INTO products (id, name, price, stock) VALUES ({duplicate_id}, '重复商品', 10, 1)")
            # 如果上面语句没有抛异常（例如表为空时 max_id=0，duplicate_id=1，表中无id=1，就不报错）
            # 为了确保失败，可以故意使用一个很大但冲突的值，更可靠的方法是先插入一条正常数据再用相同id插入
            # 简化演示：直接尝试插入一个已知会冲突的id（比如99），如果没有则先插入一条再冲突
            # 这里采用更通用的模拟：插入三条后，再尝试插入 id=1（如果已有id=1则失败）
            cursor.execute("INSERT INTO products (id, name, price, stock) VALUES (1, '冲突商品', 1, 1)")
            # 如果表已有id=1的记录，上面会报错；如果没有，则插入成功，但我们需要模拟失败场景。
            # 为了让回滚必定发生，我们可以在最后故意制造一个除零错误或语法错误：
            # raise Exception("模拟异常")   # 取消注释可强制回滚
            # 但根据题意“第四条插入重复主键导致失败”，更标准做法是确保存在 id=1 的记录。
            # 所以我们先插入一条 id=1 的记录（如果不存在），然后再重复插入它。
            # 为清晰，重构如下：
        # 更好的实现见下面代码注释中的改进版本
    except Error as e:
        print(f"数据库错误，执行回滚：{e}")
        connection.rollback()
    except Exception as e:
        print(f"其他错误，执行回滚：{e}")
        connection.rollback()
    else:
        connection.commit()
        print("插入成功，事务已提交")

# 更规范的事务插入示例（确保冲突发生）：
def insert_with_conflict(conn):
    """向 products 表中插入数据，模拟主键冲突导致回滚"""
    try:
        conn.begin()
        with conn.cursor() as cur:
            # 1. 先确保有一条 id=1 的记录（用于产生冲突）
            cur.execute("SELECT id FROM products WHERE id=1")
            if not cur.fetchone():
                cur.execute("INSERT INTO products (id, name, price, stock) VALUES (1, '初始商品', 10, 10)")
            # 2. 插入三条新记录（不指定id，自增）
            cur.execute("INSERT INTO products (name, price, stock) VALUES ('商品A', 49.90, 100)")
            cur.execute("INSERT INTO products (name, price, stock) VALUES ('商品B', 88.00, 50)")
            cur.execute("INSERT INTO products (name, price, stock) VALUES ('商品C', 120.00, 30)")
            # 3. 故意插入重复主键 id=1，导致失败
            cur.execute("INSERT INTO products (id, name, price, stock) VALUES (1, '重复商品', 999, 0)")
        conn.commit()
    except Error as e:
        print(f"插入过程发生错误，已回滚：{e}")
        conn.rollback()

def query_price_gt_50(connection):
    """查询所有价格 > 50 的商品并打印"""
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name, price, stock FROM products WHERE price > 50")
        rows = cursor.fetchall()
        print("价格大于50的商品：")
        for row in rows:
            print(f"id={row[0]}, name={row[1]}, price={row[2]}, stock={row[3]}")

def update_stock_add_10_with_transaction(connection):
    """事务：将所有商品的 stock 增加 10，提交前可回滚演示"""
    try:
        connection.begin()
        with connection.cursor() as cursor:
            cursor.execute("UPDATE products SET stock = stock + 10")
        # 模拟一个可选条件：如果希望回滚，可以在此处 raise
        # raise Exception("模拟异常，回滚更新")
        connection.commit()
        print("所有商品的 stock 已增加 10，事务提交")
    except Exception as e:
        print(f"更新 stock 发生错误，已回滚：{e}")
        connection.rollback()

# 主程序演示（需要先建立数据库和表）
if __name__ == "__main__":
    try:
        conn = pymysql.connect(**DB_CONFIG)
        create_table_if_not_exists(conn)
        # 清空表（可选，便于测试）
        with conn.cursor() as cur:
            cur.execute("DELETE FROM products")
        conn.commit()

        # 1. 事务插入（模拟冲突回滚）
        insert_with_conflict(conn)  # 此操作会因为冲突而回滚，所以最终表里可能没有那三条记录

        # 为了后续查询有数据，单独插入几条有效数据（非事务方式）
        with conn.cursor() as cur:
            cur.execute("INSERT INTO products (name, price, stock) VALUES ('笔记本', 4999, 10), ('鼠标', 88, 50), ('键盘', 199, 30)")
        conn.commit()

        # 2. 查询价格 > 50 的商品
        query_price_gt_50(conn)

        # 3. 使用事务将 stock 全部增加 10
        update_stock_add_10_with_transaction(conn)

        # 再次查询验证 stock 变化
        with conn.cursor() as cur:
            cur.execute("SELECT name, stock FROM products")
            print("更新后的库存：", cur.fetchall())

    except Error as e:
        print(f"连接数据库失败：{e}")
    finally:
        if 'conn' in locals() and conn.open:
            conn.close()