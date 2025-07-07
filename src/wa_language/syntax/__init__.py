"""Language resources syntax

Each string resource is an Interpolation (Interpolation object).
It could be
- Empty string
- Plain string that does not contain fields
- Interpolation with the fields
Example of Interpolation with the fields:
'As you wish, {sire/my lady}. {reg6?I:{reg7?You:{s11}}} will be the new {reg3?lady:lord} of {s1}.'

An Interpolation splits into a sequence of items
where each item may be
- a plain string (str object)
- a field (Field object)

So, empty and plain strings are represented by Interpolations with one string item only.

In string resources there could be three types on field expressions:
- An Identifier (Identifier object).
  Examples of Fields with Identifier:
  - '{s9}'
  - '{reg5}'
- Binary expressions (Binary object)
  It is two plain or empty strings separated by slash '/'.
  Examples of Fields with a Binary expression:
  - '{lord/lady}'
  - '{sir/madam}'
- Ternary expression (Ternary object)
  It's an identifier followed by a question mark '?' and two interpolations separated by a colon ':'.
  Each interpolation may be an empty string a plain string or may contain several fields.
  This leads to nested expressions.
  Examples of Fields with a Ternary expression:
  - {reg7?them:him}
  - {reg6?I:{reg7?You:{s11}}}
  - {reg3?Me and {reg4?{reg3} of my mates:one of my mates} are:I am}
"""