#!/usr/bin/env python3

import os
import subprocess

import wx
import wx.xrc
import scripts.start


def graphical_user_interface():
    app = wx.App()
    page = main_page(None)
    page.Show()
    app.MainLoop()


class main_page(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"BeardTrust Launcher", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.__root_directory = ''
        self.__configuration = ''
        self.__profile = ''
        self.SetSizeHints(wx.Size(500, 300), wx.Size(500, 300))

        vertical_sizer_one = wx.BoxSizer(wx.VERTICAL)

        first_row = wx.BoxSizer(wx.HORIZONTAL)

        first_row_first_column = wx.BoxSizer(wx.VERTICAL)

        self.root_directory_label = wx.StaticText(self, wx.ID_ANY, u"Project Root Directory", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.root_directory_label.Wrap(-1)

        first_row_first_column.Add(self.root_directory_label, 0, wx.ALL | wx.EXPAND, 5)

        first_row.Add(first_row_first_column, 1, wx.ALIGN_BOTTOM, 5)

        first_row_second_column = wx.BoxSizer(wx.VERTICAL)

        self.m_dirPicker2 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                             wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_USE_TEXTCTRL)
        first_row_second_column.Add(self.m_dirPicker2, 5, wx.ALL | wx.EXPAND, 5)

        first_row.Add(first_row_second_column, 3, wx.ALIGN_BOTTOM, 5)

        vertical_sizer_one.Add(first_row, 1, wx.EXPAND, 5)

        second_row = wx.BoxSizer(wx.HORIZONTAL)

        second_row_first_column = wx.BoxSizer(wx.VERTICAL)

        self.configuration_label = wx.StaticText(self, wx.ID_ANY, u"Configuration", wx.DefaultPosition, wx.DefaultSize,
                                                 0)
        self.configuration_label.Wrap(-1)

        second_row_first_column.Add(self.configuration_label, 1, wx.ALIGN_TOP | wx.ALL, 10)

        second_row.Add(second_row_first_column, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        second_row_second_column = wx.BoxSizer(wx.VERTICAL)

        configuration_choice_boxChoices = []
        self.configuration_choice_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                  configuration_choice_boxChoices, 0)
        self.configuration_choice_box.SetSelection(0)
        second_row_second_column.Add(self.configuration_choice_box, 0, wx.ALIGN_LEFT | wx.ALL | wx.EXPAND, 5)

        second_row.Add(second_row_second_column, 2, wx.ALIGN_CENTER_VERTICAL, 5)

        second_row_third_column = wx.BoxSizer(wx.VERTICAL)

        self.profile_label = wx.StaticText(self, wx.ID_ANY, u"Profile", wx.DefaultPosition, wx.DefaultSize, 0)
        self.profile_label.Wrap(-1)

        second_row_third_column.Add(self.profile_label, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        second_row.Add(second_row_third_column, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        second_row_fourth_column = wx.BoxSizer(wx.VERTICAL)

        profile_choice_boxChoices = ['dev', 'production']

        self.profile_choice_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            profile_choice_boxChoices, 0)
        self.profile_choice_box.SetSelection(0)
        second_row_fourth_column.Add(self.profile_choice_box, 0, wx.ALL | wx.EXPAND, 5)

        second_row.Add(second_row_fourth_column, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, 5)

        vertical_sizer_one.Add(second_row, 1, wx.EXPAND, 5)

        third_row = wx.BoxSizer(wx.HORIZONTAL)

        third_row_first_column = wx.BoxSizer(wx.VERTICAL)

        third_row_first_column.Add((0, 0), 1, wx.EXPAND, 5)

        third_row.Add(third_row_first_column, 1, wx.EXPAND, 5)

        third_row_second_column = wx.BoxSizer(wx.VERTICAL)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize();

        third_row_second_column.Add(m_sdbSizer1, 1, wx.ALIGN_RIGHT, 10)

        third_row.Add(third_row_second_column, 1, wx.EXPAND, 5)

        vertical_sizer_one.Add(third_row, 1, wx.EXPAND, 5)

        self.SetSizer(vertical_sizer_one)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_dirPicker2.Bind(wx.EVT_DIRPICKER_CHANGED, self.set_root_directory)
        self.configuration_choice_box.Bind(wx.EVT_CHOICE, self.set_configuration)
        self.profile_choice_box.Bind(wx.EVT_CHOICE, self.set_profile)
        self.m_sdbSizer1Cancel.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.on_ok)


    @property
    def root_directory(self):
        return self.__root_directory

    @property
    def configuration(self):
        return self.__configuration

    @property
    def profile(self):
        return self.__profile

    def __del__(self):
        pass

    def set_root_directory(self, event):
        self.__root_directory = self.m_dirPicker2.GetPath()

    def set_configuration(self, event):
        # To be implemented!
        event.Skip()

    def set_profile(self, event):
        self.__profile = self.profile_choice_box.GetString(self.profile_choice_box.GetSelection())

    def on_cancel(self, event):
        exit(0)

    def on_ok(self, event):
        self.__profile = self.profile_choice_box.GetString(self.profile_choice_box.GetSelection())
        scripts.start.start_application(self.root_directory, self.profile)

