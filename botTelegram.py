from aiogram.utils import executor
from loader import dp
from handlers import auth_client

auth_client.register_handlers_auth(dp)



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
