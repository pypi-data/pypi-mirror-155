"""Implementations of Polyline class.
"""


from apysc._display import graphics
from apysc._display.append_line_point_interface import AppendLinePointInterface
from apysc._display.line_base import LineBase
from apysc._geom.point2d import Point2D
from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.array import Array
from apysc._validation import arg_validation_decos


class Polyline(LineBase, AppendLinePointInterface):
    """
    The polyline vector graphics class.

    References
    ----------
    - Graphics move_to and line_to interfaces document
        - https://simon-ritchie.github.io/apysc/graphics_move_to_and_line_to.html  # noqa

    Examples
    --------
    >>> import apysc as ap
    >>> stage: ap.Stage = ap.Stage()
    >>> sprite: ap.Sprite = ap.Sprite()
    >>> sprite.graphics.line_style(color='#fff', thickness=5)
    >>> _ = sprite.graphics.move_to(x=50, y=50)
    >>> polyline: ap.Polyline = sprite.graphics.line_to(x=150, y=50)
    >>> polyline.line_color
    String('#ffffff')

    >>> polyline.line_thickness
    Int(5)
    """

    @arg_validation_decos.is_display_object_container(
        arg_position_index=1, optional=False)
    @arg_validation_decos.is_point_2ds(arg_position_index=2)
    @add_debug_info_setting(
        module_name=__name__, class_name='Polyline')
    def __init__(
            self, *, parent: 'graphics.Graphics',
            points: Array[Point2D]) -> None:
        """
        Create a polyline vector graphic.

        Parameters
        ----------
        parent : Graphics
            Graphics instance to link this graphic.
        points : Array of Point2D
            List of line points.

        References
        ----------
        - Graphics move_to and line_to interfaces document
            - https://simon-ritchie.github.io/apysc/graphics_move_to_and_line_to.html  # noqa

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.line_style(color='#fff', thickness=5)
        >>> _ = sprite.graphics.move_to(x=50, y=50)
        >>> polyline: ap.Polyline = sprite.graphics.line_to(x=150, y=50)
        >>> polyline.line_color
        String('#ffffff')

        >>> polyline.line_thickness
        Int(5)
        """
        from apysc._display.graphics import Graphics
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names
        parent_graphics: Graphics = parent
        variable_name: str = expression_variables_util.\
            get_next_variable_name(type_name=var_names.POLYLINE)
        super(Polyline, self).__init__(
            parent=parent, x=0, y=0,
            variable_name=variable_name)
        self.points = points
        self._set_initial_basic_values(parent=parent)
        self._append_constructor_expression()
        self._set_line_setting_if_not_none_value_exists(
            parent_graphics=parent_graphics)
        self._set_overflow_visible_setting()

    def __repr__(self) -> str:
        """
        Get a string representation of this instance (for the sake of
        debugging).

        Returns
        -------
        repr_str : str
            Type name and variable name will be set
            (e.g., `Polyline('<variable_name>')`).
        """
        repr_str: str = f"Polyline('{self.variable_name}')"
        return repr_str

    @add_debug_info_setting(
        module_name=__name__, class_name='Polyline')
    def _append_constructor_expression(self) -> None:
        """
        Append constructor expression.
        """
        import apysc as ap
        from apysc._display.stage import get_stage_variable_name
        stage_variable_name: str = get_stage_variable_name()
        points_var_name: str
        points_expression: str
        points_var_name, points_expression = \
            self._make_2dim_points_expression()
        expression: str = (
            f'{points_expression}'
            f'\nvar {self.variable_name} = {stage_variable_name}'
            f'\n  .polyline({points_var_name})'
            '\n  .attr({'
        )
        expression = self._append_basic_vals_expression(
            expression=expression, indent_num=2)
        expression += '\n  });'
        ap.append_js_expression(expression=expression)
        self._points_var_name = points_var_name
