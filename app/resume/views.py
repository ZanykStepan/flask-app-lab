from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from .models import Resume, Category
from .forms import ResumeForm

resume_bp = Blueprint('resume', __name__, template_folder='templates/resume')


@resume_bp.route('/', methods=['GET'])
def list_resumes():
    search_query = request.args.get('q', '')
    query = Resume.query
    if search_query:
        query = query.filter(Resume.title.contains(search_query) | Resume.description.contains(search_query))

    sort_by = request.args.get('sort', 'date_desc')
    if sort_by == 'date_asc':
        query = query.order_by(Resume.created_at.asc())
    elif sort_by == 'title':
        query = query.order_by(Resume.title.asc())
    else:
        query = query.order_by(Resume.created_at.desc())

    resumes = query.all()
    return render_template('list.html', resumes=resumes, search_query=search_query)


@resume_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_resume():
    form = ResumeForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        resume = Resume(
            title=form.title.data,
            skills=form.skills.data,
            description=form.description.data,
            category_id=form.category.data,
            owner=current_user
        )
        db.session.add(resume)
        db.session.commit()
        flash('Резюме успішно створено!', 'success')
        return redirect(url_for('resume.list_resumes'))

    return render_template('form.html', form=form, title="Створити резюме")


@resume_bp.route('/<int:id>')
def detail_resume(id):
    resume = db.get_or_404(Resume, id)
    return render_template('detail.html', resume=resume)


@resume_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_resume(id):
    resume = db.get_or_404(Resume, id)
    if resume.owner != current_user:
        abort(403)

    form = ResumeForm(obj=resume)
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        form.populate_obj(resume)
        resume.category_id = form.category.data
        db.session.commit()
        flash('Резюме оновлено!', 'success')
        return redirect(url_for('resume.detail_resume', id=resume.id))

    return render_template('form.html', form=form, title="Редагувати резюме")


@resume_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_resume(id):
    resume = db.get_or_404(Resume, id)
    if resume.owner != current_user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(resume)
        db.session.commit()
        flash('Резюме успішно видалено.', 'info')
        return redirect(url_for('resume.list_resumes'))
    return render_template('delete_resume_confirm.html', resume=resume)