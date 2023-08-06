class ParsingTask:
    def __init__(self, method, method_args, callback, callback_args, callback_kwargs):
        self.method = method
        self.method_args = method_args
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs
