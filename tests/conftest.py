"""
Pytest configuration and fixtures
"""
import pytest
import os
from app import create_app
from app.services.supabase import get_db_connection

@pytest.fixture
def app():
    """Create application for testing"""
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app('testing')
    
    app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
    })
    
    yield app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def auth_headers():
    """Create authentication headers"""
    return {
        'Authorization': 'Bearer test-token'
    }


class AuthActions:
    """Helper class for authentication in tests"""
    
    def __init__(self, client):
        self._client = client
    
    def login(self, email='test@example.com', password='password123'):
        return self._client.post(
            '/auth/login',
            data={'email': email, 'password': password}
        )
    
    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    """Authentication helper"""
    return AuthActions(client)
