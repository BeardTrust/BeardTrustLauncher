#!/usr/bin/env python3
import os
import signal

import wx
import wx.xrc

import scripts.start


def graphical_user_interface():
    """
    This function instantiates the graphical user interface and launches the primary application loop.

    :return: None           this function does not return a value
    """
    app = wx.App()
    page = main_page(None)
    page.Show()
    app.MainLoop()


class main_page(wx.Frame):
    """
    This class represents the primary frame, or window, of the graphical user interface.  It encapsulates
    all of the logic for transferring information from the interface to the scripts that perform the
    business logic of the application.
    """

    def __init__(self, parent):
        """
        The constructor for the main page takes a parent object as an argument and assembles the main
        page object.

        :param parent: wx.Frame             the wx.Frame object that is responsible for this object
        """
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"BeardTrust Launcher", pos=wx.DefaultPosition,
                          size=wx.Size(500, 300), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.__root_directory = ''
        self.__configuration = ''
        self.__profile = ''
        self.__child_processes = []
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
        """
        This is the accessor for the root directory property.

        :return: str            the object's root directory
        """

        return self.__root_directory

    @property
    def configuration(self):
        """
        This is the accessor for the configuration property.

        :return: str            the object's configuration
        """

        return self.__configuration

    @property
    def profile(self):
        """
        This is the accessor for the profile property.

        :return: str            the object's spring profile
        """

        return self.__profile

    @property
    def child_processes(self):
        """
        This is the accessor for the child processes property.

        :return: process[]      the list of child processes
        """
        return self.__child_processes

    def __del__(self):
        """
        The main page object's destructor.

        :return: None           this method does not return a value
        """

        pass

    def set_root_directory(self, event):
        """
        This method modifies the main page's root directory property whenever the
        directory picker or its associated text control are changed.

        :param event: Event     the onChange event fired by the directory picker
        :return: None           this method does not return a value
        """

        self.__root_directory = self.m_dirPicker2.GetPath()

    def set_configuration(self, event):
        """
        This method modifies the main page object's configuration property
        whenever the configuration selector is changed.

        :param event: Event     the onChange event fired by the configuration selector
        :return: None           this method does not return a value
        """

        # To be implemented!
        event.Skip()

    def set_profile(self, event):
        """
        This method modifies the main page object's profile property whenever the profile
        selector is changed.

        :param event: Event     the onChange event fired by the profile selector
        :return: None           this method does not return a value
        """

        self.__profile = self.profile_choice_box.GetString(self.profile_choice_box.GetSelection())

    def on_cancel(self, event):
        """
        This method exits the BeardTrust Launcher, closing any applications opened by the Launcher
        in the process.

        :param event: Event     the onClick event fired by the cancel button
        :return: int            the integer representation of the c-style system error code
        """

        for process in self.__child_processes:
            os.kill(process.pid, signal.SIGINT)
        exit(0)

    def on_ok(self, event):
        """
        This method passes the current profile property of the main page object to the script that
        handles the launching of Maven-based Spring Boot applications.

        :param event: Event     the onClick event fired by the ok button
        :return: None           this method does not return a value
        """
        self.__profile = self.profile_choice_box.GetString(self.profile_choice_box.GetSelection())
        self.__child_processes.append(scripts.start.run_spring_boot_microservice(self.root_directory, self.profile))
