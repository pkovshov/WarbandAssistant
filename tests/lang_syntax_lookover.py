from wa_language import Language
from wa_language.syntax.TernaryExpression import TernaryExpression

lang = Language.load()
for key, val in lang.items():
    for item in val.items:
        if isinstance(item, TernaryExpression):
            condition = item.condition
            true_part = item.true_part
            false_part = item.false_part
            if condition in (true_part.identifiers + false_part.identifiers):
                print(key, val, sep="|")
                break
