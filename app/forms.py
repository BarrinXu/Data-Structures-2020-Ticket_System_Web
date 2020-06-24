from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, BooleanField, RadioField, TimeField
from wtforms.fields import html5, core
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class RegisterForm(FlaskForm):
    # cur_name = StringField('当前用户', validators=[DataRequired(), Length(max=20)])
    username = StringField('用户名', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=30)])
    confirm = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    name = StringField('昵称', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(min=1, max=30)])
    privilege = IntegerField('优先级', validators=[DataRequired()])
    submit = SubmitField('注册')

    def validate_privilege(self, privilege):
        tmp = int(privilege.data)
        if tmp < 0 or tmp > 10:
            raise ValidationError('优先级输入错误')


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=30)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class QueryUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(max=20)])
    submit1 = SubmitField('查询')


class EditUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('密码')
    confirm = PasswordField('确认密码', validators=[EqualTo('password')])
    name = StringField('昵称')
    email = StringField('邮箱')
    privilege = StringField('优先级')
    submit2 = SubmitField('提交修改')


class AddTrainForm(FlaskForm):
    trainID = StringField('车次名称', validators=[DataRequired(), Length(max=20)])
    stationNum = IntegerField('车站数', validators=[DataRequired()])
    seatNum = IntegerField('座位数', validators=[DataRequired()])
    stations = StringField('所经车站，用空格隔开', validators=[DataRequired()])
    prices = StringField('区间票价，用空格隔开', validators=[DataRequired()])
    startTimes = html5.TimeField('出发时刻', format='%H:%M')
    travelTimes = StringField('区间时长，用空格隔开', validators=[DataRequired()])
    stopoverTimes = StringField('靠站时间，用空格隔开', validators=[DataRequired()])
    startSaleDate = html5.DateField('起售日期')
    endSaleDate = html5.DateField('结售日期')
    type = StringField('列车类型', validators=[DataRequired()])
    submit1 = SubmitField('添加')


class ReleaseTrainForm(FlaskForm):
    releaseID = StringField('车次名称', validators=[DataRequired(), Length(max=20)])
    submit2 = SubmitField('发布')


class DeleteTrainForm(FlaskForm):
    deleteID = StringField('车次名称', validators=[DataRequired(), Length(max=20)])
    submit3 = SubmitField('删除')


class QueryTrainForm(FlaskForm):
    QueryID = StringField('车次名称', validators=[DataRequired(), Length(max=20)])
    QueryDate = html5.DateField('出发日期')
    submit4 = SubmitField('查询')


class QueryTicketForm(FlaskForm):
    Dep = StringField('出发站', validators=[DataRequired()])
    Arr = StringField('到达站', validators=[DataRequired()])
    Date = html5.DateField('出发日期', validators=[DataRequired()])
    Sort = RadioField(validators=[DataRequired()], choices=[('time', '时间优先'), ('cost', '价格优先')], default='time')
    Ways = RadioField(validators=[DataRequired()], choices=[('query_ticket', '直达'), ('query_transfer', '换乘一次')],
                      default='query_ticket')
    submit1 = SubmitField('查询')


class BuyTicketForm(FlaskForm):
    ID = StringField('车次名称', validators=[DataRequired()])
    DT = html5.DateField('出发日期', validators=[DataRequired()])
    NM = IntegerField('票数', validators=[DataRequired()])
    ST = StringField('出发站', validators=[DataRequired()])
    ED = StringField('到达站', validators=[DataRequired()])
    choice = RadioField(validators=[DataRequired()], choices=[('false', '不接受候补'), ('true', '接受候补购票')], default='false')
    submit2 = SubmitField('提交订单')

