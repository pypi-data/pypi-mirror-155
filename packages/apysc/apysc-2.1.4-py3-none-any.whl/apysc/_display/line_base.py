"""Base class implementation for each line.
"""

from abc import ABC
from abc import abstractmethod

from apysc._display import graphics
from apysc._display.fill_alpha_interface import FillAlphaInterface
from apysc._display.fill_color_interface import FillColorInterface
from apysc._display.graphics_base import GraphicsBase
from apysc._display.line_alpha_interface import LineAlphaInterface
from apysc._display.line_color_interface import LineColorInterface
from apysc._display.line_dash_dot_setting_interface import \
    LineDashDotSettingInterface
from apysc._display.line_dash_setting_interface import LineDashSettingInterface
from apysc._display.line_dot_setting_interface import LineDotSettingInterface
from apysc._display.line_joints_interface import LineJointsInterface
from apysc._display.line_round_dot_setting_interface import \
    LineRoundDotSettingInterface
from apysc._html.debug_mode import add_debug_info_setting


class LineBase(
        GraphicsBase, FillColorInterface, FillAlphaInterface,
        LineColorInterface, LineAlphaInterface,
        LineJointsInterface, LineDotSettingInterface,
        LineDashSettingInterface, LineRoundDotSettingInterface,
        LineDashDotSettingInterface, ABC):

    @abstractmethod
    def __repr__(self) -> str:
        """
        Get a string representation of this instance (for the sake of
        debugging).
        """

    @add_debug_info_setting(
        module_name=__name__, class_name='LineBase')
    def _set_line_setting_if_not_none_value_exists(
            self, *, parent_graphics: 'graphics.Graphics') -> None:
        """
        If a line setting (dot, dash, or something else) with a value
        other than None exists, set that value to the attribute.

        Parameters
        ----------
        parent_graphics : Graphics
            Parent Graphics instance.
        """
        from apysc._display.graphics import Graphics
        parent_graphics_: Graphics = parent_graphics
        if parent_graphics_.line_dot_setting is not None:
            self.line_dot_setting = parent_graphics_.line_dot_setting
            return
        if parent_graphics_.line_dash_setting is not None:
            self.line_dash_setting = parent_graphics_.line_dash_setting
            return
        if parent_graphics_.line_round_dot_setting is not None:
            self.line_round_dot_setting = \
                parent_graphics_.line_round_dot_setting
            return
        if parent_graphics_.line_dash_dot_setting is not None:
            self.line_dash_dot_setting = \
                parent_graphics_.line_dash_dot_setting
            return

    @add_debug_info_setting(
        module_name=__name__, class_name='LineBase')
    def _set_initial_basic_values(
            self, *, parent: 'graphics.Graphics') -> None:
        """
        Set initial fundamental values (such as the fill color or
        line thickness).

        Parameters
        ----------
        parent : Graphics
            Graphics instance to link this graphic.
        """
        from apysc._display.graphics import Graphics
        parent_graphics: Graphics = parent
        self._set_initial_fill_color_if_not_blank(
            fill_color=parent_graphics.fill_color)
        self._update_fill_alpha_and_skip_appending_exp(
            value=parent_graphics.fill_alpha)
        self._set_initial_line_color_if_not_blank(
            line_color=parent_graphics.line_color)
        self._update_line_thickness_and_skip_appending_exp(
            value=parent_graphics.line_thickness)
        self._update_line_alpha_and_skip_appending_exp(
            value=parent_graphics.line_alpha)
        self._initialize_x_if_not_initialized()
        self._initialize_y_if_not_initialized()
        self._update_line_cap_and_skip_appending_exp(
            value=parent_graphics.line_cap)
        self._update_line_joints_and_skip_appending_exp(
            value=parent_graphics.line_joints)

        self._append_applying_new_attr_val_exp(
            new_attr=self._fill_alpha, attr_name='fill_alpha')
        self._append_attr_to_linking_stack(
            attr=self._fill_alpha, attr_name='fill_alpha')

        self._append_applying_new_attr_val_exp(
            new_attr=self._fill_color, attr_name='fill_color')
        self._append_attr_to_linking_stack(
            attr=self._fill_color, attr_name='fill_color')

        self._append_applying_new_attr_val_exp(
            new_attr=self._line_color, attr_name='line_color')
        self._append_attr_to_linking_stack(
            attr=self._line_color, attr_name='line_color')

        self._append_applying_new_attr_val_exp(
            new_attr=self._line_alpha, attr_name='line_alpha')
        self._append_attr_to_linking_stack(
            attr=self._line_alpha, attr_name='line_alpha')

        self._append_applying_new_attr_val_exp(
            new_attr=self._line_thickness, attr_name='line_thickness')
        self._append_attr_to_linking_stack(
            attr=self._line_thickness, attr_name='line_thickness')

    @add_debug_info_setting(
        module_name=__name__, class_name='LineBase')
    def _append_basic_vals_expression(
            self, *, expression: str, indent_num: int) -> str:
        """
        Append basic values expression to a specified one.

        Parameters
        ----------
        expression : str
            Target expression.
        indent_num : int
            Indentation number.

        Returns
        -------
        expression : str
            After appending expression.
        """
        from apysc._display import graphics_expression
        from apysc._display.graphics import Graphics
        graphics: Graphics = self.parent_graphics
        expression = graphics_expression.append_fill_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_fill_opacity_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_stroke_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_stroke_width_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_stroke_opacity_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_stroke_linecap_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_stroke_linejoin_expression(
            graphics=graphics, expression=expression,
            indent_num=indent_num)
        expression = graphics_expression.append_x_expression(
            graphic=self, expression=expression, indent_num=indent_num)
        expression = graphics_expression.append_y_expression(
            graphic=self, expression=expression, indent_num=indent_num)
        return expression
