import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'instance', 'novel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ------------------ 模型定义 ------------------
# 角色表
class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    alias = db.Column(db.String(80))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 关系
    relationships1 = db.relationship('Relationship', foreign_keys='Relationship.character1_id', backref='character1', lazy=True)
    relationships2 = db.relationship('Relationship', foreign_keys='Relationship.character2_id', backref='character2', lazy=True)
    events = db.relationship('EventCharacter', back_populates='character', lazy=True)

    def __repr__(self):
        return f'<Character {self.name}>'

# 关系表（无向，存储一次，约定 character1_id < character2_id）
class Relationship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    character1_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    character2_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    relation_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint('character1_id != character2_id', name='no_self_relation'),
    )

    @property
    def character_a(self):
        return Character.query.get(self.character1_id)

    @property
    def character_b(self):
        return Character.query.get(self.character2_id)

# 时间线事件表
class TimelineEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20))  # 存字符串便于灵活格式，建议 YYYY-MM-DD
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    characters = db.relationship('EventCharacter', back_populates='event', lazy=True)

# 事件-角色 多对多关联表
class EventCharacter(db.Model):
    event_id = db.Column(db.Integer, db.ForeignKey('timeline_event.id'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), primary_key=True)
    character = db.relationship('Character', back_populates='events')
    event = db.relationship('TimelineEvent', back_populates='characters')

# 科技树节点（自引用）
class TechNode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('tech_node.id'), nullable=True)
    children = db.relationship('TechNode', backref=db.backref('parent', remote_side=[id]), lazy=True)

# ------------------ 路由 ------------------
@app.route('/')
def index():
    char_count = Character.query.count()
    rel_count = Relationship.query.count()
    event_count = TimelineEvent.query.count()
    tech_count = TechNode.query.count()
    return render_template('index.html',
                           char_count=char_count,
                           rel_count=rel_count,
                           event_count=event_count,
                           tech_count=tech_count)

# ---------- 角色管理 ----------
@app.route('/characters')
def characters():
    chars = Character.query.order_by(Character.created_at.desc()).all()
    return render_template('characters.html', characters=chars)

@app.route('/character/add', methods=['GET', 'POST'])
def character_add():
    if request.method == 'POST':
        name = request.form['name']
        alias = request.form.get('alias', '')
        gender = request.form.get('gender', '')
        age = request.form.get('age', type=int)
        desc = request.form.get('description', '')
        char = Character(name=name, alias=alias, gender=gender, age=age, description=desc)
        db.session.add(char)
        db.session.commit()
        flash('角色添加成功', 'success')
        return redirect(url_for('characters'))
    return render_template('character_form.html', character=None)

@app.route('/character/edit/<int:char_id>', methods=['GET', 'POST'])
def character_edit(char_id):
    char = Character.query.get_or_404(char_id)
    if request.method == 'POST':
        char.name = request.form['name']
        char.alias = request.form.get('alias', '')
        char.gender = request.form.get('gender', '')
        char.age = request.form.get('age', type=int)
        char.description = request.form.get('description', '')
        db.session.commit()
        flash('角色更新成功', 'success')
        return redirect(url_for('characters'))
    return render_template('character_form.html', character=char)

@app.route('/character/delete/<int:char_id>')
def character_delete(char_id):
    char = Character.query.get_or_404(char_id)
    # 删除关联的关系、事件关联（外键级联未设置，手动处理）
    Relationship.query.filter(
        (Relationship.character1_id == char_id) | (Relationship.character2_id == char_id)
    ).delete()
    EventCharacter.query.filter_by(character_id=char_id).delete()
    db.session.delete(char)
    db.session.commit()
    flash('角色已删除', 'success')
    return redirect(url_for('characters'))

# ---------- 关系管理 ----------
@app.route('/relationships')
def relationships():
    rels = Relationship.query.all()
    return render_template('relationships.html', relationships=rels)

@app.route('/relationship/add', methods=['GET', 'POST'])
def relationship_add():
    if request.method == 'POST':
        char1_id = request.form['character1_id']
        char2_id = request.form['character2_id']
        rel_type = request.form['relation_type']
        desc = request.form.get('description', '')
        # 保证小id在前，避免重复方向
        if int(char1_id) > int(char2_id):
            char1_id, char2_id = char2_id, char1_id
        # 检查是否已存在相同关系（可选）
        existing = Relationship.query.filter_by(character1_id=char1_id, character2_id=char2_id).first()
        if existing:
            flash('这两个角色之间已经存在关系', 'danger')
        else:
            rel = Relationship(character1_id=char1_id, character2_id=char2_id, relation_type=rel_type, description=desc)
            db.session.add(rel)
            db.session.commit()
            flash('关系添加成功', 'success')
        return redirect(url_for('relationships'))
    characters = Character.query.order_by(Character.name).all()
    return render_template('relationship_form.html', relationship=None, characters=characters)

