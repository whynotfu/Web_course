from app import app
from models import db, User, Category, Course, Review

with app.app_context():
    # Пользователи
    admin = User(login='admin', first_name='Алексей', last_name='Иванов')
    admin.set_password('admin123')

    user2 = User(login='user2', first_name='Мария', last_name='Петрова')
    user2.set_password('user2123')

    user3 = User(login='user3', first_name='Дмитрий', last_name='Сидоров')
    user3.set_password('user3123')

    db.session.add_all([admin, user2, user3])
    db.session.commit()

    # Категории
    cat1 = Category(name='Программирование')
    cat2 = Category(name='Математика')
    cat3 = Category(name='Языкознание')
    db.session.add_all([cat1, cat2, cat3])
    db.session.commit()

    # Курсы
    course1 = Course(
        name='Python для начинающих',
        short_desc='Основы языка Python: синтаксис, функции, ООП.',
        full_desc='Полный курс по Python с нуля. Подходит для тех, кто только начинает программировать. '
                  'Вы изучите синтаксис, структуры данных, функции, классы и работу с файлами.',
        category_id=cat1.id,
        author_id=admin.id,
        rating_sum=0,
        rating_num=0,
    )
    course2 = Course(
        name='Линейная алгебра',
        short_desc='Матрицы, векторы, линейные преобразования.',
        full_desc='Курс охватывает основы линейной алгебры: матрицы, определители, собственные значения и векторы.',
        category_id=cat2.id,
        author_id=user2.id,
        rating_sum=0,
        rating_num=0,
    )
    course3 = Course(
        name='Английский для начинающих',
        short_desc='Базовая грамматика и лексика английского языка.',
        full_desc='Курс для тех, кто только начинает изучать английский язык. Грамматика, произношение, базовые диалоги.',
        category_id=cat3.id,
        author_id=admin.id,
        rating_sum=0,
        rating_num=0,
    )
    db.session.add_all([course1, course2, course3])
    db.session.commit()

    # Отзывы к первому курсу
    reviews = [
        Review(rating=5, text='Отличный курс, всё очень понятно объяснено!',
               course_id=course1.id, user_id=user2.id),
        Review(rating=4, text='Хороший материал, но хотелось бы больше практики.',
               course_id=course1.id, user_id=user3.id),
    ]
    for r in reviews:
        course1.rating_sum += r.rating
        course1.rating_num += 1
    db.session.add_all(reviews)

    # Отзыв ко второму курсу
    r3 = Review(rating=3, text='Неплохо, но местами слишком поверхностно.',
                course_id=course2.id, user_id=admin.id)
    course2.rating_sum += r3.rating
    course2.rating_num += 1
    db.session.add(r3)

    db.session.commit()
    print('Готово! Данные добавлены.')
    print('Логины: admin/admin123  user2/user2123  user3/user3123')
