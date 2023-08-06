"""Graphics class-related expression implementations.
"""

from apysc._display.graphics import Graphics
from apysc._display.graphics_base import GraphicsBase
from apysc._html.debug_mode import add_debug_info_setting


@add_debug_info_setting(module_name=__name__)
def append_fill_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append a fill expression to specified expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended fill expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    if graphics.fill_color == '':
        expression += f'\n{spaces}fill: "none",'
        return expression
    expression += (
        f'\n{spaces}fill: {graphics.fill_color.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_fill_opacity_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append a fill opacity expression to a specified expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended fill opacity expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}"fill-opacity": {graphics.fill_alpha.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_x_expression(
        *, graphic: GraphicsBase, expression: str, indent_num: int) -> str:
    """
    Append x position expression to specified expression's string.

    Parameters
    ----------
    graphic : GraphicsBase
        Target graphic instance, for example, Rectangle.
    expression : str
        Expression string to be appended x position expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}x: {graphic.x.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_y_expression(
        *, graphic: GraphicsBase, expression: str, indent_num: int) -> str:
    """
    Append y position expression to specified expression's string.

    Parameters
    ----------
    graphic : GraphicsBase
        Target graphic instance, for example, Rectangle.
    expression : str
        Expression string to be appended y position expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}y: {graphic.y.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_stroke_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append stroke expression to specified expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended stroke expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    if graphics.line_color == '':
        return expression
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}stroke: {graphics.line_color.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_stroke_width_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append stroke width expression to specified expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended stroke width expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}"stroke-width": '
        f'{graphics.line_thickness.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_stroke_opacity_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append stroke opacity expression to specified expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended stroke opacity expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    from apysc._string import indent_util
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}"stroke-opacity": {graphics.line_alpha.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_stroke_linecap_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append stroke line cap expression to specified expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended stroke linecap expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    import apysc as ap
    from apysc._string import indent_util
    if graphics.line_cap == ap.LineCaps.BUTT.value:
        return expression
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}"stroke-linecap": {graphics.line_cap.variable_name},'
    )
    return expression


@add_debug_info_setting(module_name=__name__)
def append_stroke_linejoin_expression(
        *, graphics: Graphics, expression: str, indent_num: int) -> str:
    """
    Append stroke line-join expression to specified
    expression's string.

    Parameters
    ----------
    graphics : Graphics
        Target Graphics instance.
    expression : str
        Expression string to be appended stroke linejoin expression.
    indent_num : int
        Indentation number.

    Returns
    -------
    expression : str
        After appended expression string.
    """
    import apysc as ap
    from apysc._string import indent_util
    if graphics.line_joints == ap.LineJoints.MITER.value:
        return expression
    spaces: str = indent_util.make_spaces_for_html(indent_num=indent_num)
    expression += (
        f'\n{spaces}"stroke-linejoin": '
        f'{graphics.line_joints.variable_name},'
    )
    return expression
