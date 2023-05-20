# blog/routes.py

from flask import render_template, request, session, flash, redirect, url_for
from . import app, db
from .forms import EntryForm, LoginForm
from .models import Entry, db, Post
import functools

@app.route("/homepage/", methods=['GET'])
def homepage():
    return render_template("homepage.html")

def login_required(view_func):
   @functools.wraps(view_func)
   def check_permissions(*args, **kwargs):
       if session.get('logged_in'):
           return view_func(*args, **kwargs)
       return redirect(url_for('login', next=request.path))
   return check_permissions

@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('base.html', posts=posts)

@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def create_or_edit_entry(entry_id=None):
    if entry_id:
        entry = Entry.query.get_or_404(entry_id)
        form = EntryForm(obj=entry)
    else:
        entry = None
        form = EntryForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if entry:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)

            db.session.commit()
            return redirect(url_for('index'))

    return render_template("entry_form.html", form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
   form = LoginForm()
   errors = None
   next_url = request.args.get('next')
   if request.method == 'POST':
       if form.validate_on_submit():
           session['logged_in'] = True
           session.permanent = True  # Use cookie to store session.
           flash('You are now logged in.', 'success')
           return redirect(next_url or url_for('index'))
       else:
           errors = form.errors
   return render_template("login_form.html", form=form, errors=errors)

@app.route('/logout/', methods=['GET', 'POST'])
def logout():
   if request.method == 'POST':
       session.clear()
       flash('You are now logged out.', 'success')
   return redirect(url_for('index'))

@app.route("/drafts/", methods=['GET'])
@login_required
def list_drafts():
   drafts = Entry.query.filter_by(is_published=False).order_by(Entry.pub_date.desc())
   return render_template("drafts.html", drafts=drafts)


@app.route("/delete-post/<int:entry_id>", methods=["POST"])
@login_required
def delete_entry(entry_id):
    entry = Entry.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash('The entry has been deleted.', 'success')
    return redirect(url_for('index'))