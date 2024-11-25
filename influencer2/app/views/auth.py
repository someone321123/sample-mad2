from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import *
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            if current_user.__class__ == Influencer:
                return redirect(url_for('influencer.dashboard'))
            elif current_user.__class__ == Sponsor:
                return redirect(url_for('sponsor.dashboard'))
            elif current_user.__class__ == Admin:
                return redirect(url_for('admin.dashboard'))
        next_url = request.args.get('next','')
        return render_template('auth/login.html', next=next_url)

    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        remember = data.get('remember', False)
        next_url = data.get('next')
        print(next_url)
        user = Influencer.query.filter_by(username=username).first()

        if user and user.password == password:
            print(user._to_dict())
            print(user.flag)
            print("--------------")
            if user.flag == True:
                return jsonify(success=False, message='Flagged! Contact admins')
            login_user(user, remember=remember)
            return jsonify(success=True, next=(next_url or url_for('influencer.dashboard')), id=user.influencer_id)
            
        user = Sponsor.query.filter_by(username=username).first()

        if user and user.password == password:
            if user.flag == True:
                return jsonify(success=False, message='Flagged! Contact admins')
            login_user(user, remember=remember)
            return jsonify(success=True, next=(next_url or url_for('sponsor.dashboard')), id=user.sponsor_id)
        
        user = Admin.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user, remember=remember)
            return jsonify(success=True, next=(next_url or url_for('admin.dashboard')), id=user.admin_id)
        
        return jsonify(success=False, message='Invalid username or password')

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/register_sponsor')
def register_sponsor():
    logout_user()
    return render_template('auth/register_sponsor.html')

@auth_bp.route('/register_influencer')
def register_influencer():
    logout_user()
    return render_template('auth/register_influencer.html')
