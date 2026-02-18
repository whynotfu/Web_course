from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from models import db, Course, Category, User, Review
from tools import CoursesFilter, ImageSaver

bp = Blueprint('courses', __name__, url_prefix='/courses')

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

SORT_OPTIONS = {
    'newest':      Review.created_at.desc(),
    'oldest':      Review.created_at.asc(),
    'rating_desc': Review.rating.desc(),
    'rating_asc':  Review.rating.asc(),
}

def params():
    return { p: request.form.get(p) or None for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': [x for x in request.args.getlist('category_ids') if x],
    }

def _get_user_review(course_id):
    if not current_user.is_authenticated:
        return None
    return db.session.execute(
        db.select(Review).filter_by(course_id=course_id, user_id=current_user.id)
    ).scalar()

def _get_recent_reviews(course_id, limit=5):
    return db.session.execute(
        db.select(Review)
        .filter_by(course_id=course_id)
        .order_by(Review.created_at.desc())
        .limit(limit)
    ).scalars().all()


@bp.route('/')
def index():
    courses = CoursesFilter(**search_params()).perform()
    pagination = db.paginate(courses)
    courses = pagination.items
    categories = db.session.execute(db.select(Category)).scalars()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
@login_required
def new():
    course = Course()
    categories = db.session.execute(db.select(Category)).scalars()
    users = db.session.execute(db.select(User)).scalars()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users,
                           course=course)

@bp.route('/create', methods=['POST'])
@login_required
def create():
    f = request.files.get('background_img')
    img = None
    course = Course()
    try:
        if f and f.filename:
            img = ImageSaver(f).save()

        image_id = img.id if img else None
        course = Course(**params(), background_image_id=image_id)
        db.session.add(course)
        db.session.commit()
    except IntegrityError as err:
        flash(f'Возникла ошибка при записи данных в БД. Проверьте корректность введённых данных. ({err})', 'danger')
        db.session.rollback()
        categories = db.session.execute(db.select(Category)).scalars()
        users = db.session.execute(db.select(User)).scalars()
        return render_template('courses/new.html',
                            categories=categories,
                            users=users,
                            course=course)

    flash(f'Курс {course.name} был успешно добавлен!', 'success')

    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = db.get_or_404(Course, course_id)
    recent_reviews = _get_recent_reviews(course_id)
    user_review = _get_user_review(course_id)
    return render_template('courses/show.html',
                           course=course,
                           recent_reviews=recent_reviews,
                           user_review=user_review,
                           review_errors={},
                           form_rating=5,
                           form_text='')

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    course = db.get_or_404(Course, course_id)
    sort = request.args.get('sort', 'newest')
    order = SORT_OPTIONS.get(sort, Review.created_at.desc())

    query = db.select(Review).filter_by(course_id=course_id).order_by(order)
    pagination = db.paginate(query, per_page=5)
    reviews_list = pagination.items

    user_review = _get_user_review(course_id)
    return render_template('courses/reviews.html',
                           course=course,
                           reviews=reviews_list,
                           pagination=pagination,
                           sort=sort,
                           user_review=user_review,
                           review_errors={},
                           form_rating=5,
                           form_text='')

@bp.route('/<int:course_id>/reviews/create', methods=['POST'])
@login_required
def create_review(course_id):
    course = db.get_or_404(Course, course_id)

    user_review = _get_user_review(course_id)
    if user_review:
        flash('Вы уже оставляли отзыв к этому курсу.', 'warning')
        return redirect(url_for('courses.show', course_id=course_id))

    rating = request.form.get('rating', type=int)
    text = request.form.get('text', '').strip()
    redirect_to = request.form.get('redirect_to', 'show')

    errors = {}
    if rating is None or rating not in range(0, 6):
        errors['rating'] = 'Выберите оценку от 0 до 5.'
    if not text:
        errors['text'] = 'Введите текст отзыва.'

    if errors:
        flash('Пожалуйста, исправьте ошибки в форме.', 'danger')
        if redirect_to == 'reviews':
            sort = request.args.get('sort', 'newest')
            order = SORT_OPTIONS.get(sort, Review.created_at.desc())
            query = db.select(Review).filter_by(course_id=course_id).order_by(order)
            pagination = db.paginate(query, per_page=5)
            return render_template('courses/reviews.html',
                                   course=course,
                                   reviews=pagination.items,
                                   pagination=pagination,
                                   sort=sort,
                                   user_review=None,
                                   review_errors=errors,
                                   form_rating=rating,
                                   form_text=text)
        recent_reviews = _get_recent_reviews(course_id)
        return render_template('courses/show.html',
                               course=course,
                               recent_reviews=recent_reviews,
                               user_review=None,
                               review_errors=errors,
                               form_rating=rating,
                               form_text=text)

    review = Review(rating=rating, text=text,
                    course_id=course_id, user_id=current_user.id)
    course.rating_sum += rating
    course.rating_num += 1
    db.session.add(review)
    db.session.commit()

    flash('Ваш отзыв успешно добавлен!', 'success')
    return redirect(url_for('courses.show', course_id=course_id))
