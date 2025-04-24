import pytest
from pymongo.errors import WriteError
from src.util.dao import DAO
from pymongo import MongoClient


@pytest.fixture
def test_dao():
    client = MongoClient("mongodb://root:root@localhost:27017")
    db = client["edutask_test"]
    collection = db["test_users"]
    collection.drop()
    return DAO(collection_name="test_users")

def test_create_valid_user(test_dao):
    valid_user = {
        "firstName" : "Erik",
        "lastName" : "Isaksson",
        "email" : "erik.isaksson@example.com"
    }
    result = test_dao.create(valid_user)
    assert "_id" in result

def test_create_missing_required_field(test_dao):
    missing_email = {
        "firstName" : "Erik",
        "lastName" : "Nolander"
    }
    with pytest.raises(WriteError):
        test_dao.create(missing_email)

def test_create_invalid_type(test_dao):
    wrong_type = {
        "firstName" : 1234,
        "lastName" : "Något",
        "email" : "något@example.com"
    }
    with pytest.raises(WriteError):
        test_dao.create(wrong_type)

def test_create_extra_field(test_dao):
    extra_field = {
        "firstName" : "John",
        "lastName" : "Doe",
        "email" : "john.doe@example.com",
        "admin" : True
    }
    with pytest.raises(WriteError):
        test_dao.create(extra_field)

def test_create_simulated_db_error(monkeypatch, test_dao):
    def mock_insert_fail(*args, **kwargs):
        raise Exception("Simulated DB failure")
    monkeypatch.setattr(test_dao.collection, "insert_one", mock_insert_fail)
    with pytest.raises(Exception, match="Simulated DB failure"):
        test_dao.create({
            "firstName" : "Karl",
            "lastName" : "Svensson",
            "email" : "karl.svensson@example.com"
        })