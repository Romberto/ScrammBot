import psycopg2
from config import DATABASES


def connect():
    try:
        connection = psycopg2.connect(user=DATABASES['default']['USER'],
                                      # пароль, который указали при установке PostgreSQL
                                      password=DATABASES['default']['PASSWORD'],
                                      host="127.0.0.1",
                                      port="5432",
                                      dbname=DATABASES['default']['NAME'])
        return connection

    except Exception as _ex:
        print("*" * 20, " ошибка ", "*" * 20)
        print(_ex)
        return False


async def get_user_db(name):
    # возвращает пользователя по username
    conn = connect()
    if conn:
        cursor = conn.cursor()
        # Выполнение SQL-запроса

        cursor.execute("SELECT * FROM auth_user WHERE username='" + name + "';")
        # Получить результат
        record = cursor.fetchone()
        if record:
            conn.close()
            return record
        else:
            conn.close()
            return False


async def set_secret_key(user_id, secret_key: str, ):
    # устанавливает секретный код в таблице auth_user_profile
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE auth_user_profile SET secret_key=%s WHERE user_id = %s", (secret_key, user_id))
            conn.commit()
            conn.close()
            return True


        except Exception as _ex:
            print(_ex)
            conn.close()
            return False


async def add_user(user_id, chat_id):
    # добавляет  chat_id в таблицу auth_user_authuserbot
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO auth_user_authuserbot (user_id, chat_id) VALUES (%s,%s);", (user_id, chat_id))
            conn.commit()
            conn.close()
        except Exception as _ex:
            print('ошибка ', _ex)
            conn.close()


async def get_auth_user():
    conn = connect()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT chat_id FROM auth_user_authuserbot")
            result = []
            for item in cursor:
                result.append(item[0])
            conn.close()
            return result
        except Exception as _ex:
            print(_ex)
            conn.close()


if __name__ == "__main__":
    pass
