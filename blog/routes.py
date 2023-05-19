# blog/routes.py

from flask import render_template, request, redirect, url_for
from . import app, db
from .forms import EntryForm
from .models import Entry

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