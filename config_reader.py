from environs import Env

env = Env()
env.read_env(path="./.env")
SECRET_KEY = env.str("BOT_TOKEN")
