from flask import render_template, redirect, url_for, flash, request, abort, session
from . import posts_bp
from app import db
from .models import Post
from .forms import PostForm


@posts_bp.route('/')
def get_posts():
    posts = db.session.query(Post).order_by(Post.posted.desc()).all()
    return render_template('posts.html', posts=posts, title='Всі пости')


@posts_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post, title=post.title)


@posts_bp.route('/create', methods=['GET', 'POST'])
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            posted=form.publish_date.data,
            is_active=form.is_active.data,
            author=session.get('username', 'Anonymous')
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f"Пост '{new_post.title}' успішно створено!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template('add_post.html', form=form, title='Створити пост')


@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    if request.method == 'GET':
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        form.populate_obj(post)
        post.posted = form.publish_date.data
        db.session.commit()
        flash("Пост оновлено!", "success")
        return redirect(url_for('posts.detail_post', id=post.id))

    return render_template('add_post.html', form=form, title='Редагувати пост')


@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)

    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Пост видалено.", "danger")
        return redirect(url_for('posts.get_posts'))

    return render_template('delete_resume_confirm.html', post=post)