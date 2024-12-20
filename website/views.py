from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML 

        if len(note) < 1:
            flash('Note is too short!', category='error') 
        else:
            new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note 
            db.session.add(new_note) #adding the note to the database 
            db.session.commit()
            flash('Note added!', category='success')

    return render_template("notes.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/update-password', methods=['POST'])
def update_password():
    data = request.get_json()
    if not data or not data.get('value'):
        return jsonify({'success': False, 'message': 'No email provided.'}), 400

    user = User.query.get(1)  # Replace with your user identification logic
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    user.email = data['value']
    db.session.commit()
    return jsonify({'success': True, 'message': 'Email updated successfully.'})


@views.route('/update-email', methods=['POST'])
def update_email():
    data = request.get_json()
    if not data or not data.get('value'):
        return jsonify({'success': False, 'message': 'No email provided.'}), 400

    user = User.query.get(1)  # Replace with your user identification logic
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    user.email = data['value']
    db.session.commit()
    return jsonify({'success': True, 'message': 'Email updated successfully.'})

@views.route('/update-username', methods=['POST'])
def update_username():
    data = request.get_json()
    if not data or not data.get('value'):
        return jsonify({'success': False, 'message': 'No username provided.'}), 400

    user = User.query.get(1)  # Replace with your user identification logic
    if not user:
        return jsonify({'success': False, 'message': 'User not found.'}), 404

    user.username = data['value']
    db.session.commit()
    return jsonify({'success': True, 'message': 'Username updated successfully.'})