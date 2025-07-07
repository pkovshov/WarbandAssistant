from wa_language.LangLoader import load_lang
from wa_language.syntax.Ternary import Ternary

lang = load_lang()
for key, val in lang.items():
    for field in val.fields:
        expression = field.expression
        if isinstance(expression, Ternary):
            condition = expression.condition
            true_part = expression.true_part
            false_part = expression.false_part
            if condition.variable in (true_part.variables | false_part.variables):
                print(key, val, sep="|")
                break
