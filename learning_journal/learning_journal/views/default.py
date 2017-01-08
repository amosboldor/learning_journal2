"""."""


from pyramid.response import Response
from pyramid.view import view_config
from learning_journal.models import Entries
from pyramid.httpexceptions import HTTPFound
from datetime import date
from learning_journal.security import check_credentials
from pyramid.security import remember, forget
# from sqlalchemy.exc import DBAPIError


@view_config(route_name='list', renderer='../templates/list.jinja2')
def list_view(request):
    """."""
    try:
        query = request.dbsession.query(Entries).all()
        # one = query.filter(MyModel.name == 'one').first()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    return {'entries': query}


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entries).get(entry_id)
    return {'entry': entry}


@view_config(route_name='create', renderer='../templates/create.jinja2')
def create_view(request):
    """View for the create page."""
    if request.method == 'POST':
        entry = request.POST
        row = Entries(title=entry['title'], title1=entry['title1'], create_date=date.today(), body=entry['body'])
        request.dbsession.add(row)
        return HTTPFound(request.route_url('list'))
    return {}


@view_config(route_name='edit', renderer='../templates/edit.jinja2')
def edit_view(request):
    """View for the edit page."""
    entry_id = int(request.matchdict['id'])
    if request.method == 'POST':
        entry = request.POST
        query = request.dbsession.query(Entries).get(entry_id)
        query.title = entry['title']
        query.title1 = entry['title1']
        query.body = entry['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('list'))
    entry = request.dbsession.query(Entries).get(entry_id)
    return {'entry': entry}


@view_config(route_name="login", renderer="../templates/login.jinja2")
def login_view(request):
    """Login view."""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            auth_head = remember(request, username)
            return HTTPFound(request.route_url("list"),
                             headers=auth_head
                             )
    return {}


@view_config(route_name='logout')
def logout(request):
    """Logout view."""
    auth_head = forget(request)
    return HTTPFound(request.route_url('list'), headers=auth_head)


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""