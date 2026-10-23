from conection import *      


async def create_user(username,  telegram_id):
    try:
        conn = await connection_db()
        await conn.execute("""
        insert into users(username, telegram_id) Values
        ($1, $2)
                     """, username, str(telegram_id))
    except Exception as Error:
        print(f"Create user Error: {Error}")
    finally:
        await conn.close()






async def get_users():
    try:
        conn = await connection_db()
        users = await conn.fetch("""
        select * from users
                     """)
        return users
    except Exception as Error:
        print(f"Get user Error: {Error}")
    finally:
            await conn.close()






async def withdraw(ammount, tg_di, title):
    try:
        conn = await connection_db()

        await conn.execute("""
UPDATE users
SET balance = balance - $1
WHERE telegram_id = $2;
""", ammount, str(tg_di))
            
        await conn.execute("""
INSERT INTO history ( title, type, sum)
VALUES ($1, 'withdraw', $2);
""", title, int(ammount))
        return True
    except Exception as erorr:
        print(f"Withdraw erorr: {erorr}")
    finally:
        await conn.close()






async def deposit(ammount, tg_di, title):
    try:
        conn = await connection_db()

        await conn.execute("""
UPDATE users
SET balance = balance + $1
WHERE telegram_id = $2;
""", ammount, str(tg_di))
        await conn.execute("""
INSERT INTO history ( title, type, sum)
VALUES ($1, 'deposit', $2);
""", title,  int(ammount))
        return True
    except Exception as erorr:
        print(f"deposit erorr: {erorr}")
    finally:
        await conn.close()




async def profile(tg_id):
    try:
        conn = await connection_db()
        return await conn.fetchrow("""
        select * from users 
        where telegram_id = $1
                     """, str(tg_id))
    except Exception as erorr:
        print(f"Show profile erorr: {erorr}")
    finally:
            await conn.close()



async def history():
    try:
        conn = await connection_db()
        return await conn.fetch("""
SELECT * FROM history
""",)
    except Exception as erorr:
        print(f"history erorr: {erorr}")
    finally:
        await conn.close()










async def get_user_by_id(telegram_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
        select * from users where telegram_id = $1
                     """, str(telegram_id))
        return user
    except Exception as Error:
        print(f"Get user by id Error: {Error}")
    finally:
        await conn.close()
        




