import aiosqlite

async def send_qa_to_db(user, question,answer):
    conn = await aiosqlite.connect('db/petrsu.db')
    send_ans = ''

    for an in answer:
        send_ans += an + ';'

    await conn.execute(f"INSERT INTO qa_table (telegram_id, question, answer) VALUES ('{user}', '{question}', '{send_ans[:-1]}');")
    await conn.commit()
    await conn.close()