import aiosqlite, time


# await db.execute('INSERT INTO users (user_id, username, balance, all_time) VALUES (?, ?, ?, ?)', (user_id, user_name, 0, 0))
# await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (user_name, user_id))

async def check_start(database):
    global db
    db = await aiosqlite.connect(database)
    


    await db.execute('''CREATE TABLE IF NOT EXISTS users
        (user_id INT, username TEXT, status INT DEFAULT 0, reg_date INT DEFAULT 0)'''
    )

    await db.commit()
    return db


async def add_db(user_id, username, start_time):
    info = await (await db.execute("select * from users where user_id = ?", (user_id,))).fetchone()
    if not info:
        await db.execute('INSERT INTO users (user_id, username, reg_date) VALUES (?, ?, ?)', (user_id, username, start_time))
        await db.commit()
    else:
        if username != info[1]:
            await db.execute("UPDATE users SET username = ? WHERE user_id = ?", (username, user_id))
            await db.commit()


async def get_user(user_id):
    info = await (await db.execute("select * from users where user_id = ?", (user_id,))).fetchone()
    return info


async def set_limit(user_id, status):
    await db.execute("UPDATE users SET status = ? WHERE user_id = ?", (status, user_id))
    await db.commit()

async def get_users():
    info = await (await db.execute("select * from users")).fetchall()
    return info


async def get_info():
    a = len(await (await db.execute("select * from users where reg_date > ?", ((time.time() - 86400),))).fetchall())
    b = len(await (await db.execute("select * from users where reg_date > ?", ((time.time() - 7*86400),))).fetchall())
    c = len(await (await db.execute("select * from users where reg_date > ?", ((time.time() - 30*86400),))).fetchall())
    d = len(await get_users())
    return a, b, c, d
