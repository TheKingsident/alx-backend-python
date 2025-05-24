import aiosqlite
import asyncio

async def async_fetch_users():
    """Asynchronously fetch users from the database."""
    async with aiosqlite.connect("users.db") as connection:
        cursor = await connection.cursor()
        await cursor.execute("SELECT * FROM users")
        results = await cursor.fetchall()
        return results
    
async def async_fetch_older_users():
    """Asynchronously fetch users older than 40 from the database."""
    async with aiosqlite.connect("users.db") as connection:
        cursor = await connection.cursor()
        await cursor.execute("SELECT * FROM users WHERE age > ?", (40,))
        results = await cursor.fetchall()
        return results
    
async def fetch_concurrently():
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()   
    )

    print("All Users:")
    for user in all_users:
        print(dict(user))
    
    print("\nOlder Users:")
    for user in older_users:
        print(dict(user))

asyncio.run(fetch_concurrently())
