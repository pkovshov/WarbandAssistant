"""Language resources syntax

Each string resource is an Interpolation (Interpolation object).
It could be
- Empty string
- Plain string that does not contain expressions
- Interpolation with the expressions
Example of Interpolation with the expressions:
'As you wish, {sire/my lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.'

An Interpolation splits into a sequence of items
where each item may be
- a plain string (str object)
- an expression (Expression object)

So, empty and plain strings are represented by Interpolations with one plain string item only.

In string resources there could be three types on expressions:
- Identifier expression (IdentifierExpression object).
  Examples of identifier expressions:
  - '{s9}'
  - '{reg5}'
- Binary expressions (BinaryExpression object)
  It is two plain or empty strings separated by slash '/'.
  Examples of binary expressions:
  - '{lord/lady}'
  - '{sir/madam}'
- Ternary expression (TernaryExpression object)
  It's an identifier followed by a question mark '?' and two interpolations separated by a colon ':'.
  Each interpolation may be an empty string, a plain string or may contain several items
  (plain strings or expressions or both).
  This leads to nested expressions.
  Examples of ternary expressions:
  - {reg7?them:him}
  - {reg6?I:{reg7?You:{s11}}}
  - {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am}
"""
