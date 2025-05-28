# wrmp - Where Are My People

This is a recruitment assignment for Vatix consisting of a fairly simple API written in Django and Django REST Framework.

# Setup
`wrmp` is easiest to install using [uv](https://docs.astral.sh/uv/#installation).

1. Clone the repo.
2. Use `uv sync` to install dependencies.
3. Run `uv run manage.py migrate`
    1. If you end up setting `DEBUG` to `False` in `settings.py`, don't forget to set `ALLOWED_HOSTS` as well.
4. Use `uv run manage.py runserver` to run the app.

# If I had more time, I would fix/add:
- That one horrible try/catch lookup in the AssignDevice view.
- A WSGI server (since [the Django team is in the business of making Web Frameworks, not Web servers](https://docs.djangoproject.com/en/1.8/ref/django-admin/#runserver-port-or-address-port))
- Tests
- Typing
