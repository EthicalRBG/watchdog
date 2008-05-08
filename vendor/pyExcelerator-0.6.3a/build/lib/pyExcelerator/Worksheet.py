#!/usr/bin/env python
# -*- coding: windows-1251 -*-

#  Copyright (C) 2005 Roman V. Kiseliov
#  All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#
#  3. All advertising materials mentioning features or use of this
#     software must display the following acknowledgment:
#     "This product includes software developed by
#      Roman V. Kiseliov <roman@kiseliov.ru>."
#
#  4. Redistributions of any form whatsoever must retain the following
#     acknowledgment:
#     "This product includes software developed by
#      Roman V. Kiseliov <roman@kiseliov.ru>."
#
#  THIS SOFTWARE IS PROVIDED BY Roman V. Kiseliov ``AS IS'' AND ANY
#  EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL Roman V. Kiseliov OR
#  ITS CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
#  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
#  HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
#  STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
#  OF THE POSSIBILITY OF SUCH DAMAGE.


'''
            BOF
            UNCALCED
            INDEX
            Calculation Settings Block
            PRINTHEADERS
            PRINTGRIDLINES
            GRIDSET
            GUTS
            DEFAULTROWHEIGHT
            WSBOOL
            Page Settings Block
            Worksheet Protection Block
            DEFCOLWIDTH
            COLINFO
            SORT
            DIMENSIONS
            Row Blocks
            WINDOW2
            SCL
            PANE
            SELECTION
            STANDARDWIDTH
            MERGEDCELLS
            LABELRANGES
            PHONETIC
            Conditional Formatting Table
            Hyperlink Table
            Data Validity Table
            SHEETLAYOUT (BIFF8X only)
            SHEETPROTECTION (BIFF8X only)
            RANGEPROTECTION (BIFF8X only)
            EOF
'''

__rev_id__ = """$Id: Worksheet.py,v 1.7 2005/08/11 08:53:48 rvk Exp $"""


import BIFFRecords
import Bitmap
import Formatting
import Style
from Deco import *


