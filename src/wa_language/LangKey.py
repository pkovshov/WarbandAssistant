class LangKey(str):
    """
    Tests:
    >>> print(repr(LangKey("wa_player")))
    LangKey('wa_player')
    """
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, repr(str(self)))
