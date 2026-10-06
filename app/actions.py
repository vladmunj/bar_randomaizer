user_actions = {}

def set_action(user_id: int, action: str):
    user_actions[user_id] = action

def get_action(user_id: int):
    return user_actions.get(user_id)

def clear_action(user_id: int):
    user_actions.pop(user_id, None)