# Copyright (c) 2021, 2022 Henix, Henix.fr
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Expressions helpers"""

from typing import Any, Optional, Tuple

import re


## Expressions

PATH_EXPR = r'^([a-zA-Z_]\w*)(\.[a-zA-Z_]\w*|\[\'\w+\'\])+$'

STRING = r'(\'([^\']*)\')+'
IDENTIFIER = r'^[a-zA-Z_]\w*'
NUMBER = r'^(0x[0-9a-fA-F]+)|(-?\d+(\.\d+)?)'
OPERATOR = r'^(==|!=|!|<=|<|>=|>|\[|\]|\(|\)|\.|&&|\|\|)'

INFIX_OPERATOR = ['==', '!=', '<=', '<', '>', '>=', '&&', '||']

VALUE = 0
KIND = 1

STRING_TOKEN = 1
IDENTIFIER_TOKEN = 2
NUMBER_TOKEN = 3
OPERATOR_TOKEN = 4
END_TOKEN = 0


########################################################################
## Tokenizer


def get_token(expr: str):
    """Get first token in expr.

    # Required parameters

    - expr: a string

    # Returned value

    A tuple of three elements: `token`, `kind`, `expr`.

    # Raised exceptions

    A _ValueError_ exception is raised if the token is invalid.
    """
    if match := re.match(IDENTIFIER, expr):
        return match.group(0), IDENTIFIER_TOKEN, expr[match.end() :].strip()
    if match := re.match(STRING, expr):
        return (
            match.group(0)[1:-1].replace("''", "'"),
            STRING_TOKEN,
            expr[match.end() :].strip(),
        )
    if match := re.match(NUMBER, expr):
        num = match.group(0)
        if num.startswith('0x'):
            num = int(num, 16)
        else:
            num = float(num)
        return num, NUMBER_TOKEN, expr[match.end() :].strip()
    if match := re.match(OPERATOR, expr):
        return match.group(0), OPERATOR_TOKEN, expr[match.end() :].strip()
    raise ValueError(f'Invalid token {expr}')


def tokenize(expr: str):
    """Return a list of tokens found in expr.

    # Required parameters

    - expr: a string

    # Returned value

    A list of _tokens_.  Each token is a (value, kind) pair.  The list
    ends with an `(None, END_TOKEN)` pair.

    # Raised exceptions

    A _ValueError_ is raised if `expr` contains an invalid token.
    """
    tokens = []
    while expr:
        token, kind, expr = get_token(expr)
        tokens.append((token, kind))
    tokens.append((None, END_TOKEN))
    return tokens


########################################################################
## Operators helpers


def _is_infix_operator(token) -> bool:
    return token[KIND] == OPERATOR_TOKEN and token[VALUE] in INFIX_OPERATOR


def _is_dereference(token) -> bool:
    return token[KIND] == OPERATOR_TOKEN and token[VALUE] == '.'


def _is_index(token) -> bool:
    return token[KIND] == OPERATOR_TOKEN and token[VALUE] == '['


def _is_segment_start(token) -> bool:
    return _is_dereference(token) or _is_index(token)


def _is_lparen(token) -> bool:
    return token[KIND] == OPERATOR_TOKEN and token[VALUE] == '('


def _is_rparen(token) -> bool:
    return token[KIND] == OPERATOR_TOKEN and token[VALUE] == ')'


def _is_identifier(token) -> bool:
    return token[KIND] == IDENTIFIER_TOKEN


def _is_boolean(token) -> bool:
    return _is_identifier(token) and token[VALUE].lower() in ('true', 'false')


def _is_null(token) -> bool:
    return _is_identifier(token) and token[VALUE].lower() == 'null'


def _is_string(token) -> bool:
    return token[KIND] == STRING_TOKEN


########################################################################
## Path helpers


def find_path(tokens, start):
    """Find longest path in tokens starting at offset start.

    A _path_ is an identifier, possibly followed segments.  Segments are
    of the form `.identifier` or `[term]`, where `term` is either a
    path or a string.
    """
    path_len = 1
    while _is_segment_start(tokens[start + path_len]):
        if _is_dereference(tokens[start + path_len]):
            if not _is_identifier(tokens[start + path_len + 1]):
                raise ValueError(
                    f'Invalid token, was expecting identifier {tokens[start+path_len+1]}'
                )
            path_len += 2
        else:
            if _is_string(tokens[start + path_len + 1]):
                path_len += 3
            elif _is_identifier(tokens[start + path_len + 1]):
                path_len += 2 + find_path(tokens, start + path_len + 1)
            else:
                raise ValueError(
                    f'Invalid token, was expecting identifier or string {tokens[start+path_len+1]}'
                )
    return path_len


def evaluate_path(path, contexts):
    """Evaluate path using contexts.

    The path is syntactically valid.
    """

    def _evaluate_segments(start, value):
        if not _is_segment_start(path[start]):
            return value
        if _is_dereference(path[start]):
            if _is_segment_start(path[start + 2]):
                return _evaluate_segments(start + 2, value[path[start + 1][VALUE]])
            return value[path[start + 1][VALUE]]

        if path[start + 1][KIND] == STRING_TOKEN:
            what = path[start + 1][VALUE]
            if _is_segment_start(path[start + 3]):
                return _evaluate_segments(start + 3, value[what])
        else:
            path_len = find_path(path, start + 1)
            what = evaluate_path(path[start + 1 : start + 1 + path_len + 1], contexts)
            if _is_segment_start(path[start + 1 + path_len + 1]):
                return _evaluate_segments(start + 1 + path_len + 1, value[what])
        return value[what]

    segment = path[0][VALUE]
    if segment not in contexts:
        raise ValueError(f'Invalid segment {segment} or incorrect function call')

    return _evaluate_segments(1, contexts[segment])


def _to_number(val: Any) -> float:
    if val is None or val == '':
        return 0
    if isinstance(val, bool):
        return 1 if val else 0
    if isinstance(val, str):
        try:
            return float(val)
        except ValueError:
            return float('nan')
    if isinstance(val, (int, float)):
        return float(val)
    return float('nan')


def evaluate_operation(lhs, operator: str, rhs) -> bool:
    """Perform binary operation evaluation.

    Type casting performed as per specification.

    # Required parameters

    - lhs: an object
    - operator: a string
    - rhs: an object

    # Returned value

    A boolean.
    """
    if isinstance(lhs, str) and isinstance(rhs, str):
        lhs = lhs.lower()
        rhs = rhs.lower()
    elif type(lhs) != type(rhs):
        lhs = _to_number(lhs)
        rhs = _to_number(rhs)
    if operator == '==':
        return lhs == rhs
    if operator == '!=':
        return lhs != rhs
    if operator == '<':
        return lhs < rhs
    if operator == '<=':
        return lhs <= rhs
    if operator == '>':
        return lhs > rhs
    if operator == '>=':
        return lhs >= rhs
    if operator == '&&':
        return lhs and rhs
    if operator == '||':
        return lhs or rhs
    raise ValueError(f'Unknown operator {operator}')


def evaluate_tokenized(
    tokens, contexts, start, end_token=(None, END_TOKEN)
) -> Tuple[Optional[int], Any]:
    """Perform tokenized expression evaluation, using contexts.

    # Required parameters

    - tokens: a list of _tokens_
    - contexts: a dictionary
    - start: an integer

    # Returned value

    An object (depending on `tokens`).  Could be a boolean, a number, a
    string, a list, or a dictionary.
    """
    kind = tokens[start][KIND]
    if kind == END_TOKEN:
        return None, None
    if kind == IDENTIFIER_TOKEN:
        if _is_boolean(tokens[start]):
            what = tokens[start][VALUE].lower() == 'true'
            path = 1
        elif _is_null(tokens[start]):
            what = None
            path = 1
        elif _is_lparen(tokens[start + 1]) and _is_rparen(tokens[start + 2]):
            what = evaluate_status_function(tokens[start][VALUE], contexts)
            path = 3
        else:
            path = find_path(tokens, start)
            what = evaluate_path(tokens[start : start + path + 1], contexts)
    elif kind in (STRING_TOKEN, NUMBER_TOKEN):
        what = tokens[start][VALUE]
        path = 1
    elif _is_lparen(tokens[start]):
        path, what = evaluate_tokenized(
            tokens, contexts, start + 1, (')', OPERATOR_TOKEN)
        )
        if path is None:
            raise ValueError(
                'Unexpected end of expression, was expecting right parent.'
            )
        if not _is_rparen(tokens[start + path + 1]):
            raise ValueError(
                f'Invalid token, was expecting right parent {tokens[start+path+1]})'
            )
        path += 2
    else:
        raise ValueError(
            f'Invalid token, was expecting identifier, string or number {tokens[start]}'
        )
    if _is_infix_operator(tokens[start + path]):
        path_rhs, rhs = evaluate_tokenized(
            tokens, contexts, start + path + 1, end_token
        )
        if path_rhs is None:
            raise ValueError('Unexpected end of expression.')
        return path + 1 + path_rhs, evaluate_operation(
            what, tokens[start + path][VALUE], rhs
        )
    if tokens[start + path] == end_token:
        return path, what

    eot = '' if end_token[0] is None else f' or "{end_token[0]}"'
    if tokens[start + path][0] is None:
        raise ValueError(f'Unexpected end of expression, was expecting operator{eot}')
    raise ValueError(
        f'Invalid token, was expecting operator{eot}, got {tokens[start+path]}'
    )


def evaluate(expr: str, contexts):
    """Perform expression evaluation, using contexts.

    # Required parameters

    - expr: a string
    - contexts: a dictionary

    # Returned value

    An object (depending on `expr`).  Could be a boolean, a number, a
    string, a list, or a dictionary.
    """
    return evaluate_tokenized(tokenize(expr), contexts, 0)[1]


def evaluate_str(value: str, contexts):
    """Perform expression evaluation in string.

    `value` is either an expression or a string with expression(s) in
    it.

    # Required parameters

    - value: a string
    - contexts: a dictionary

    # Returned value

    If `value` is an expression, returns its evaluated value (can be
    any object).  If `value` contains expressions, returns a string
    with the expressions replaced by their values.
    """
    value = value.strip()
    if (
        value.startswith('${{')
        and value.endswith('}}')
        and value.count('${{') == 1
        and value.count('}}') == 1
    ):
        result = evaluate(value[3:-2].strip(), contexts)
    else:
        result = ''
        while '${{' in value:
            lhs, _, value = value.partition('${{')
            result += lhs
            expr, _, value = value.partition('}}')
            result += str(evaluate(expr.strip(), contexts))
        result += value
    return result


def evaluate_item(item, contexts):
    """Perform expression evaluation for item.

    If `item` is a list or dictionary, perform recursive evaluation.

    # Required parameters

    - item: any object
    - contexts: a dictionary

    # Returned value

    An object (same type as `item`).
    """
    if isinstance(item, dict):
        return evaluate_items(item, contexts)
    if isinstance(item, list):
        return [evaluate_item(entry, contexts) for entry in item]
    if isinstance(item, str):
        return evaluate_str(item, contexts)
    return item


def evaluate_items(items, contexts):
    """Perform expression evaluation in items.

    If items contain sub-elements, the evaluation is performed recursively.

    If the referenced context element does not exist, raises a _KeyError_
    exception.

    Strip spaces around expressions, but does not strip spaces not in
    expressions.

    TODO: limit 'variables' context usage ('name', 'with', and 'if')
    """
    result = {}
    for item, value in items.items():
        if isinstance(value, str) and '${{' in value:
            result[item] = evaluate_str(value, contexts)
        elif isinstance(value, dict):
            result[item] = evaluate_items(value, contexts)
        elif isinstance(value, list):
            result[item] = [evaluate_item(entry, contexts) for entry in value]
        else:
            result[item] = value
    return result


def evaluate_status_function(name: str, contexts) -> bool:
    """Evaluate job status function."""
    if name == 'always':
        return True
    if name == 'success':
        return contexts['job']['status'] == 'success'
    if name == 'failure':
        return contexts['job']['status'] == 'failure'
    if name == 'cancelled':
        return contexts['job']['status'] == 'cancelled'
    raise ValueError(f'Unknown function {name}')


def evaluate_bool(expr: str, contexts) -> bool:
    """Evaluate expression in context.

    `expr` may be surrounded by `${{` and `}}`.

    # Required parameters

    - expr: a string
    - contexts: a dictionary

    # Returned value

    A boolean.
    """
    expr = _maybe_remove_expression_syntax(expr)
    return _to_number(evaluate(expr, contexts)) != 0


def _maybe_remove_expression_syntax(expr: str) -> str:
    """Strip expression syntax if present."""
    expr = expr.strip()
    if re.match(r'^\$\{\{.*\}\}$', expr):
        expr = expr[3:-2]
    return expr.strip()
