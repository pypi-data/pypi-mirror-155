import enum
import operator


class BlockType(enum.Enum):
    controls_if = "controls_if"
    logic_compare = "logic_compare"
    logic_operation = "logic_operation"
    logic_negate = "logic_negate"
    logic_null = "logic_null"
    variables_get = "variables_get"
    variables_set = "variables_set"
    math_number = "math_number"
    math_change = "math_change"
    math_arithmetic = "math_arithmetic"
    text = "text"
    text_print = "text_print"


logic_operators_to_fn = {
    "LT": operator.lt,
    "LTE": operator.le,
    "GT": operator.gt,
    "GTE": operator.ge,
    "EQ": operator.eq,
    "NEQ": operator.ne,
}

math_operators_to_fn = {
    "ADD": operator.add,
    "MINUS": operator.sub,
    "MULTIPLY": operator.mul,
    "DIVIDE": operator.truediv,
    "POWER": operator.pow,
}

boolean_operators_to_fn = {
    "AND": operator.and_,
    "OR": operator.or_,
}
