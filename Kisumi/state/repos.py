from user.manager import UserManager
from resources.loader import JSONLoader
from resources.db.geo.geo import GeolocationDB
from repositories.user import OnlineUsersRepo

user_manager = UserManager()
json_loader = JSONLoader()
geoloc = GeolocationDB()
online = OnlineUsersRepo()
