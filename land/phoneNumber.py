__author__ = 'hudutech'


class PhoneNumberValidator():
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def validate(self):
        length = len(self.phone_number)
        phone_list = list(self.phone_number)
        prefix = phone_list[0]

        if prefix == '0' and length == 10:
            prefix = '+254'
            return
