import asyncio

messages_to_delete_pool: dict[tuple[int, int], set[int]] = {}

def add_message_to_delete(
    chat_id: int,
    user_id: int,
    message_id: int,
):
    key = (chat_id, user_id)
    if key not in messages_to_delete_pool:
        messages_to_delete_pool[key] = set()
    messages_to_delete_pool[key].add(message_id)

async def delete_messages_from_pool(
    client,
    chat_id: int,
    user_id: int,
    delay: int = 5,
):
    key = (chat_id, user_id)
    await asyncio.sleep(delay)
    message_ids = messages_to_delete_pool.pop(key, set())
    if not message_ids: return
    try:
        await client.delete_messages(
            chat_id,
            list(message_ids),
        )
    except Exception as error:
        print(f"Failed to delete messages: {error}")