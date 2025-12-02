from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm
import logging

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')


@app.route('/')
def resume():
    return render_template('resume.html', title='Резюме')


@app.route('/contacts', methods=['GET', 'POST'])
def contacts():
    form = ContactForm()

    if form.validate_on_submit():
        log_message = f"User: {form.name.data}, Email: {form.email.data}, Subject: {form.subject.data}"
        logging.info(log_message)

        flash(f"Повідомлення від {form.name.data} ({form.email.data}) успішно надіслано!", "success")

        return redirect(url_for('contacts'))

    return render_template('contacts.html', title='Контакти', form=form)
