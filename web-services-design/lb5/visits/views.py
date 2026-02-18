import csv
import io

from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import current_user

from db import get_db
from auth import check_rights, is_admin, can_view_logs

visits_bp = Blueprint('visits', __name__, url_prefix='/visits')

PER_PAGE = 10


def _user_label(row):
    """Return ФИО or 'Неаутентифицированный пользователь'."""
    parts = [row['last_name'], row['first_name'], row['middle_name']]
    name = ' '.join(p for p in parts if p)
    return name if name else 'Неаутентифицированный пользователь'


# ── Main log page (paginated) ─────────────────────────────────────────────────

@visits_bp.route('/')
@check_rights(can_view_logs)
def index():
    db  = get_db()
    page   = request.args.get('page', 1, type=int)
    offset = (page - 1) * PER_PAGE

    base_query = '''
        SELECT vl.id, vl.path,
               strftime('%d.%m.%Y %H:%M:%S', vl.created_at) AS created_at_fmt,
               u.last_name, u.first_name, u.middle_name
        FROM visit_logs vl
        LEFT JOIN users u ON vl.user_id = u.id
        {where}
        ORDER BY vl.created_at DESC
        LIMIT {limit} OFFSET {offset}
    '''
    count_query = 'SELECT COUNT(*) FROM visit_logs vl {where}'

    if current_user.is_admin:
        where = ''
        params_count = ()
        params_rows  = ()
    else:
        where = 'WHERE vl.user_id = ?'
        params_count = (current_user.id,)
        params_rows  = (current_user.id,)

    total = db.execute(count_query.format(where=where), params_count).fetchone()[0]
    logs  = db.execute(base_query.format(where=where, limit=PER_PAGE, offset=offset),
                       params_rows).fetchall()

    pages = max(1, (total + PER_PAGE - 1) // PER_PAGE)
    return render_template('visits/index.html',
                           title='Журнал посещений',
                           logs=logs, page=page, pages=pages, total=total,
                           user_label=_user_label)


# ── Pages report ──────────────────────────────────────────────────────────────

@visits_bp.route('/pages')
@check_rights(is_admin)
def pages_report():
    stats = get_db().execute('''
        SELECT path, COUNT(*) AS cnt
        FROM visit_logs
        GROUP BY path
        ORDER BY cnt DESC
    ''').fetchall()
    return render_template('visits/pages.html', title='Отчёт по страницам', stats=stats)


@visits_bp.route('/pages/export')
@check_rights(is_admin)
def pages_export():
    stats = get_db().execute('''
        SELECT path, COUNT(*) AS cnt
        FROM visit_logs
        GROUP BY path
        ORDER BY cnt DESC
    ''').fetchall()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['№', 'Страница', 'Количество посещений'])
    for i, row in enumerate(stats, 1):
        writer.writerow([i, row['path'], row['cnt']])

    response = make_response('\ufeff' + buf.getvalue())   # BOM for Excel UTF-8
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=pages_report.csv'
    return response


# ── Users report ──────────────────────────────────────────────────────────────

@visits_bp.route('/users')
@check_rights(is_admin)
def users_report():
    stats = get_db().execute('''
        SELECT vl.user_id, u.last_name, u.first_name, u.middle_name, COUNT(*) AS cnt
        FROM visit_logs vl
        LEFT JOIN users u ON vl.user_id = u.id
        GROUP BY vl.user_id
        ORDER BY cnt DESC
    ''').fetchall()
    return render_template('visits/users.html', title='Отчёт по пользователям',
                           stats=stats, user_label=_user_label)


@visits_bp.route('/users/export')
@check_rights(is_admin)
def users_export():
    stats = get_db().execute('''
        SELECT vl.user_id, u.last_name, u.first_name, u.middle_name, COUNT(*) AS cnt
        FROM visit_logs vl
        LEFT JOIN users u ON vl.user_id = u.id
        GROUP BY vl.user_id
        ORDER BY cnt DESC
    ''').fetchall()

    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(['№', 'Пользователь', 'Количество посещений'])
    for i, row in enumerate(stats, 1):
        parts = [row['last_name'], row['first_name'], row['middle_name']]
        name = ' '.join(p for p in parts if p) or 'Неаутентифицированный пользователь'
        writer.writerow([i, name, row['cnt']])

    response = make_response('\ufeff' + buf.getvalue())
    response.headers['Content-Type'] = 'text/csv; charset=utf-8'
    response.headers['Content-Disposition'] = 'attachment; filename=users_report.csv'
    return response