@app.route('/relationship/edit/<int:rel_id>', methods=['GET', 'POST'])
def relationship_edit(rel_id):
    rel = Relationship.query.get_or_404(rel_id)
    if request.method == 'POST':
        char1_id = request.form['character1_id']
        char2_id = request.form['character2_id']
        if int(char1_id) > int(char2_id):
            char1_id, char2_id = char2_id, char1_id
        rel.character1_id = char1_id
        rel.character2_id = char2_id
        rel.relation_type = request.form['relation_type']
        rel.description = request.form.get('description', '')
        db.session.commit()
        flash('关系更新成功', 'success')
        return redirect(url_for('relationships'))
    characters = Character.query.order_by(Character.name).all()
    return render_template('relationship_form.html', relationship=rel, characters=characters)

@app.route('/relationship/delete/<int:rel_id>')
def relationship_delete(rel_id):
    rel = Relationship.query.get_or_404(rel_id)
    db.session.delete(rel)
    db.session.commit()
    flash('关系已删除', 'success')
    return redirect(url_for('relationships'))

# ---------- 时间线事件 ----------
@app.route('/timeline')
def timeline():
    events = TimelineEvent.query.order_by(TimelineEvent.date).all()
    return render_template('timeline.html', events=events)

@app.route('/timeline/add', methods=['GET', 'POST'])
def timeline_add():
    if request.method == 'POST':
        title = request.form['title']
        date = request.form.get('date', '')
        desc = request.form.get('description', '')
        event = TimelineEvent(title=title, date=date, description=desc)
        db.session.add(event)
        db.session.flush()  # 获取id
        # 处理关联角色
        char_ids = request.form.getlist('characters')
        for cid in char_ids:
            ec = EventCharacter(event_id=event.id, character_id=int(cid))
            db.session.add(ec)
        db.session.commit()
        flash('事件添加成功', 'success')
        return redirect(url_for('timeline'))
    characters = Character.query.order_by(Character.name).all()
    return render_template('timeline_form.html', event=None, characters=characters)

@app.route('/timeline/edit/<int:event_id>', methods=['GET', 'POST'])
def timeline_edit(event_id):
    event = TimelineEvent.query.get_or_404(event_id)
    if request.method == 'POST':
        event.title = request.form['title']
        event.date = request.form.get('date', '')
        event.description = request.form.get('description', '')
        # 更新关联角色
        EventCharacter.query.filter_by(event_id=event.id).delete()
        char_ids = request.form.getlist('characters')
        for cid in char_ids:
            ec = EventCharacter(event_id=event.id, character_id=int(cid))
            db.session.add(ec)
        db.session.commit()
        flash('事件更新成功', 'success')
        return redirect(url_for('timeline'))
    characters = Character.query.order_by(Character.name).all()
    selected_char_ids = [ec.character_id for ec in event.characters]
    return render_template('timeline_form.html', event=event, characters=characters, selected=selected_char_ids)

@app.route('/timeline/delete/<int:event_id>')
def timeline_delete(event_id):
    event = TimelineEvent.query.get_or_404(event_id)
    EventCharacter.query.filter_by(event_id=event.id).delete()
    db.session.delete(event)
    db.session.commit()
    flash('事件已删除', 'success')
    return redirect(url_for('timeline'))

# ---------- 科技树 ----------
def build_tree(nodes, parent_id=None):
    """递归构建树形结构"""
    tree = []
    for node in nodes:
        if node.parent_id == parent_id:
            children = build_tree(nodes, node.id)
            node.children_list = children
            tree.append(node)
    return tree

@app.route('/tech_tree')
def tech_tree():
    nodes = TechNode.query.all()
    tree = build_tree(nodes)
    return render_template('tech_tree.html', tree=tree)

@app.route('/tech/add', methods=['GET', 'POST'])
def tech_add():
    if request.method == 'POST':
        name = request.form['name']
        desc = request.form.get('description', '')
        parent_id = request.form.get('parent_id')
        parent_id = int(parent_id) if parent_id and parent_id != '' else None
        node = TechNode(name=name, description=desc, parent_id=parent_id)
        db.session.add(node)
        db.session.commit()
        flash('科技节点添加成功', 'success')
        return redirect(url_for('tech_tree'))
    parents = TechNode.query.all()
    return render_template('tech_form.html', node=None, parents=parents)

@app.route('/tech/edit/<int:node_id>', methods=['GET', 'POST'])
def tech_edit(node_id):
    node = TechNode.query.get_or_404(node_id)
    if request.method == 'POST':
        node.name = request.form['name']
        node.description = request.form.get('description', '')
        parent_id = request.form.get('parent_id')
        node.parent_id = int(parent_id) if parent_id and parent_id != '' else None
        db.session.commit()
        flash('科技节点更新成功', 'success')
        return redirect(url_for('tech_tree'))
    parents = TechNode.query.filter(TechNode.id != node.id).all()  # 避免自循环
    return render_template('tech_form.html', node=node, parents=parents)

@app.route('/tech/delete/<int:node_id>')
def tech_delete(node_id):
    node = TechNode.query.get_or_404(node_id)
    # 将子节点的parent_id置空
    for child in node.children:
        child.parent_id = None
    db.session.delete(node)
    db.session.commit()
    flash('科技节点已删除', 'success')
    return redirect(url_for('tech_tree'))

# ------------------ 启动前创建表 ------------------
with app.app_context():
    import os
    instance_dir = os.path.join(app.root_path, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)