import os
from pathlib import Path
import csv
import qrcode


class QrCoder(object):
    """
    Class QrCoder
    """

    def __init__(self, data_filename='template_list.csv'):
        """ QrCoder Constructor
        """
        self.src_filename = data_filename
        self.src_ext = None
        self.src_fullname = None
        self.supported_exts = ['csv']
        # self.supported_exts = ['csv', 'json', 'xml']
        self.save_root_dir = 'qr-codes'
        self.save_dir = None
        self.props = {}

        self.create_template()
        self.normalize_file(self.src_filename)

    @classmethod
    def __name__(cls):
        return str(cls.__name__)

    def create_template(self):
        template = Path('template_list.csv')
        if not template.is_file():
            with open(template, 'w', newline='') as csvfile:
                fieldnames = ['filename', 'text']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow({'filename': 'TextField', 'text': 'Spam ' * 5})
                writer.writerow({'filename': 'WebSite', 'text': 'https://stackoverflow.com'})

    def normalize_file(self, fn):
        """
        Normalize filename and extension
        """
        parts = fn.split('.')

        try:
            # set extension for source
            if parts[-1] in self.supported_exts:
                self.src_ext = str(parts.pop(-1))
                self.src_filename = str('.'.join(parts))
                self.src_fullname = str(f'{self.src_filename}.{self.src_ext}')
            else:
                raise RuntimeError('Extension parse error')

        except (IndexError, FileNotFoundError) as e:
            raise e

    def data_filename(self, fn=None):
        """
        Get or Set filename
        """
        if fn is None:
            return self.src_fullname

        self.normalize_file(fn)
        return self.src_fullname

    def mkdir(self):
        """
        Create directory
        :rtype: object
        """

        self.save_dir = f"{self.save_root_dir}/{self.src_filename}"
        if not os.path.exists(self.save_dir):
            try:
                os.makedirs(self.save_dir)
                return self.save_dir
            except OSError:
                print("Failed to create directory %s" % self.save_dir)
            else:
                print("Successfully created directory %s" % self.save_dir)

    def make(self):
        """
        Make qr-codes from file
        """
        with open(self.data_filename(), newline='') as csvfile:
            self.mkdir()
            csv_reader = csv.reader(csvfile, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are %s' % ", ".join(row))
                else:
                    self._qr_make(row[0], row[1])
                    print(f'\tMake QR with name %s and text body .' % (row[0], row[1]))
                line_count += 1
            print(f'Processed %s lines.' % line_count)
            print("Result saved to directory %s" % self.save_dir)

    def _qr_make(self, fn=None, text=None):
        # QR save process

        img = qrcode.make(text)
        img.save(f"{self.save_dir}/{fn}.png")