class Worksheet(object):
    from Workbook import Workbook

    #################################################################
    ## Constructor
    #################################################################
    @accepts(object, (str, unicode), Workbook)
    def __init__(self, sheetname, parent_book):
        import Row
        self.Row = Row.Row

        import Column
        self.Column = Column.Column

        self.__name = sheetname
        self.__parent = parent_book

        self.__rows = {}
        self.__cols = {}
        self.__merged_ranges = []
        self.__bmp_rec = ''

        self.__show_formulas = 0
        self.__show_grid = 1
        self.__show_headers = 1
        self.__panes_frozen = 0
        self.__show_empty_as_zero = 1
        self.__auto_colour_grid = 1
        self.__cols_right_to_left = 0
        self.__show_outline = 1
        self.__remove_splits = 0
        self.__selected = 0
        self.__hidden = 0
        self.__page_preview = 0

        self.__first_visible_row = 0
        self.__first_visible_col = 0
        self.__grid_colour = 0x40
        self.__preview_magn = 0
        self.__normal_magn = 0

        self.__vert_split_pos = None
        self.__horz_split_pos = None
        self.__vert_split_first_visible = None
        self.__horz_split_first_visible = None
        self.__split_active_pane = None

        self.__row_gut_width = 0
        self.__col_gut_height = 0

        self.__show_auto_page_breaks = 1
        self.__dialogue_sheet = 0
        self.__auto_style_outline = 0
        self.__outline_below = 0
        self.__outline_right = 0
        self.__fit_num_pages = 0
        self.__show_row_outline = 1
        self.__show_col_outline = 1
        self.__alt_expr_eval = 0
        self.__alt_formula_entries = 0

        self.__row_default_height = 0x00FF
        self.__col_default_width = 0x0008

        self.__calc_mode = 1
        self.__calc_count = 0x0064
        self.__RC_ref_mode = 1
        self.__iterations_on = 0
        self.__delta = 0.001
        self.__save_recalc = 0

        self.__print_headers = 0
        self.__print_grid = 0
        self.__grid_set = 1
        self.__vert_page_breaks = []
        self.__horz_page_breaks = []
        self.__header_str = '&P'
        self.__footer_str = '&F'
        self.__print_centered_vert = 0
        self.__print_centered_horz = 1
        self.__left_margin = 0.3 #0.5
        self.__right_margin = 0.3 #0.5
        self.__top_margin = 0.61 #1.0
        self.__bottom_margin = 0.37 #1.0
        self.__paper_size_code = 9 # A4
        self.__print_scaling = 100
        self.__start_page_number = 1
        self.__fit_width_to_pages = 1
        self.__fit_height_to_pages = 1
        self.__print_in_rows = 1
        self.__portrait = 1
        self.__print_not_colour = 0
        self.__print_draft = 0
        self.__print_notes = 0
        self.__print_notes_at_end = 0
        self.__print_omit_errors = 0
        self.__print_hres = 0x012C # 300 dpi
        self.__print_vres = 0x012C # 300 dpi
        self.__header_margin = 0.1
        self.__footer_margin = 0.1
        self.__copies_num = 1

        self.__wnd_protect = 0
        self.__obj_protect = 0
        self.__protect = 0
        self.__scen_protect = 0
        self.__password = ''

    #################################################################
    ## Properties, "getters", "setters"
    #################################################################

    @accepts(object, (str, unicode))
    def set_name(self, value):
        self.__name = value

    def get_name(self):
        return self.__name

    name = property(get_name, set_name)

    #################################################################

    def get_parent(self):
        return self.__parent

    parent = property(get_parent)

    #################################################################

    def get_rows(self):
        return self.__rows

    rows = property(get_rows)

    #################################################################

    def get_cols(self):
        return self.__cols

    cols = property(get_cols)

    #################################################################

    def get_merged_ranges(self):
        return self.__merged_ranges

    merged_ranges = property(get_merged_ranges)

    #################################################################

    def get_bmp_rec(self):
        return self.__bmp_rec

    bmp_rec = property(get_bmp_rec)

    #################################################################

    @accepts(object, bool)
    def set_show_formulas(self, value):
        self.__show_formulas = int(value)

    def get_show_formulas(self):
        return bool(self.__show_formulas)

    show_formulas = property(get_show_formulas, set_show_formulas)

    #################################################################

    @accepts(object, bool)
    def set_show_grid(self, value):
        self.__show_grid = int(value)

    def get_show_grid(self):
        return bool(self.__show_grid)

    show_grid = property(get_show_grid, set_show_grid)

    #################################################################

    @accepts(object, bool)
    def set_show_headers(self, value):
        self.__show_headers = int(value)

    def get_show_headers(self):
        return bool(self.__show_headers)

    show_headers = property(get_show_headers, set_show_headers)

    #################################################################

    @accepts(object, bool)
    def set_panes_frozen(self, value):
        self.__panes_frozen = int(value)

    def get_panes_frozen(self):
        return bool(self.__panes_frozen)

    panes_frozen = property(get_panes_frozen, set_panes_frozen)

    #################################################################

    @accepts(object, bool)
    def set_show_empty_as_zero(self, value):
        self.__show_empty_as_zero = int(value)

    def get_show_empty_as_zero(self):
        return bool(self.__show_empty_as_zero)

    show_empty_as_zero = property(get_show_empty_as_zero, set_show_empty_as_zero)

    #################################################################

    @accepts(object, bool)
    def set_auto_colour_grid(self, value):
        self.__auto_colour_grid = int(value)

    def get_auto_colour_grid(self):
        return bool(self.__auto_colour_grid)

    auto_colour_grid = property(get_auto_colour_grid, set_auto_colour_grid)

    #################################################################

    @accepts(object, bool)
    def set_cols_right_to_left(self, value):
        self.__cols_right_to_left = int(value)

    def get_cols_right_to_left(self):
        return bool(self.__cols_right_to_left)

    cols_right_to_left = property(get_cols_right_to_left, set_cols_right_to_left)

    #################################################################

    @accepts(object, bool)
    def set_show_outline(self, value):
        self.__show_outline = int(value)

    def get_show_outline(self):
        return bool(self.__show_outline)

    show_outline = property(get_show_outline, set_show_outline)

    #################################################################

    @accepts(object, bool)
    def set_remove_splits(self, value):
        self.__remove_splits = int(value)

    def get_remove_splits(self):
        return bool(self.__remove_splits)

    remove_splits = property(get_remove_splits, set_remove_splits)

    #################################################################

    @accepts(object, bool)
    def set_selected(self, value):
        self.__selected = int(value)

    def get_selected(self):
        return bool(self.__selected)

    selected = property(get_selected, set_selected)

    #################################################################

    @accepts(object, bool)
    def set_hidden(self, value):
        self.__hidden = int(value)

    def get_hidden(self):
        return bool(self.__hidden)

    hidden = property(get_hidden, set_hidden)

    #################################################################

    @accepts(object, bool)
    def set_page_preview(self, value):
        self.__page_preview = int(value)

    def get_page_preview(self):
        return bool(self.__page_preview)

    page_preview = property(get_page_preview, set_page_preview)

    #################################################################

    @accepts(object, int)
    def set_first_visible_row(self, value):
        self.__first_visible_row = value

    def get_first_visible_row(self):
        return self.__first_visible_row

    first_visible_row = property(get_first_visible_row, set_first_visible_row)

    #################################################################

    @accepts(object, int)
    def set_first_visible_col(self, value):
        self.__first_visible_col = value

    def get_first_visible_col(self):
        return self.__first_visible_col

    first_visible_col = property(get_first_visible_col, set_first_visible_col)

    #################################################################

    @accepts(object, int)
    def set_grid_colour(self, value):
        self.__grid_colour = value

    def get_grid_colour(self):
        return self.__grid_colour

    grid_colour = property(get_grid_colour, set_grid_colour)

    #################################################################

    @accepts(object, int)
    def set_preview_magn(self, value):
        self.__preview_magn = value

    def get_preview_magn(self):
        return self.__preview_magn

    preview_magn = property(get_preview_magn, set_preview_magn)

    #################################################################

    @accepts(object, int)
    def set_normal_magn(self, value):
        self.__normal_magn = value

    def get_normal_magn(self):
        return self.__normal_magn

    normal_magn = property(get_normal_magn, set_normal_magn)

    #################################################################

    @accepts(object, int)
    def set_vert_split_pos(self, value):
        self.__vert_split_pos = abs(value)

    def get_vert_split_pos(self):
        return self.__vert_split_pos

    vert_split_pos = property(get_vert_split_pos, set_vert_split_pos)

    #################################################################

    @accepts(object, int)
    def set_horz_split_pos(self, value):
        self.__horz_split_pos = abs(value)

    def get_horz_split_pos(self):
        return self.__horz_split_pos

    horz_split_pos = property(get_horz_split_pos, set_horz_split_pos)

    #################################################################

    @accepts(object, int)
    def set_vert_split_first_visible(self, value):
        self.__vert_split_first_visible = abs(value)

    def get_vert_split_first_visible(self):
        return self.__vert_split_first_visible

    vert_split_first_visible = property(get_vert_split_first_visible, set_vert_split_first_visible)

    #################################################################

    @accepts(object, int)
    def set_horz_split_first_visible(self, value):
        self.__horz_split_first_visible = abs(value)

    def get_horz_split_first_visible(self):
        return self.__horz_split_first_visible

    horz_split_first_visible = property(get_horz_split_first_visible, set_horz_split_first_visible)

    #################################################################

    #@accepts(object, int)
    #def set_split_active_pane(self, value):
    #    self.__split_active_pane = abs(value) & 0x03
    #
    #def get_split_active_pane(self):
    #    return self.__split_active_pane
    #
    #split_active_pane = property(get_split_active_pane, set_split_active_pane)

    #################################################################

    #@accepts(object, int)
    #def set_row_gut_width(self, value):
    #    self.__row_gut_width = value
    #
    #def get_row_gut_width(self):
    #    return self.__row_gut_width
    #
    #row_gut_width = property(get_row_gut_width, set_row_gut_width)
    #
    #################################################################
    #
    #@accepts(object, int)
    #def set_col_gut_height(self, value):
    #    self.__col_gut_height = value
    #
    #def get_col_gut_height(self):
    #    return self.__col_gut_height
    #
    #col_gut_height = property(get_col_gut_height, set_col_gut_height)
    #
    #################################################################

    @accepts(object, bool)
    def set_show_auto_page_breaks(self, value):
        self.__show_auto_page_breaks = int(value)

    def get_show_auto_page_breaks(self):
        return bool(self.__show_auto_page_breaks)

    show_auto_page_breaks = property(get_show_auto_page_breaks, set_show_auto_page_breaks)

    #################################################################

    @accepts(object, bool)
    def set_dialogue_sheet(self, value):
        self.__dialogue_sheet = int(value)

    def get_dialogue_sheet(self):
        return bool(self.__dialogue_sheet)

    dialogue_sheet = property(get_dialogue_sheet, set_dialogue_sheet)

    #################################################################

    @accepts(object, bool)
    def set_auto_style_outline(self, value):
        self.__auto_style_outline = int(value)

    def get_auto_style_outline(self):
        return bool(self.__auto_style_outline)

    auto_style_outline = property(get_auto_style_outline, set_auto_style_outline)

    #################################################################

    @accepts(object, bool)
    def set_outline_below(self, value):
        self.__outline_below = int(value)

    def get_outline_below(self):
        return bool(self.__outline_below)

    outline_below = property(get_outline_below, set_outline_below)

    #################################################################

    @accepts(object, bool)
    def set_outline_right(self, value):
        self.__outline_right = int(value)

    def get_outline_right(self):
        return bool(self.__outline_right)

    outline_right = property(get_outline_right, set_outline_right)

    #################################################################

    @accepts(object, int)
    def set_fit_num_pages(self, value):
        self.__fit_num_pages = value

    def get_fit_num_pages(self):
        return self.__fit_num_pages

    fit_num_pages = property(get_fit_num_pages, set_fit_num_pages)

    #################################################################

    @accepts(object, bool)
    def set_show_row_outline(self, value):
        self.__show_row_outline = int(value)

    def get_show_row_outline(self):
        return bool(self.__show_row_outline)

    show_row_outline = property(get_show_row_outline, set_show_row_outline)

    #################################################################

    @accepts(object, bool)
    def set_show_col_outline(self, value):
        self.__show_col_outline = int(value)

    def get_show_col_outline(self):
        return bool(self.__show_col_outline)

    show_col_outline = property(get_show_col_outline, set_show_col_outline)

    #################################################################

    @accepts(object, bool)
    def set_alt_expr_eval(self, value):
        self.__alt_expr_eval = int(value)

    def get_alt_expr_eval(self):
        return bool(self.__alt_expr_eval)

    alt_expr_eval = property(get_alt_expr_eval, set_alt_expr_eval)

    #################################################################

    @accepts(object, bool)
    def set_alt_formula_entries(self, value):
        self.__alt_formula_entries = int(value)

    def get_alt_formula_entries(self):
        return bool(self.__alt_formula_entries)

    alt_formula_entries = property(get_alt_formula_entries, set_alt_formula_entries)

    #################################################################

    @accepts(object, int)
    def set_row_default_height(self, value):
        self.__row_default_height = value

    def get_row_default_height(self):
        return self.__row_default_height

    row_default_height = property(get_row_default_height, set_row_default_height)

    #################################################################

    @accepts(object, int)
    def set_col_default_width(self, value):
        self.__col_default_width = value

    def get_col_default_width(self):
        return self.__col_default_width

    col_default_width = property(get_col_default_width, set_col_default_width)

    #################################################################

    @accepts(object, int)
    def set_calc_mode(self, value):
        self.__calc_mode = value & 0x03

    def get_calc_mode(self):
        return self.__calc_mode

    calc_mode = property(get_calc_mode, set_calc_mode)

    #################################################################

    @accepts(object, int)
    def set_calc_count(self, value):
        self.__calc_count = value

    def get_calc_count(self):
        return self.__calc_count

    calc_count = property(get_calc_count, set_calc_count)

    #################################################################

    @accepts(object, bool)
    def set_RC_ref_mode(self, value):
        self.__RC_ref_mode = int(value)

    def get_RC_ref_mode(self):
        return bool(self.__RC_ref_mode)

    RC_ref_mode = property(get_RC_ref_mode, set_RC_ref_mode)

    #################################################################

    @accepts(object, bool)
    def set_iterations_on(self, value):
        self.__iterations_on = int(value)

    def get_iterations_on(self):
        return bool(self.__iterations_on)

    iterations_on = property(get_iterations_on, set_iterations_on)

    #################################################################

    @accepts(object, float)
    def set_delta(self, value):
        self.__delta = value

    def get_delta(self):
        return self.__delta

    delta = property(get_delta, set_delta)

    #################################################################

    @accepts(object, bool)
    def set_save_recalc(self, value):
        self.__save_recalc = int(value)

    def get_save_recalc(self):
        return bool(self.__save_recalc)

    save_recalc = property(get_save_recalc, set_save_recalc)

    #################################################################

    @accepts(object, bool)
    def set_print_headers(self, value):
        self.__print_headers = int(value)

    def get_print_headers(self):
        return bool(self.__print_headers)

    print_headers = property(get_print_headers, set_print_headers)

    #################################################################

    @accepts(object, bool)
    def set_print_grid(self, value):
        self.__print_grid = int(value)

    def get_print_grid(self):
        return bool(self.__print_grid)

    print_grid = property(get_print_grid, set_print_grid)

    #################################################################
    #
    #@accepts(object, bool)
    #def set_grid_set(self, value):
    #    self.__grid_set = int(value)
    #
    #def get_grid_set(self):
    #    return bool(self.__grid_set)
    #
    #grid_set = property(get_grid_set, set_grid_set)
    #
    #################################################################

    @accepts(object, list)
    def set_vert_page_breaks(self, value):
        self.__vert_page_breaks = value

    def get_vert_page_breaks(self):
        return self.__vert_page_breaks

    vert_page_breaks = property(get_vert_page_breaks, set_vert_page_breaks)

    #################################################################

    @accepts(object, list)
    def set_horz_page_breaks(self, value):
        self.__horz_page_breaks = value

    def get_horz_page_breaks(self):
        return self.__horz_page_breaks

    horz_page_breaks = property(get_horz_page_breaks, set_horz_page_breaks)

    #################################################################

    @accepts(object, (str, unicode))
    def set_header_str(self, value):
        self.__header_str = value

    def get_header_str(self):
        return self.__header_str

    header_str = property(get_header_str, set_header_str)

    #################################################################

    @accepts(object, (str, unicode))
    def set_footer_str(self, value):
        self.__footer_str = value

    def get_footer_str(self):
        return self.__footer_str

    footer_str = property(get_footer_str, set_footer_str)

    #################################################################

    @accepts(object, bool)
    def set_print_centered_vert(self, value):
        self.__print_centered_vert = int(value)

    def get_print_centered_vert(self):
        return bool(self.__print_centered_vert)

    print_centered_vert = property(get_print_centered_vert, set_print_centered_vert)

    #################################################################

    @accepts(object, bool)
    def set_print_centered_horz(self, value):
        self.__print_centered_horz = int(value)

    def get_print_centered_horz(self):
        return bool(self.__print_centered_horz)

    print_centered_horz = property(get_print_centered_horz, set_print_centered_horz)

    #################################################################

    @accepts(object, float)
    def set_left_margin(self, value):
        self.__left_margin = value

    def get_left_margin(self):
        return self.__left_margin

    left_margin = property(get_left_margin, set_left_margin)

    #################################################################

    @accepts(object, float)
    def set_right_margin(self, value):
        self.__right_margin = value

    def get_right_margin(self):
        return self.__right_margin

    right_margin = property(get_right_margin, set_right_margin)

    #################################################################

    @accepts(object, float)
    def set_top_margin(self, value):
        self.__top_margin = value

    def get_top_margin(self):
        return self.__top_margin

    top_margin = property(get_top_margin, set_top_margin)

    #################################################################

    @accepts(object, float)
    def set_bottom_margin(self, value):
        self.__bottom_margin = value

    def get_bottom_margin(self):
        return self.__bottom_margin

    bottom_margin = property(get_bottom_margin, set_bottom_margin)

    #################################################################

    @accepts(object, int)
    def set_paper_size_code(self, value):
        self.__paper_size_code = value

    def get_paper_size_code(self):
        return self.__paper_size_code

    paper_size_code = property(get_paper_size_code, set_paper_size_code)

    #################################################################

    @accepts(object, int)
    def set_print_scaling(self, value):
        self.__print_scaling = value

    def get_print_scaling(self):
        return self.__print_scaling

    print_scaling = property(get_print_scaling, set_print_scaling)

    #################################################################

    @accepts(object, int)
    def set_start_page_number(self, value):
        self.__start_page_number = value

    def get_start_page_number(self):
        return self.__start_page_number

    start_page_number = property(get_start_page_number, set_start_page_number)

    #################################################################

    @accepts(object, int)
    def set_fit_width_to_pages(self, value):
        self.__fit_width_to_pages = value

    def get_fit_width_to_pages(self):
        return self.__fit_width_to_pages

    fit_width_to_pages = property(get_fit_width_to_pages, set_fit_width_to_pages)

    #################################################################

    @accepts(object, int)
    def set_fit_height_to_pages(self, value):
        self.__fit_height_to_pages = value

    def get_fit_height_to_pages(self):
        return self.__fit_height_to_pages

    fit_height_to_pages = property(get_fit_height_to_pages, set_fit_height_to_pages)

    #################################################################

    @accepts(object, bool)
    def set_print_in_rows(self, value):
        self.__print_in_rows = int(value)

    def get_print_in_rows(self):
        return bool(self.__print_in_rows)

    print_in_rows = property(get_print_in_rows, set_print_in_rows)

    #################################################################

    @accepts(object, bool)
    def set_portrait(self, value):
        self.__portrait = int(value)

    def get_portrait(self):
        return bool(self.__portrait)

    portrait = property(get_portrait, set_portrait)

    #################################################################

    @accepts(object, bool)
    def set_print_colour(self, value):
        self.__print_not_colour = int(not value)

    def get_print_colour(self):
        return not bool(self.__print_not_colour)

    print_colour = property(get_print_colour, set_print_colour)

    #################################################################

    @accepts(object, bool)
    def set_print_draft(self, value):
        self.__print_draft = int(value)

    def get_print_draft(self):
        return bool(self.__print_draft)

    print_draft = property(get_print_draft, set_print_draft)

    #################################################################

    @accepts(object, bool)
    def set_print_notes(self, value):
        self.__print_notes = int(value)

    def get_print_notes(self):
        return bool(self.__print_notes)

    print_notes = property(get_print_notes, set_print_notes)

    #################################################################

    @accepts(object, bool)
    def set_print_notes_at_end(self, value):
        self.__print_notes_at_end = int(value)

    def get_print_notes_at_end(self):
        return bool(self.__print_notes_at_end)

    print_notes_at_end = property(get_print_notes_at_end, set_print_notes_at_end)

    #################################################################

    @accepts(object, bool)
    def set_print_omit_errors(self, value):
        self.__print_omit_errors = int(value)

    def get_print_omit_errors(self):
        return bool(self.__print_omit_errors)

    print_omit_errors = property(get_print_omit_errors, set_print_omit_errors)

    #################################################################

    @accepts(object, int)
    def set_print_hres(self, value):
        self.__print_hres = value

    def get_print_hres(self):
        return self.__print_hres

    print_hres = property(get_print_hres, set_print_hres)

    #################################################################

    @accepts(object, int)
    def set_print_vres(self, value):
        self.__print_vres = value

    def get_print_vres(self):
        return self.__print_vres

    print_vres = property(get_print_vres, set_print_vres)

    #################################################################

    @accepts(object, float)
    def set_header_margin(self, value):
        self.__header_margin = value

    def get_header_margin(self):
        return self.__header_margin

    header_margin = property(get_header_margin, set_header_margin)

    #################################################################

    @accepts(object, float)
    def set_footer_margin(self, value):
        self.__footer_margin = value

    def get_footer_margin(self):
        return self.__footer_margin

    footer_margin = property(get_footer_margin, set_footer_margin)

    #################################################################

    @accepts(object, int)
    def set_copies_num(self, value):
        self.__copies_num = value

    def get_copies_num(self):
        return self.__copies_num

    copies_num = property(get_copies_num, set_copies_num)

    ##################################################################

    @accepts(object, bool)
    def set_wnd_protect(self, value):
        self.__wnd_protect = int(value)

    def get_wnd_protect(self):
        return bool(self.__wnd_protect)

    wnd_protect = property(get_wnd_protect, set_wnd_protect)

    #################################################################

    @accepts(object, bool)
    def set_obj_protect(self, value):
        self.__obj_protect = int(value)

    def get_obj_protect(self):
        return bool(self.__obj_protect)

    obj_protect = property(get_obj_protect, set_obj_protect)

    #################################################################

    @accepts(object, bool)
    def set_protect(self, value):
        self.__protect = int(value)

    def get_protect(self):
        return bool(self.__protect)

    protect = property(get_protect, set_protect)

    #################################################################

    @accepts(object, bool)
    def set_scen_protect(self, value):
        self.__scen_protect = int(value)

    def get_scen_protect(self):
        return bool(self.__scen_protect)

    scen_protect = property(get_scen_protect, set_scen_protect)

    #################################################################

    @accepts(object, str)
    def set_password(self, value):
        self.__password = value

    def get_password(self):
        return self.__password

    password = property(get_password, set_password)

    ##################################################################
    ## Methods
    ##################################################################

    def get_parent(self):
        return self.__parent

    def write(self, r, c, label="", style=Style.XFStyle()):
        self.row(r).write(c, label, style)

    def merge(self, r1, r2, c1, c2, style=Style.XFStyle()):
        self.row(r1).write_blanks(c1, c2,  style)
        for r in range(r1+1, r2+1):
            self.row(r).write_blanks(c1, c2,  style)
        self.__merged_ranges.append((r1, r2, c1, c2))

    def write_merge(self, r1, r2, c1, c2, label="", style=Style.XFStyle()):
        self.merge(r1, r2, c1, c2, style)
        self.write(r1, c1,  label, style)

    def insert_bitmap(self, filename, row, col, x = 0, y = 0, scale_x = 1, scale_y = 1):
        bmp = Bitmap.ImDataBmpRecord(filename)
        obj = Bitmap.ObjBmpRecord(row, col, self, bmp, x, y, scale_x, scale_y)

        self.__bmp_rec += obj.get() + bmp.get()

    def col(self, indx):
        if indx not in self.__cols:
            self.__cols[indx] = self.Column(indx, self)
        return self.__cols[indx]

    def row(self, indx):
        if indx not in self.__rows:
            self.__rows[indx] = self.Row(indx, self)
        return self.__rows[indx]

    def row_height(self, row): # in pixels
        if row in self.__rows:
            return self.__rows[row].get_height_in_pixels()
        else:
            return 17

    def col_width(self, col): # in pixels
        #if col in self.__cols:
        #    return self.__cols[col].width_in_pixels()
        #else:
            return 64

    def get_labels_count(self):
        result = 0
        for r in self.__rows:
            result += self.__rows[r].get_str_count()
        return result

    ##################################################################
    ## BIFF records generation
    ##################################################################

    def __bof_rec(self):
        return BIFFRecords.Biff8BOFRecord(BIFFRecords.Biff8BOFRecord.WORKSHEET).get()

    def __guts_rec(self):
        row_visible_levels = 0
        if len(self.__rows) != 0:
            row_visible_levels = max([self.__rows[r].level for r in self.__rows]) + 1

        col_visible_levels = 0
        if len(self.__cols) != 0:
            col_visible_levels = max([self.__cols[c].level for c in self.__cols]) + 1

        return BIFFRecords.GutsRecord(self.__row_gut_width, self.__col_gut_height, row_visible_levels, col_visible_levels).get()

    def __wsbool_rec(self):
        options = 0x00
        options |= (self.__show_auto_page_breaks & 0x01) << 0
        options |= (self.__dialogue_sheet & 0x01) << 4
        options |= (self.__auto_style_outline & 0x01) << 5
        options |= (self.__outline_below & 0x01) << 6
        options |= (self.__outline_right & 0x01) << 7
        options |= (self.__fit_num_pages & 0x01) << 8
        options |= (self.__show_row_outline & 0x01) << 10
        options |= (self.__show_col_outline & 0x01) << 11
        options |= (self.__alt_expr_eval & 0x01) << 14
        options |= (self.__alt_formula_entries & 0x01) << 15

        return BIFFRecords.WSBoolRecord(options).get()

    def __eof_rec(self):
        return BIFFRecords.EOFRecord().get()

    def __colinfo_rec(self):
        result = ''
        for col in self.__cols:
            result += self.__cols[col].get_biff_record()
        return result

    def __dimensions_rec(self):
        first_used_row = 0
        last_used_row = 0
        first_used_col = 0
        last_used_col = 0
        if len(self.__rows) > 0:
            first_used_row = min(self.__rows)
            last_used_row = max(self.__rows)
            first_used_col = 0xFFFFFFFF
            last_used_col = 0
            for r in self.__rows:
                _min = self.__rows[r].get_min_col()
                _max = self.__rows[r].get_max_col()
                if _min < first_used_col:
                    first_used_col = _min
                if _max > last_used_col:
                    last_used_col = _max

        return BIFFRecords.DimensionsRecord(first_used_row, last_used_row, first_used_col, last_used_col).get()

    def __window2_rec(self):
        options = 0
        options |= (self.__show_formulas        & 0x01) << 0
        options |= (self.__show_grid            & 0x01) << 1
        options |= (self.__show_headers         & 0x01) << 2
        options |= (self.__panes_frozen         & 0x01) << 3
        options |= (self.__show_empty_as_zero   & 0x01) << 4
        options |= (self.__auto_colour_grid     & 0x01) << 5
        options |= (self.__cols_right_to_left   & 0x01) << 6
        options |= (self.__show_outline         & 0x01) << 7
        options |= (self.__remove_splits        & 0x01) << 8
        options |= (self.__selected             & 0x01) << 9
        options |= (self.__hidden               & 0x01) << 10
        options |= (self.__page_preview         & 0x01) << 11

        return BIFFRecords.Window2Record(options, self.__first_visible_row, self.__first_visible_col,
                                        self.__grid_colour,
                                        self.__preview_magn, self.__normal_magn).get()

    def __panes_rec(self):
        if self.__vert_split_pos is None and self.__horz_split_pos is None:
            return ""

        if self.__vert_split_pos is None:
            self.__vert_split_pos = 0
        if self.__horz_split_pos is None:
            self.__horz_split_pos = 0

        if self.__panes_frozen:
            if self.__vert_split_first_visible is None:
                self.__vert_split_first_visible = self.__vert_split_pos
            if self.__horz_split_first_visible is None:
                self.__horz_split_first_visible = self.__horz_split_pos
        else:
            if self.__vert_split_first_visible is None:
                self.__vert_split_first_visible = 0
            if self.__horz_split_first_visible is None:
                self.__horz_split_first_visible = 0
            # inspired by pyXLWriter
            self.__horz_split_pos = 20*self.__horz_split_pos + 255
            self.__vert_split_pos = 113.879*self.__vert_split_pos + 390

        if self.__vert_split_pos > 0 and self.__horz_split_pos > 0:
            self.__split_active_pane = 0
        elif self.__vert_split_pos > 0 and self.__horz_split_pos == 0:
            self.__split_active_pane = 1
        elif self.__vert_split_pos == 0 and self.__horz_split_pos > 0:
            self.__split_active_pane = 2
        else:
            self.__split_active_pane = 3

        result = BIFFRecords.PanesRecord(self.__vert_split_pos,
                                         self.__horz_split_pos,
                                         self.__horz_split_first_visible,
                                         self.__vert_split_first_visible,
                                         self.__split_active_pane).get()
        return result

    def __row_blocks_rec(self):
        # this function takes almost 99% of overall execution time 
        # when file is saved
        # return '' 
        result = []
        i = 0
        used_rows = self.__rows.keys()
        while i < len(used_rows):
            j = 0
            while i < len(used_rows) and (j < 32):
                result.append(self.__rows[used_rows[i]].get_row_biff_data())
                result.append(self.__rows[used_rows[i]].get_cells_biff_data())
                j += 1
                i += 1

        return ''.join(result)

    def __merged_rec(self):
        return BIFFRecords.MergedCellsRecord(self.__merged_ranges).get()

    def __bitmaps_rec(self):
        return self.__bmp_rec

    def __calc_settings_rec(self):
        result = ''
        result += BIFFRecords.CalcModeRecord(self.__calc_mode & 0x01).get()
        result += BIFFRecords.CalcCountRecord(self.__calc_count & 0xFFFF).get()
        result += BIFFRecords.RefModeRecord(self.__RC_ref_mode & 0x01).get()
        result += BIFFRecords.IterationRecord(self.__iterations_on & 0x01).get()
        result += BIFFRecords.DeltaRecord(self.__delta).get()
        result += BIFFRecords.SaveRecalcRecord(self.__save_recalc & 0x01).get()
        return result

    def __print_settings_rec(self):
        result = ''
        result += BIFFRecords.PrintHeadersRecord(self.__print_headers).get()
        result += BIFFRecords.PrintGridLinesRecord(self.__print_grid).get()
        result += BIFFRecords.GridSetRecord(self.__grid_set).get()
        result += BIFFRecords.HorizontalPageBreaksRecord(self.__horz_page_breaks).get()
        result += BIFFRecords.VerticalPageBreaksRecord(self.__vert_page_breaks).get()
        result += BIFFRecords.HeaderRecord(self.__header_str).get()
        result += BIFFRecords.FooterRecord(self.__footer_str).get()
        result += BIFFRecords.HCenterRecord(self.__print_centered_horz).get()
        result += BIFFRecords.VCenterRecord(self.__print_centered_vert).get()
        result += BIFFRecords.LeftMarginRecord(self.__left_margin).get()
        result += BIFFRecords.RightMarginRecord(self.__right_margin).get()
        result += BIFFRecords.TopMarginRecord(self.__top_margin).get()
        result += BIFFRecords.BottomMarginRecord(self.__bottom_margin).get()

        setup_page_options =  (self.__print_in_rows & 0x01) << 0
        setup_page_options |=  (self.__portrait & 0x01) << 1
        setup_page_options |=  (0x00 & 0x01) << 2
        setup_page_options |=  (self.__print_not_colour & 0x01) << 3
        setup_page_options |=  (self.__print_draft & 0x01) << 4
        setup_page_options |=  (self.__print_notes & 0x01) << 5
        setup_page_options |=  (0x00 & 0x01) << 6
        setup_page_options |=  (0x01 & 0x01) << 7
        setup_page_options |=  (self.__print_notes_at_end & 0x01) << 9
        setup_page_options |=  (self.__print_omit_errors & 0x03) << 10

        result += BIFFRecords.SetupPageRecord(self.__paper_size_code,
                                self.__print_scaling,
                                self.__start_page_number,
                                self.__fit_width_to_pages,
                                self.__fit_height_to_pages,
                                setup_page_options,
                                self.__print_hres,
                                self.__print_vres,
                                self.__header_margin,
                                self.__footer_margin,
                                self.__copies_num).get()
        return result

    def __protection_rec(self):
        result = ''
        result += BIFFRecords.ProtectRecord(self.__protect).get()
        result += BIFFRecords.ScenProtectRecord(self.__scen_protect).get()
        result += BIFFRecords.WindowProtectRecord(self.__wnd_protect).get()
        result += BIFFRecords.ObjectProtectRecord(self.__obj_protect).get()
        result += BIFFRecords.PasswordRecord(self.__password).get()
        return result

    def get_biff_data(self):
        result = ''
        result += self.__bof_rec()
        result += self.__calc_settings_rec()
        result += self.__guts_rec()
        result += self.__wsbool_rec()
        result += self.__colinfo_rec()
        result += self.__dimensions_rec()
        result += self.__print_settings_rec()
        result += self.__protection_rec()
        result += self.__row_blocks_rec()
        result += self.__merged_rec()
        result += self.__bitmaps_rec()
        result += self.__window2_rec()
        result += self.__panes_rec()
        result += self.__eof_rec()

        return result



