class Session(object):
    def __init__(self):
        self.sessions = {}

    def find_create_session(self, chat_id):
        if chat_id in self.sessions:
            return chat_id
        else:
            self.sessions[chat_id] = {'context': {}}
        return chat_id

    def update_context(self, chat_id, context):
        self.sessions[chat_id]['context'] = context

    def del_context(self, chat_id, context):
        del self.sessions[chat_id]['context']

    def destroy_session(self, chat_id):
        del self.sessions[chat_id]

    def get_context(self, chat_id):
        return self.sessions[chat_id]['context']
