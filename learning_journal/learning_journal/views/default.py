"""Main views for Learning Journal Blog app."""


# from pyramid.response import Response
from pyramid.view import view_config
from learning_journal.models import Entries
from pyramid.httpexceptions import HTTPFound
import datetime
from learning_journal.security import check_credentials
from pyramid.security import remember, forget


@view_config(route_name='list', renderer='../templates/list.jinja2')
def list_view(request):
    """A listing of expenses for the home page."""
    query = request.dbsession.query(Entries)
    entries = query.order_by(Entries.create_date.desc()).all()
    # print ("LISTING ENTRIES " + entries)
    # import pdb; pdb.set_trace()
    return {
        'entries': entries
    }


@view_config(route_name='detail', renderer='../templates/detail.jinja2')
def detail_view(request):
    """Detail page for entry in blog."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entries).get(entry_id)
    return {'entry': entry}


@view_config(
    route_name='create',
    renderer='../templates/create.jinja2',
    permission='add'
)
def create_view(request):
    """View for the create page."""
    if request.POST:
        entry = Entries(
            title=request.POST['title'],
            title1=request.POST['title1'],
            body=request.POST['body'],
            create_date=datetime.datetime.now()
        )
        request.dbsession.add(entry)
        return HTTPFound(request.route_url('list'))
    return {}


@view_config(
    route_name='edit',
    renderer='../templates/edit.jinja2',
    permission='add'
)
def edit_view(request):
    """View for the edit page."""
    entry_id = int(request.matchdict['id'])
    entry = request.dbsession.query(Entries).get(entry_id)
    if request.POST:
        entry.title = request.POST['title']
        entry.title1 = request.POST['title1']
        # entry.create_date = request.POST['create_date']
        entry.body = request.POST['body']
        request.dbsession.flush()
        return HTTPFound(request.route_url('list'))

    form_fill = {
        'title': entry.title,
        'title1': entry.title1,
        'body': entry.body
    }
    return {'data': form_fill}


@view_config(route_name="login", renderer="../templates/login.jinja2")
def login_view(request):
    """Login view."""
    if request.POST:
        print("I got the post, yay")
        username = request.POST["username"]
        password = request.POST["password"]
        if check_credentials(username, password):
            print("Password correct!")
            auth_head = remember(request, username)
            return HTTPFound(
                request.route_url("list"),
                headers=auth_head
            )
        else:
            print("You look shady, password isn't correct")
    return {}


@view_config(route_name='logout')
def logout(request):
    """Logout view."""
    auth_head = forget(request)
    return HTTPFound(request.route_url('list'), headers=auth_head)

# @forbidden_view_config(route_name="forbidden", renderer="../templates/forbidden.jinja2")
# def not_allowed_view(request):
#     return {}

# @notfound_view_config()


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
