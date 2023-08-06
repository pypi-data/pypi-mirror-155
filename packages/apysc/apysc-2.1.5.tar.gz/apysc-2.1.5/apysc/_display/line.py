"""Implementations of the Line class.
"""


from apysc._display import graphics
from apysc._display.line_base import LineBase
from apysc._geom import point2d
from apysc._html.debug_mode import add_debug_info_setting
from apysc._validation import arg_validation_decos


class Line(LineBase):
    """
    The line vector graphics class.

    References
    ----------
    - Graphics draw_line interface document
        - https://simon-ritchie.github.io/apysc/graphics_draw_line.html  # noqa
    - Graphics draw_dotted_line interface document
        - https://simon-ritchie.github.io/apysc/graphics_draw_dotted_line.html  # noqa
    - Graphics draw_dashed_line interface document
        - https://simon-ritchie.github.io/apysc/graphics_draw_dashed_line.html  # noqa
    - Graphics draw_round_dotted_line interface document
        - https://simon-ritchie.github.io/apysc/graphics_draw_round_dotted_line.html  # noqa
    - Graphics draw_dash_dotted_line interface document
        - https://simon-ritchie.github.io/apysc/graphics_draw_dash_dotted_line.html # noqa

    Examples
    --------
    >>> import apysc as ap
    >>> stage: ap.Stage = ap.Stage()
    >>> sprite: ap.Sprite = ap.Sprite()
    >>> sprite.graphics.line_style(color='#fff', thickness=5)
    >>> line: ap.Line = sprite.graphics.draw_line(
    ...     x_start=50, y_start=50, x_end=150, y_end=50)
    >>> line.line_color
    String('#ffffff')

    >>> line.line_thickness
    Int(5)
    """

    _start_point: 'point2d.Point2D'
    _end_point: 'point2d.Point2D'

    @arg_validation_decos.is_display_object_container(
        arg_position_index=1, optional=False)
    @arg_validation_decos.is_point_2d(arg_position_index=2)
    @arg_validation_decos.is_point_2d(arg_position_index=3)
    @add_debug_info_setting(
        module_name=__name__, class_name='Line')
    def __init__(
            self, *, parent: 'graphics.Graphics',
            start_point: 'point2d.Point2D',
            end_point: 'point2d.Point2D') -> None:
        """
        Create a line vector graphic.

        Parameters
        ----------
        parent : Graphics
            Graphics instance to link this graphic.
        start_point : Points2D
            Line start point.
        end_point : Points2D
            Line end point.

        References
        ----------
        - Graphics draw_line interface document
            - https://simon-ritchie.github.io/apysc/graphics_draw_line.html  # noqa
        - Graphics draw_dotted_line interface document
            - https://simon-ritchie.github.io/apysc/graphics_draw_dotted_line.html  # noqa
        - Graphics draw_dashed_line interface document
            - https://simon-ritchie.github.io/apysc/graphics_draw_dashed_line.html  # noqa
        - Graphics draw_round_dotted_line interface document
            - https://simon-ritchie.github.io/apysc/graphics_draw_round_dotted_line.html  # noqa
        - Graphics draw_dash_dotted_line interface document
            - https://simon-ritchie.github.io/apysc/graphics_draw_dash_dotted_line.html # noqa

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.line_style(color='#fff', thickness=5)
        >>> line: ap.Line = sprite.graphics.draw_line(
        ...     x_start=50, y_start=50, x_end=150, y_end=50)
        >>> line.line_color
        String('#ffffff')

        >>> line.line_thickness
        Int(5)
        """
        from apysc._display.graphics import Graphics
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names
        parent_graphics: Graphics = parent
        variable_name: str = expression_variables_util.\
            get_next_variable_name(type_name=var_names.LINE)
        super(Line, self).__init__(
            parent=parent, x=0, y=0, variable_name=variable_name)
        self._start_point = start_point
        self._end_point = end_point
        self._set_initial_basic_values(parent=parent)
        self._append_constructor_expression()
        self._set_line_setting_if_not_none_value_exists(
            parent_graphics=parent_graphics)
        self._set_overflow_visible_setting()

    @add_debug_info_setting(
        module_name=__name__, class_name='Line')
    def _append_constructor_expression(self) -> None:
        """
        Append a constructor expression.
        """
        import apysc as ap
        from apysc._display.stage import get_stage_variable_name
        stage_variable_name: str = get_stage_variable_name()
        points_str: str = self._make_points_expression()
        expression: str = (
            f'var {self.variable_name} = {stage_variable_name}'
            f'\n  .line({points_str})'
            '\n  .attr({'
        )
        expression = self._append_basic_vals_expression(
            expression=expression,
            indent_num=2)
        expression += '\n  });'
        ap.append_js_expression(expression=expression)

    def _make_points_expression(self) -> str:
        """
        Make line start and end expression str.

        Returns
        -------
        expression : str
            Each point expression.
        """
        import apysc as ap
        start_point: ap.Point2D = self._start_point
        end_point: ap.Point2D = self._end_point
        expression: str = (
            f'{start_point.x.variable_name}, '
            f'{start_point.y.variable_name}, '
            f'{end_point.x.variable_name}, '
            f'{end_point.y.variable_name}'
        )
        return expression

    def __repr__(self) -> str:
        """
        Get a string representation of this instance (for the sake of
        debugging).

        Returns
        -------
        repr_str : str
            Type name and variable name will be set
            (e.g., `Line('<variable_name>')`).
        """
        repr_str: str = f"Line('{self.variable_name}')"
        return repr_str
