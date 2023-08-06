from collections.abc import Iterable


def type_check(arg_name:str, input, types:Iterable):
    if not any([isinstance(input, t) for t in types]):
        raise TypeError(f'Argument: "{arg_name}" should be (1) of types "{types}", not "{type(input)}"!')

def val_check(arg_name:str, input, allowed_vals:Iterable):
    if input not in allowed_vals:
        raise ValueError(f'Argument: "{arg_name}" should be (1) of "{allowed_vals}", not "{input}"!')
