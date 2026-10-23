from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()
pasword  = os.getenv("PASSWORD_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="postgres",
            database="finance_bot",
            password=pasword
        )
        return conn
    except Exception as Error:
        print(f"Connection Error: {Error}")





async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
Create table if not exists users(
    id serial primary key,
    username varchar(100),
    balance int default 0,
    telegram_id varchar(200),
    created_at timestamp default now(),
    is_active boolean default true
);


Create table if not exists history (
id serial primary key,
title varchar(100),
type varchar(200),
sum int,
user_id int references users(id),
status boolean default false,
is_active boolean default true
)
""")
        print("Table created")
    except Exception as Error:
        print(f"Create Error: {Error}")
    finally:
        await conn.close()


