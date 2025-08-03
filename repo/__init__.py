from repo.repo import Repo
from utils import config

repo = Repo(
    username=config.DATABASE.username,
    password=config.DATABASE.password,
    host=config.DATABASE.host,
    port=config.DATABASE.port,
    db=config.DATABASE.database
)