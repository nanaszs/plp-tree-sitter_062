export default grammar({
  name: 'filter',
  extras: $ => [/\s/],
  word: $ => $.identifier,

  rules: {
    query: $ => $._expr,

    _expr: $ => choice(
      $.comparison, $.in_expression, $.contains_expression,
      $.and_expression, $.or_expression,
      $.not_expression, $.parenthesized,
    ),

    comparison: $ => seq(
      field('field', $.identifier),
      field('operator', choice('=', '!=', '>', '<', '>=', '<=')),
      field('value', $._value),
    ),

    in_expression: $ => seq(
      field('field', $.identifier),
      'in',
      '(',
      field('value', $._value),
      repeat(seq(',', field('value', $._value))),
      ')',
    ),

    contains_expression: $ => seq(
      field('field', $.identifier),
      'contains',
      field('value', $._value),
    ),

    or_expression: $ => prec.left(1, seq(field('left', $._expr), 'or', field('right', $._expr))),
    and_expression: $ => prec.left(2, seq(field('left', $._expr), 'and', field('right', $._expr))),
    not_expression: $ => prec(3, seq('not', field('operand', $._expr))),
    parenthesized: $ => seq('(', $._expr, ')'),

    _value: $ => choice($.string, $.number, $.boolean),
    string: $ => /"[^"]*"/,
    number: $ => /\d+(\.\d+)?/,
    boolean: $ => choice('true', 'false'),
    identifier: $ => /[a-zA-Z_][a-zA-Z0-9_.]*/,
  }
});