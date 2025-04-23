import pytest
from unittest.mock import MagicMock
from src.controllers.controller import Controller
from src.controllers.usercontroller import UserController
from src.util.dao import DAO

@pytest.fixture
def mock_dao():
    return MagicMock(spec=DAO)

@pytest.fixture
def user_controller(mock_dao):
    return UserController(dao=mock_dao)

def test_valid_email_single_user(user_controller, mock_dao):
    mock_user = {'email' : 'valid@domain.com'}
    mock_dao.find.return_value = [mock_user]
    result = user_controller.get_user_by_email('valid@domain.com')
    assert result == mock_user

def test_valid_email_multiple_users(user_controller, mock_dao, capsys):
    users = [{'email' : 'valid@domain.com'}, {'email' : 'valid@domain.com'}]
    mock_dao.find.return_value = users
    result1 = user_controller.get_user_by_email('valid@domain.com')
    captured = capsys.readouterr()
    assert 'more than one user' in captured.out
    assert result1 == users[0]

def test_valid_email_no_user_found(user_controller, mock_dao):
    mock_dao.find.return_value = []
    result2 = user_controller.get_user_by_email('valid@domain.com')
    assert result2 is None

def tes_invalid_email_raises_value_error(users_controller):
    with pytest.raises(ValueError):
        user_controller.get_user_by_email('invalidemail')

def test_dao_exception_raises_exception(user_controller, mock_dao):
    mock_dao.find.side_effect = Exception("DB error")
    with pytest.raises(Exception) as excinfo:
        user_controller.get_user_by_email('valid@domain.com')
    assert "DB error" in str(excinfo.value)