from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
import re



class User(Form):
    mobile = fields.CharField(
        required=True,
        max_length=11,
        error_messages={'required': '手机号码不能为空', 'invaild': '手机号码格式不正确'}
    )

    mbpwd = fields.CharField(
        required=True,
        error_messages={'required': '密码不能为空'},
        widget=widgets.PasswordInput()
    )

    def clean_mobile(self):
        # 去取用户提交的值：可能是错误是的，也可能是正确的
        value = self.cleaned_data['mobile']
        mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
        if not mobile_re.match(value):
            raise ValidationError('手机号码格式错误')
        else:
            return value  # 这里必须要返回正确的值，因



class UrlCheck(Form):

    url = fields.URLField(
        required=True,
        error_messages={'required':'url不能为空','invalid':'链接地址格式不正确'}
    )
