from user.manager import UserManager
from resources.loader import JSONLoader
from repositories.user import StableClientsRepo

user_manager = UserManager()
json_loader = JSONLoader()
stable_clients = StableClientsRepo()
