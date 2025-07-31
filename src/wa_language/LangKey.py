class LangKey(str):
    """
    Tests:
    >>> print(repr(LangKey("wa_player")))
    LangKey('wa_player')
    """
    def __repr__(self):
        return "{}({})".format("LangKey", super().__repr__())


# Ugly hack for binding and spreading
# As far as we store obj in binding but substitute str(obj)
# we have to provide a LangKey that returns LangValue by __str__ method
# in order to substitute that value instead of variable
# TODO: Make it more explicitly what we substitute by LangValue.binding
#       Using str(obj) confuses and leads to such hucks
class LangKeyStr(LangKey):
    def __new__(cls, key, substitute):
        inst = super().__new__(cls, key)
        inst.__str = substitute
        return inst

    def __str__(self):
        return self.__str
