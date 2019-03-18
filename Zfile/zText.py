__author__ = "zanweb <zanweb@163.com>"


class TextFile(object):
    def __init__(self, file_with_path):
        self.file_with_path = file_with_path
        self.return_info = None

    def get_lysaght_order(self):
        try:
            with open(self.file_with_path) as f:
                lines = f.readlines()
                line_list = []
                for line in lines:
                    line_del = line.strip('\n')
                    line_info = line_del.split(' ', 1)
                    line_list.append(line_info)
                self.return_info = dict(line_list)
                f.close()
        except Exception as e:
            print(e)
        finally:
            return self.return_info


if __name__ == '__main__':
    txt_f = TextFile('../testfiles/order.txt')
    txt_info = txt_f.get_lysaght_order()
    print(txt_info)
