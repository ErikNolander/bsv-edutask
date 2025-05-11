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

#changed from using two asserts to using one assert (def 1)
def test_valid_email_multiple_users_logs_warning(user_controller, mock_dao, capsys):
    users = [{'email' : 'valid@domain.com'}, {'email' : 'valid@domain.com'}]
    mock_dao.find.return_value = users
    user_controller.get_user_by_email('valid@domain.com')
    captured = capsys.readouterr()
    assert 'more than one user' in captured.out
#def 2
def test_valid_email_multiple_users_returns_first(user_controller, mock_dao):
    users = [{'email' : 'valid@domain.com'}, {'email' : 'valid@domain.com'}]
    mock_dao.find.return_value = users
    result = user_controller.get_user_by_email('valid@domain.com')
    assert result == users[0]

def test_valid_email_no_user_found(user_controller, mock_dao):
    mock_dao.find.return_value = []
    result2 = user_controller.get_user_by_email('valid@domain.com')
    assert result2 is None

def test_invalid_email_raises_value_error(user_controller):
    with pytest.raises(ValueError):
        user_controller.get_user_by_email('invalidemail')

#updated to use match=
def test_dao_exception_raises_exception(user_controller, mock_dao):
    mock_dao.find.side_effect = Exception("DB error")
    with pytest.raises(Exception, match="DB error"):
        user_controller.get_user_by_email('valid@domain.com')