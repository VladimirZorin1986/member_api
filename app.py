from flask import Flask, g, request, jsonify
from database import get_db
from authorization import authorized

app = Flask(__name__)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite3_db'):
        g.sqlite3_db.close()


@app.route('/member', methods=['GET'])
@authorized
def get_members():
    db = get_db()
    members_cur = db.execute('select id, name, email, level from members')
    members = members_cur.fetchall()

    return jsonify({'members': [{'id': member['id'], 'name': member['name'],
                                 'email': member['email'], 'level': member['level']}
                                for member in members]})


@app.route('/member/<int:member_id>', methods=['GET'])
@authorized
def get_member(member_id):
    db = get_db()
    member_cur = db.execute('select id, name, email, level from members where id = ?', [member_id])
    member = member_cur.fetchone()
    return jsonify({'member': {'id': member['id'], 'name': member['name'],
                               'email': member['email'], 'level': member['level']}})


@app.route('/member', methods=['POST'])
@authorized
def add_member():
    new_member_data = request.get_json()
    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute('insert into members (name, email, level) values (?, ?, ?)',
               [name, email, level])
    db.commit()

    member_cur = db.execute('select id, name, email, level from members where name = ?', [name])
    new_member = member_cur.fetchone()

    return jsonify({'member': {'id': new_member['id'], 'name': new_member['name'],
                    'email': new_member['email'], 'level': new_member['level']}})


@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
@authorized
def edit_member(member_id):
    edit_member_data = request.get_json()
    name = edit_member_data['name']
    email = edit_member_data['email']
    level = edit_member_data['level']
    db = get_db()
    db.execute('update members set name = ?, email = ?, level = ? where id = ?',
               [name, email, level, member_id])
    db.commit()

    edit_member_cur = db.execute('select id, name, email, level from members where id = ?', [member_id])
    member = edit_member_cur.fetchone()

    return jsonify({'member': {'id': member['id'], 'name': member['name'],
                               'email': member['email'], 'level': member['level']}})


@app.route('/member/<int:member_id>', methods=['DELETE'])
@authorized
def delete_member(member_id):
    db = get_db()
    db.execute('delete from members where id = ?', [member_id])
    db.commit()
    return jsonify({'message': 'The member has been deleted!'})

