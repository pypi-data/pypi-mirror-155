class prentr:
    """ `Print anything without any hassle` """
    def __setattr__(self,_, *value):
        print(', '.join(map(str, *value)) if isinstance(value[0], tuple) else value[0])

