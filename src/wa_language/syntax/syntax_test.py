from wa_language.syntax.Identifier import Identifier
from wa_language.syntax.IdentifierExpression import IdentifierExpression
from wa_language.syntax.BinaryExpression import BinaryExpression
from wa_language.syntax.TernaryExpression import TernaryExpression
from wa_language.syntax.Interpolation import Interpolation


def test_interpolation():
    source = "{reg1?{reg2}:Hello {sir/madam} from {s1?me:us}} and welcome"
    result = Interpolation(source)
    result_str = str(result)
    assert result_str == source


if __name__ == "__main__":
    test_interpolation()
