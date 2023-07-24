from flask_testing import TestCase
from main import app
from flask import current_app, url_for

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def test_app_exists(self):
        print("TESTING: existe app")
        self.assertIsNotNone(current_app)

    def test_app_in_test_mode(self):
        print("TESTING: app modo testing")
        self.assertTrue(current_app.config['TESTING'])

    """def test_index_redirects(self):
        print("TESTING: index redirecciona")
        response = self.client.get(url_for('Templates.inicio'))
        self.assertRedirects(response, url_for('Templates.hello'))"""

    def test_hello_get(self):
        print("TESTING: hello get")
        response = self.client.get(url_for('Templates.hello'))
        self.assert200(response)

    """def test_hello_post(self):
        fake_form = {
            'username': 'fake',
            'password': 'fake-password'
        }
        response = self.client.post(url_for('Templates.login_post'), data=fake_form)
        print(response.request.path)
        assert response.request.path == '/hello'"""
