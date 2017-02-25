from django.db import models

from django.utils.timezone import datetime


class SeparatedValuesField(models.TextField):
    """
        Usage:
            class Foo(models.Model):
                bar = SeparatedValuesField()
            _list = [1, '2', date.today()]
            obj = Foo.objects.create(bar=_list)
            assert obj.bar == _list
        """

    #__metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        self.date_format = kwargs.pop('date_format', "%d/%m/%Y")
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    #def from_db_value(self, value, expression, connection, context):


    def to_python(self, value):
        dt_str = lambda dt: datetime.strptime(dt, self.date_format).date()
        if not value:
            return
        if isinstance(value, list):
            return value
        _list = []
        for x in value.split(self.token):
            try:
                _list.append(dt_str(x))
            except ValueError:
                if x.isdigit():
                    _list.append(int(x))
                else:
                    _list.append(x)
        return _list

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value:
            return
        _list = []
        for _str in value:
            if isinstance(_str, datetime):
                _str = _str.strftime(self.date_format)
            elif _str is None:
                _str = ''
            _list.append(unicode(_str))

        return self.token.join(_list)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
