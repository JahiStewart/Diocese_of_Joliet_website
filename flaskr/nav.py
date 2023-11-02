from flask_nav import Nav
from flask_nav.elements import Navbar, View

nav = Nav()

# registers the "top" menubar
@nav.navigation()
def mynavbar():
    return Navbar(
        'Navbar',
        View('Home', 'index'),
        View('Register', 'auth.register'),
        View('Login', 'auth.login'),
    )

def init_app(app):
    nav.init_app(app)



