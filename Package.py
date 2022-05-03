from colorama import init, Fore, Back, Style


class Package:
    def __init__(self):
        init()

        self.__app_name__ = 'QrCoder'
        self.__version__ = '0.1.0'

        self.packageInfo = {
            'Name': self.__app_name__,
            'Version': self.__version__,
            'buildDate': '2022-05-01'
        }

    def package_info(self):
        res = [self._set_color('> Package Info')]
        for k, v in self.packageInfo.items():
            res.append(self._set_color(text=f'\t%s : %s' % (k, v), fore=Fore.LIGHTCYAN_EX, bright=Style.NORMAL))
        res.append(self._set_color('========= <'))

        return '\r\n'.join(res)

    @staticmethod
    def _set_color(text=None, fore=Fore.CYAN, bright=Style.BRIGHT):
        return fore + bright + str(text) + Style.RESET_ALL
