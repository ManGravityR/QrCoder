import glob
from datetime import datetime
from pathlib import Path
from colorama import init, Fore, Back, Style
from Package import Package

from QrCoder import QrCoder


class EventManager(object):
    """Events Manager

    Choose option from menu:
    > Help usage\t\t\t\t - show context help

    > Select your source file\t - select CSV, JSON, XML file with data
    \t - Select file from current path

    > Generate from source file\t - run generate QR codes from selected file
    \t - All QR images are saved to a directory by the source file name

    > Exit the program\t\t\t - exit form program :)
    """

    def __init__(self):
        """Events Manager Constructor
        """

        init()

        self.pkg = Package()

        # Connect Qr Class
        self.qr = QrCoder()

        # Registry all events
        self._eventsRegistry = {}

        # Current event worker
        self._this_event = None

        """
        # self._events     - Events Items
        # self._events     - this list -> dict for many events
        # Example: [{'name': 'select_file', 'method': 'select_file'}, {'name': 'select_file', 'method': 'select_file'}]
        # 
        # self._events     - this dict for one event
        # Example: {'name': 'select_file', 'method': 'select_file'}

        # Supported keys
        # - title       As view title menu item
        # - name        Unique Name for item
        # - method      Event method name (def. as `name`)
        # - property    Props for item
        """
        self._events = [
            {
                'title': 'Help usage',
                'name': 'help_usage',
            },
            {
                'title': 'Select source file',
                'name': 'select_file',
                # 'method': 'select_file',
                # 'property': 'select_file'
            },
            {
                'title': 'Generate from source file',
                'name': 'generate',
            },
            {
                'title': 'Exit the program',
                'name': 'exit',
            }
        ]
        self.menu()

    @classmethod
    def __name__(cls):
        return str(cls.__name__)

    def menu(self):
        # Menu wrapper for first run
        print(self.pkg.package_info())
        print('=== MENU ===')
        print('Hey! Here is what I can do:')
        while True:
            self._menu_items()

    def _menu_items(self):
        # Show Menu items

        index = 1
        for event in self._events:
            prop = ''
            try:
                if hasattr(__class__, 'select_file') and event['name'] == 'select_file' and self.qr.src_fullname:
                    prop = f"(selected: {self.qr.src_fullname})"
            except KeyError:
                prop = ''

            index_item = "%s%s%s" % (Style.BRIGHT + Fore.RED, index, Style.RESET_ALL)
            title_item = "%s%s%s" % (Fore.GREEN, event['title'], Style.RESET_ALL)
            print("\t%s. %s %s" % (index_item, title_item, prop))
            index = index + 1

        response = None
        while not isinstance(response, int):
            try:
                response = int(input('I have a choose: '))
                response = response - 1
            except ValueError:
                continue

        try:
            if self._events[response] in self._events:
                self.execute(self._events[response])
        except IndexError:
            print('Oooh... Are you serious? Come on again.')

    def _register(self):
        # Register event task

        self._eventsRegistry.update(
            {
                id(self._this_event):
                    {
                        'id': id(self._this_event),
                        'event': self._this_event,
                        'time': datetime.now().strftime('%m.%d.%Y %H:%M:%S.%f')
                    }
            })

    def _register_status(self, status):
        # Mutable event status task in Register
        self._eventsRegistry[id(self._this_event)]['status'] = status

    def _prepare(self):
        # Prepare event model

        if 'name' not in self._this_event:
            raise KeyError('Important Event field `name` not exits')

        fields = ['method', 'property']
        for field in fields:
            if field not in self._this_event:
                self._this_event[field] = self._this_event['name']

        if self._this_event['method'].startswith('event_') is False:
            self._this_event['method'] = f"event_{self._this_event['method']}"

    def events(self, events=[]):
        pass

    # @staticmethod
    def execute(self, events):
        """
        Run event input node
        :mutable: true
        """

        if isinstance(events, list):
            for event in events:
                self.execute(event)

        if not isinstance(events, dict):
            raise TypeError('Event dictionary not found')

        self._this_event = events

        try:
            self._prepare()
            self._register()
        except KeyError as e:
            raise e

        if callable(getattr(__class__, self._this_event['method'])):
            value = getattr(__class__, self._this_event['method'])(self)
            if value is not [None, False]:
                setattr(__class__, self._this_event['name'], value)
                self._register_status(1)
        else:
            raise RuntimeError(f"Event {self._this_event['name']} not exist or not callable")

    def event_help_usage(self):
        """
        View doc-block for Supported Classes
        """
        objects = [self, self.qr]

        for obj in objects:
            print(f"\r\nMethods {obj.__name__()}")  # Method Heading

            for func in dir(obj):
                __obj = getattr(obj, func)
                if callable(__obj) \
                        and (not func.startswith("__") or func.startswith("__init__")) \
                        and not func.endswith("Class"):
                    if func == "__init__":
                        scope = 'Description: '
                        func = ''
                    elif func.startswith("_"):
                        scope = 'private'
                    else:
                        scope = 'public'
                        func = f'{func}()'

                    if __obj.__doc__ is not None:
                        print(f'\t%s %s' % (scope, func), __obj.__doc__)
        print(f"=============\r\n")

    @staticmethod
    def event_select_file(self):
        """
        Event input filename
        """
        files = [f for ext in self.qr.supported_exts for f in glob.glob(f'*.{ext}')]

        if not files:
            raise RuntimeError(
                'No files found. Required list with extensions: (%s)' % ', '.join(self.qr.supported_exts)
            )

        print(f'Select data source file')
        index = 1

        for file in files:
            index_item = "%s%s%s" % (Style.BRIGHT + Fore.RED, index, Style.RESET_ALL)
            file_item = "%s%s%s" % (Fore.GREEN, file, Style.RESET_ALL)
            print(f'\t%s. %s' % (index_item, file_item))
            index = index + 1
        file = int(input(f'I have a choose > '))

        file = file - 1
        if file == '':
            return self.execute({'name': 'select_file'})

        my_file = Path(files[file])
        if not my_file.is_file():
            print(f'File named {my_file} does not exist')
            return self.execute({'name': 'select_file'})

        # Confirmation Event
        response = True
        response = input(f'Are you sure and want to continue with the file {Fore.GREEN}{Style.BRIGHT}{my_file}{Style.RESET_ALL}? [Y/n]\r\n')

        # Failure
        if response == 'n' or response == 'N':
            return self.execute({'name': 'select_file'})

        # Success
        if response or response == '' or response == 'Y' or response == 'y':
            print(f'File {my_file} selected for generation')
            setattr(__class__, 'select_file', str(my_file))
            self.qr.data_filename(str(my_file))

    def event_generate(self):
        """
        Make qr codes from selected list
        """
        while hasattr(__class__, 'select_file') is False:
            print('Source file not specified. Select a file first!')
            self.execute({'name': 'select_file'})
        self.qr.make()

    @staticmethod
    def event_exit(self):
        """
        Exit from program
        """
        print('The program was stopped by the user')
        exit(1)