class Expression:
    def __repr__(self):
        return f"{self.__class__.__name__}({repr(str(self))})"
