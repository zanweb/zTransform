    @property
    def action_code(self):
        return self._action_code

    @action_code.setter
    def action_code(self, value):
        if not isinstance(value, str):
            raise ValueError('action_code must be a string!')
        if len(value) > 20:
            raise ValueError('action_code must less than 20 characters!')
        self._action_code = value

    @action_code.deleter
    def action_code(self):
        raise AttributeError("Can't delete attribute")
