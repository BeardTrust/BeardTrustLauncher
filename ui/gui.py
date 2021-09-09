#!/usr/bin/env python3

from subprocess import Popen

import wx
import wx.xrc

import scripts.process_management


def graphical_user_interface() -> None:
    """
    This function instantiates the graphical user interface and launches the primary application loop.

    :return: None           this function does not return a value
    """
    app = wx.App()
    # noinspection PyTypeChecker
    page = LauncherWindow(None)
    page.Show()
    app.MainLoop()


class LauncherWindow(wx.Frame):
    """
    This class represents the primary frame, or window, of the graphical user interface.  It encapsulates
    all of the logic for transferring information from the interface to the scripts that perform the
    business logic of the application.
    """

    def __init__(self, parent: wx.Frame) -> None:
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

        main_sizer = wx.BoxSizer(wx.VERTICAL)

        first_row = wx.BoxSizer(wx.HORIZONTAL)

        first_row_first_column = wx.BoxSizer(wx.VERTICAL)

        self.root_directory_label = wx.StaticText(self, wx.ID_ANY, u"Project Root Directory", wx.DefaultPosition,
                                                  wx.DefaultSize, 0)
        self.root_directory_label.Wrap(-1)

        first_row_first_column.Add(self.root_directory_label, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL | wx.BOTTOM, 13)

        first_row.Add(first_row_first_column, 1, wx.ALIGN_BOTTOM, 5)

        first_row_second_column = wx.BoxSizer(wx.VERTICAL)

        self.m_dirPicker2 = wx.DirPickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition,
                                             wx.DefaultSize, wx.DIRP_DEFAULT_STYLE | wx.DIRP_USE_TEXTCTRL)
        first_row_second_column.Add(self.m_dirPicker2, 5, wx.ALL | wx.EXPAND, 5)

        first_row.Add(first_row_second_column, 3, wx.ALIGN_BOTTOM, 5)

        main_sizer.Add(first_row, 1, wx.EXPAND | wx.ALL, 5)

        second_row = wx.BoxSizer(wx.HORIZONTAL)

        second_row_first_column = wx.BoxSizer(wx.VERTICAL)

        self.configuration_label = wx.StaticText(self, wx.ID_ANY, u"Configuration", wx.DefaultPosition, wx.DefaultSize,
                                                 0)
        self.configuration_label.Wrap(-1)

        second_row_first_column.Add(self.configuration_label, 1, wx.ALIGN_TOP | wx.ALL, 10)

        second_row.Add(second_row_first_column, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        second_row_second_column = wx.BoxSizer(wx.VERTICAL)

        configuration_choices = [u'All - Native', u'Spring-Boot', u'NPM', u'Yarn']
        self.configuration_choice_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                  configuration_choices, 0)
        self.configuration_choice_box.SetSelection(0)
        second_row_second_column.Add(self.configuration_choice_box, 0, wx.ALIGN_LEFT | wx.ALL | wx.EXPAND, 5)

        second_row.Add(second_row_second_column, 2, wx.ALIGN_CENTER_VERTICAL, 5)

        second_row_third_column = wx.BoxSizer(wx.VERTICAL)

        self.profile_label = wx.StaticText(self, wx.ID_ANY, u"Profile", wx.DefaultPosition, wx.DefaultSize, 0)
        self.profile_label.Wrap(-1)

        second_row_third_column.Add(self.profile_label, 0, wx.ALIGN_RIGHT | wx.ALL, 10)

        second_row.Add(second_row_third_column, 1, wx.ALIGN_CENTER_VERTICAL, 5)

        second_row_fourth_column = wx.BoxSizer(wx.VERTICAL)

        profile_choices = [u'dev', u'production']

        self.profile_choice_box = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            profile_choices, 0)
        self.profile_choice_box.SetSelection(0)
        second_row_fourth_column.Add(self.profile_choice_box, 0, wx.ALL | wx.EXPAND, 5)

        second_row.Add(second_row_fourth_column, 2, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT, 5)

        main_sizer.Add(second_row, 1, wx.EXPAND | wx.ALL, 5)

        third_row = wx.BoxSizer(wx.HORIZONTAL)

        third_row_first_column = wx.BoxSizer(wx.VERTICAL)

        third_row_first_column.Add((0, 0), 1, wx.EXPAND, 5)

        third_row.Add(third_row_first_column, 1, wx.EXPAND, 5)

        third_row_second_column = wx.BoxSizer(wx.VERTICAL)

        button_sizer = wx.StdDialogButtonSizer()
        self.ok_button = wx.Button(self, wx.ID_OK)
        button_sizer.AddButton(self.ok_button)
        self.cancel_button = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(self.cancel_button)
        button_sizer.Realize()

        third_row_second_column.Add(button_sizer, 1, wx.ALIGN_RIGHT, 10)

        third_row.Add(third_row_second_column, 1, wx.EXPAND, 5)

        main_sizer.Add(third_row, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.m_dirPicker2.Bind(wx.EVT_DIRPICKER_CHANGED, self.set_root_directory)
        self.configuration_choice_box.Bind(wx.EVT_CHOICE, self.set_configuration)
        self.profile_choice_box.Bind(wx.EVT_CHOICE, self.set_profile)
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_cancel)
        self.ok_button.Bind(wx.EVT_BUTTON, self.on_ok)

    @property
    def root_directory(self) -> str:
        """
        This is the accessor for the root directory property.

        :return: str            the object's root directory
        """

        return self.__root_directory

    @property
    def configuration(self) -> str:
        """
        This is the accessor for the configuration property.

        :return: str            the object's configuration
        """

        return self.__configuration

    @property
    def profile(self) -> str:
        """
        This is the accessor for the profile property.

        :return: str            the object's spring profile
        """

        return self.__profile

    @property
    def child_processes(self) -> list[Popen]:
        """
        This is the accessor for the child processes property.

        :return: process[]      the list of child processes
        """
        return self.__child_processes

    def __del__(self) -> None:
        """
        The main page object's destructor.

        :return: None           this method does not return a value
        """

        pass

    def set_root_directory(self, event) -> None:
        """
        This method modifies the main page's root directory property whenever the
        directory picker or its associated text control are changed.

        :return: None           this method does not return a value
        """

        event.Skip()
        self.__root_directory = self.m_dirPicker2.GetPath()

    def set_configuration(self, event) -> None:
        """
        This method modifies the main page object's configuration property
        whenever the configuration selector is changed.

        :return: None           this method does not return a value
        """

        event.Skip()
        self.__configuration = self.configuration_choice_box.GetString(self.configuration_choice_box.GetSelection())

    def set_profile(self, event) -> None:
        """
        This method modifies the main page object's profile property whenever the profile
        selector is changed.

        :return: None           this method does not return a value
        """

        event.Skip()
        self.__profile = self.profile_choice_box.GetString(self.profile_choice_box.GetSelection())

    def on_cancel(self, event) -> None:
        """
        This method exits the BeardTrust Launcher, closing any applications opened by the Launcher
        in the process.

        :return: None            this method does not return a value
        """

        exit_code = 0
        event.Skip()

        for process in self.__child_processes:
            exit_code += scripts.process_management.terminate_process(process)
        exit(exit_code)

    def on_ok(self, event) -> None:
        """
        This method passes the current profile property of the main page object to the script that
        handles the launching of Maven-based Spring Boot applications.

        :return: None           this method does not return a value
        """

        event.Skip()
        self.__profile = self.profile_choice_box.GetString(self.profile_choice_box.GetSelection())
        self.__configuration = self.configuration_choice_box.GetString(self.configuration_choice_box.GetSelection())

        if self.__configuration.lower() == 'spring-boot':
            self.__child_processes.append(
            scripts.process_management.run_spring_boot_microservice(self.root_directory, self.profile))
        elif self.__configuration.lower() == 'all - native':
            process_list = scripts.process_management.launch_all_applications(self.root_directory, self.profile)
            for process in process_list:
                self.__child_processes.append(process)
