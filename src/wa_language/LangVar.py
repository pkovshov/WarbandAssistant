class LangVar(str):
    def __repr__(self):
        return "{}({})".format(self.__class__.__name__,
                               super().__repr__())

class __PlayerSexVarType(LangVar):
    __inst = None

    def __new__(cls):
        if cls.__inst is None:
            cls.__inst = super().__new__(cls)
        return cls.__inst

    def __eq__(self, other):
        return self is other

    def __ne__(self, other):
        return self is not other

    def __hash__(self):
        return hash(id(self))

    def __repr__(self):
        return "PlayerSexVar"


PlayerSexVar = __PlayerSexVarType()

PLAYER_NAME_VAR = LangVar("playername")
