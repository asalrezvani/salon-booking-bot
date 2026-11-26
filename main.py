import telebot
from telebot.types import ReplyKeyboardMarkup,ReplyKeyboardRemove,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from telebot.util import antiflood
from config import *
from texts import *
import datetime
import jdatetime
import logging
from DML import *
from DQL import *


API_TOKEN = db_config1['API_TOKEN']
channel_cid = int(db_config1['channel_cid'])
admins = eval(db_config1['admins'])

bot = telebot.TeleBot(API_TOKEN)
hideboard = ReplyKeyboardRemove()
commands = {
    'start'  : text["start"], 
    'help'   : text["help"]
}
admin_commands = {
        'add_category'       : text['category'],
        'add_service'        : text['service'],
        'add_personnel'      : text['personnel'],
        'add_capacity'       : text['capacity'],
        'show_taking_turns'  : text['taking_turns'],
        'show_customers'     : text['customers'],
        'add_day_off'        : text["day_off"],
}
message_ids = {
    text["start"]          : 2,
    text["help"]           : 4,
    text["birth_takhfif"]  : 6,
    text["call_us"]        : 8,
}

user_data = dict()
user_step = dict()
known_users = dict()

logging.basicConfig(filename="project.log",format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO)

def listener(message):
    for m in message:
        if m.content_type == 'text':
            logging.info(f' user input this [{m.text}] message.')
            print(f'{m.chat.first_name} [{m.chat.id}]: {m.text}')
        elif m.content_type == 'contact':
            print(f'{m.chat.first_name} [{m.chat.id}]: new contact recived.')
bot.set_update_listener(listener)

def send_message(*args, **kwargs):
    try:
        return antiflood(bot.send_message, *args, **kwargs)
    except telebot.apihelper.ApiTelegramException:
        print(f'bot was blocked by the user')
    except Exception as e:
        print(repr(e))

def create_calendar(year=None, month=None):
    today = jdatetime.date.today()
    if year == None:
        year = today.year
    if month == None:
        month = today.month

    monthes = [text['farvardin'],text['ordibehesht'],text['khordad'],text['tir'],text['mordad'],
        text['shahrivar'],text['mehr'],text['aban'],text['azar'],text['dey'],text['bahman'],text['esfand']]

    if month <= 6:
        month_days = 31
    elif month <= 11:
        month_days = 30
    elif jdatetime.date(year , 1,1).isleap():
        month_days = 30
    else:
        month_days = 29

    markup = InlineKeyboardMarkup(row_width=7)
    markup.add(InlineKeyboardButton('◀️', callback_data=f'month_prev_{year}_{month}'),
               InlineKeyboardButton(f'{monthes[month -1]} {year}', callback_data='month_title'),
               InlineKeyboardButton('▶️', callback_data=f'month_next_{year}_{month}'))
    markup.add(InlineKeyboardButton(text['saturday'], callback_data='saturday'),
               InlineKeyboardButton(text['sunday'], callback_data ='sunday'),
               InlineKeyboardButton(text['monday'], callback_data ='monday'),
               InlineKeyboardButton(text['tuesday'], callback_data ='tuesday'),
               InlineKeyboardButton(text['wednesday'], callback_data ='wednesday'),
               InlineKeyboardButton(text['thursday'], callback_data ='thursday'),
               InlineKeyboardButton(text['friday'], callback_data ='friday'))

    first_day = jdatetime.date(year, month ,1)
    start = first_day.weekday()
    week = []
    for _ in range(start):
        week.append(InlineKeyboardButton('.',callback_data='date_none'))
    for day in range(1, month_days+1):
        select_day = jdatetime.date(year,month,day)
        if select_day <= today:
            week.append(InlineKeyboardButton('❌', callback_data='date_none'))
        else:
            week.append(InlineKeyboardButton(str(day), callback_data=f'date_{year}_{month}_{day}'))
        if len(week) == 7:
            markup.add(*week)
            week = []
    if week:
        while len(week) < 7:
            week.append(InlineKeyboardButton('.', callback_data='date_none'))
    markup.add(*week)
    markup.add(InlineKeyboardButton(text['turn_back'], callback_data='turn_back'))
    return markup 

def create_times(cid):
    start_time = datetime.datetime.strptime("10:00", "%H:%M")
    closing_time = datetime.datetime.strptime("19:00", "%H:%M")
    service_id = user_data[cid]['service_id']
    pers_id = user_data[cid]['pers_id']
    date = user_data[cid]['date']
    pers_serv_id = get_personnel_service_data(pers_id,service_id)
    duration = get_service_duration(ID=service_id)
    taking_turns = get_taking_turn_data()
    markup = InlineKeyboardMarkup()
    buttons = []
    while start_time + duration <= closing_time:
        times = start_time.strftime("%H:%M")
        time_dalta = datetime.timedelta(hours=start_time.hour , minutes=start_time.minute)
        reserve = False  
        for taking_turn in taking_turns:
            if taking_turn['PERS_SERV_ID'] == pers_serv_id:
                if taking_turn['DATE'] == date:
                    if taking_turn['TIME'] == time_dalta:
                        if taking_turn['STATUS'] == 'reserved':
                            reserve = True
                            break
        if not reserve:
            buttons.append(InlineKeyboardButton(times , callback_data=f'time_{times}'))
        start_time += duration
    markup.add(*buttons)
    markup.add(InlineKeyboardButton(text['turn_back'], callback_data='turn_back2'))
    return markup

def birth_message():
    global known_users
    known_users = get_known_user()
    today = datetime.date.today()
    for cid, user in known_users.items():
        birth = user['BIRTH_DATE']
        if birth is not None:
            birth_month = birth.month
            birth_day = birth.day
            if today.month == birth_month:
                if today.day == birth_day:
                    bot.copy_message(cid, channel_cid, message_ids[text["birth_takhfif"]])
birth_message()

@bot.callback_query_handler(func= lambda call: call.data.startswith(('category','service')))
def callback_line_service_handler(call):
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    if data.startswith('category'):
        category_name = data.replace('category_', '',1)
        category_id = get_category_id(name= category_name)
        if cid not in user_data:
            user_data[cid] = {}
        user_data[cid]['category'] = category_name
        user_data[cid]['categ_id'] = category_id
        services = get_service_data(categ_id=category_id)
        markup = InlineKeyboardMarkup()
        buttons = []
        for service in services:
            buttons.append(InlineKeyboardButton(f'{service["NAME"]}', callback_data=f'service_{service["NAME"]}'))
        markup.add(*buttons)
        bot.answer_callback_query(call_id, text['call_service'])
        bot.edit_message_text(text['choose_service'], cid,mid, reply_markup=markup)
    
    elif data.startswith('service'):
        today = jdatetime.date.today()
        year = today.year
        month = today.month
        service_name = data.replace('service_', '')
        service_id = get_service_id(name=service_name)
        if cid not in user_data:
            user_data[cid] = {}
        user_data[cid]['service'] = service_name
        user_data[cid]['service_id'] = service_id
        new_markup = create_calendar(year , month)
        bot.answer_callback_query(call_id, text['date'])
        bot.edit_message_text(text['choose_date'], cid,mid, reply_markup=new_markup)
    else:
        bot.answer_callback_query(call_id, text['unknown_button'])
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)

@bot.callback_query_handler(func= lambda call: call.data.startswith(('month', 'date')))
def callback_month_date_handler(call):
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    if data.startswith('month'):
        _,move, year, month = data.split('_')
        if move == 'next':
            if int(month) == 12:
                year = int(year)+1
                new_month = 1
            else:
                new_month = int(month)+1
            bot.answer_callback_query(call_id, text['next_month'])
        elif move == 'prev':
            if int(month) == 1:
                year = int(year)-1
                new_month = 12
            else:
                new_month = int(month)-1
            bot.answer_callback_query(call_id, text['prev_month'])
        new_markup = create_calendar(int(year), int(new_month))
        bot.edit_message_reply_markup(cid, mid, reply_markup=new_markup)
        
    elif data.startswith('date'):
        if data.split('_')[1] == 'none':
            bot.answer_callback_query(call_id, text['date_none'])
        else:
            select_date = data.replace('date_','')
            if cid not in user_data:
                user_data[cid] = {}
            user_data[cid]['date'] = select_date
            service_id = user_data[cid]['service_id']
            personnel_ids = get_personnel_service_id(serv_id=service_id)
            markup = InlineKeyboardMarkup()
            buttons = []
            for personnel_id in personnel_ids:
                person = get_personnel_data(ID=personnel_id)
                buttons.append(InlineKeyboardButton(f'{person["NAME"]}',callback_data=f'person_{person["NAME"]}'))
            markup.add(*buttons)
            markup.add(InlineKeyboardButton(text['turn_back'], callback_data='turn_back1'))
            bot.answer_callback_query(call_id, text['list_personnel'])
            bot.edit_message_text(text['select_personnel'], cid, mid, reply_markup=markup)
    else:
        bot.answer_callback_query(call_id, text['unknown_button'])
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)

@bot.callback_query_handler(func= lambda call: call.data.startswith(('person','turn')))
def callback_personnel_handler(call):
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    if data.startswith('person'):
        personnel_name = data.replace('person_','')
        personnel_id = get_personnel_id(name=personnel_name)
        if cid not in user_data:
            user_data[cid] = {}
        user_data[cid]['personnel'] = personnel_name
        user_data[cid]['pers_id'] = personnel_id
        new_markup = create_times(cid)
        bot.answer_callback_query(call_id, text['time'])
        bot.edit_message_text(text['choose_time'], cid,mid, reply_markup=new_markup)
    elif data.startswith('turn'):
        if data == 'turn_back':
            category_id = user_data[cid]['categ_id']
            services = get_service_data(categ_id=category_id)
            markup = InlineKeyboardMarkup()
            buttons = []
            for service in services:
                buttons.append(InlineKeyboardButton(f'{service["NAME"]}', callback_data=f'service_{service["NAME"]}'))
            markup.add(*buttons)
            bot.answer_callback_query(call_id, text['call_service'])
            bot.edit_message_text(text['choose_service'], cid, mid, reply_markup=markup)
        elif data == 'turn_back1':
            new_markup = create_calendar()
            bot.answer_callback_query(call_id, text['calendar'])
            bot.edit_message_text(text['choose_date'], cid,mid, reply_markup=new_markup)
        elif data == 'turn_back2':
            service_id = user_data[cid]['service_id']
            personnel_ids = get_personnel_service_id(serv_id=service_id)
            markup = InlineKeyboardMarkup()
            buttons = []
            for personnel_id in personnel_ids:
                person = get_personnel_data(ID=personnel_id)
                buttons.append(InlineKeyboardButton(f'{person["NAME"]}',callback_data=f'person_{person["NAME"]}'))
            markup.add(*buttons)
            markup.add(InlineKeyboardButton(text['turn_back'], callback_data='turn_back1'))
            bot.answer_callback_query(call_id , text['list_personnel'])
            bot.edit_message_text(text['select_personnel'], cid,mid, reply_markup=markup)
    else:
        bot.answer_callback_query(call_id, text['unknown_button'])
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)

@bot.callback_query_handler(func= lambda call: call.data.startswith(('time','next')))
def callback_time_handler(call):
    global known_users
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    known_users = get_known_user()
    if data.startswith('time'):
        select_time = data.replace('time_', '')
        if cid not in user_data:
            user_data[cid] = {}
        user_data[cid]['hour'] = select_time
        if cid in known_users:
            name = known_users[cid]['NAME']
            service = user_data[cid]['service']
            date = user_data[cid]['date']
            personnel = user_data[cid]['personnel']
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton('❌', callback_data='cancel'),
               InlineKeyboardButton('✅', callback_data='ok'))
            bot.answer_callback_query(call_id, text['dar_hale_sabt'])
            bot.edit_message_text(text['reserv_message'].format(name,service,date,select_time,personnel),cid, mid, reply_markup=markup)
        else:
            bot.answer_callback_query(call_id, text['information'])
            bot.edit_message_text(text['full_name'],cid, mid, reply_markup=None)
            user_step[cid] = 'FN'
    elif data.startswith('next'):
        name = user_data[cid]['name']
        service = user_data[cid]['service']
        date = user_data[cid]['date']
        hour = user_data[cid]['hour']
        personnel = user_data[cid]['personnel']
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('❌', callback_data='cancel'),
                   InlineKeyboardButton('✅', callback_data='ok'))
        bot.answer_callback_query(call_id, text['dar_hale_sabt'])
        bot.edit_message_text(text['reserv_message'].format(name,service,date,hour,personnel),cid,mid, reply_markup=markup)
    else:
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
        bot.answer_callback_query(call_id, text['unknown_button'])

@bot.callback_query_handler(func= lambda call: call.data in ['ok', 'cancel'])
def callback_ok_cancel_handler(call):
    global known_users
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    known_users = get_known_user()
    if data == 'ok':
        birth = user_data[cid].setdefault('birth', None)
        if birth == None:
            birth1 = None
        else:
            birth1 = birth.togregorian()
        service = user_data[cid]['service']
        date = user_data[cid]['date']
        shamsi_date = jdatetime.date.strptime(date, '%Y_%m_%d')
        miladi_date = shamsi_date.togregorian()
        hour = user_data[cid]['hour']
        personnel = user_data[cid]['personnel']
        pers_id = user_data[cid]['pers_id']
        serv_id = user_data[cid]['service_id']
        pers_serv_id = get_personnel_service_data(pers_id=pers_id,serv_id=serv_id)
        if cid in known_users:
            user_name = known_users[cid]['NAME']
            taking_turn_data = insert_taking_turn_data(cust_id=cid,pers_serv_id=pers_serv_id,date=miladi_date,time=hour,status='reserved')
            bot.answer_callback_query(call_id, text['sabt'])
            bot.edit_message_text(text['reservation_message'].format(user_name,service,date,hour,personnel),cid ,mid, reply_markup=None)
        else:
            name = user_data[cid]['name']
            number = user_data[cid]['number']
            customer_data = insert_customer_data(cid=cid,name=name,phone=number,birth_date=birth1)
            taking_turn_data = insert_taking_turn_data(cust_id=cid,pers_serv_id=pers_serv_id,date=miladi_date,time=hour,status='reserved')
            bot.answer_callback_query(call_id, text['sabt'])
            bot.edit_message_text(text['reservation_message'].format(name,service,date,hour,personnel),cid ,mid, reply_markup=None)
            user_step.pop(cid)

    elif data == 'cancel':
        bot.answer_callback_query(call_id, text['laqv'])
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)
        bot.delete_message(cid, mid)

@bot.callback_query_handler(func= lambda call: call.data in ['yes', 'no'])
def callback_yes_no_handler(call):
    call_id = call.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    if data == 'yes':
        update_taking_turn_status(CUST_ID=cid)
        bot.answer_callback_query(call_id , text['laqv'])
        bot.edit_message_text(text['cancel'],cid, mid, reply_markup=None)
    elif data == 'no':
        bot.answer_callback_query(call_id, text['laqv'])
        bot.edit_message_reply_markup(cid, mid, reply_markup=None)

@bot.message_handler(commands=['start'])
def command_start_handler(message):
    cid = message.chat.id
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(text['call_us'], text["cancel_reserve"], text["reservation"])
    bot.copy_message(cid,channel_cid, message_ids[text["start"]], reply_markup=keyboard)

@bot.message_handler(commands=["help"])
def command_help_handler(message):
    cid = message.chat.id
    if cid in admins:
        x = f'****{text['admin']}****\n'
        for command, desc in admin_commands.items():
            x += f'/{command} : {desc}\n'
        send_message(cid, x)
    else:
        bot.copy_message(cid, channel_cid, message_ids[text["help"]])

@bot.message_handler(commands=['add_category'])
def cammand_add_category_handler(message):
    cid = message.chat.id
    if cid in admins:
        send_message(cid, text['add_category']+'\n'
f"""
{text['name']}:{text['category_name']}
""")
        user_step[cid] = 'AC'
    else:
        default_message(message)

@bot.message_handler(commands=['add_service'])
def command_add_service_handler(message):
    cid = message.chat.id
    if cid in admins:
        send_message(cid, text['add_service'] +'\n'
f"""
{text['line']}:{text['category_name']}
{text['khedmat']}:{text['service_name']}
{text['zaman']}:{text['duration']}
""")
        user_step[cid] = 'AS'
    else:
        default_message(message)

@bot.message_handler(commands=['add_personnel'])
def command_add_personnel_handler(message):
    cid = message.chat.id
    if cid in admins:
        send_message(cid, text['add_personnel'] +'\n'
f"""
{text['name']}:{text['personnel_name']}
{text['khedmat']}:{text['service_name1']},{text['service_name2']}
""")
        user_step[cid] = 'AP'
    else:
        default_message(message)

@bot.message_handler(commands=['add_capacity'])
def command_add_capacity_handler(message):
    cid = message.chat.id
    if cid in admins:
        send_message(cid, text['add_capacity'] + '\n'
f"""
{text['name']}:{text['personnel_name']}
{text['khedmat']}:{text['service_name']}
{text['rooz']}:{text['tarikh']}
{text['zarfiat']}:{text['tedad']}
""")
        user_step[cid] = 'PC'
    else:
        default_message(message)

@bot.message_handler(commands=['show_customers'])
def command_show_customer_handler(message):
    cid = message.chat.id
    if cid in admins:
        customers = get_customer_data()
        for customer in customers:
            admin_message=(
                    f'{text["cid"]} : {customer["CID"]}'+ '\n'
                    f'{text["name"]} : {customer["NAME"]}'+ '\n'
                    f'{text["phone"]} : {customer["PHONE"]}'+ '\n'
                    f'{text["birth"]} : {customer["BIRTH_DATE"]}'
            )
            send_message(cid, admin_message)
    else:
        default_message(message)

@bot.message_handler(commands=['show_taking_turns'])
def command_show_taking_turns(message):
    cid = message.chat.id
    if cid in admins:
        taking_turns = get_taking_turn_data()
        for taking_turn in taking_turns:
            admin_message=(
                f'{text["cust_id"]} : {taking_turn["CUST_ID"]}'+ '\n'
                f'{text["pers_serv_id"]} : {taking_turn["PERS_SERV_ID"]}'+ '\n'
                f'{text["tarikh1"]} : {taking_turn["DATE"]}'+ '\n'
                f'{text["hour"]} : {taking_turn["TIME"]}'+ '\n'
                f'{text["status"]} : {taking_turn["STATUS"]}'
            )
            send_message(cid, admin_message)
    else:
        default_message(message)

@bot.message_handler(commands=['add_day_off'])
def command_day_off_handler(message):
    cid = message.chat.id
    if cid in admins:
        send_message(cid, text['add_day_off'] + '\n'
f"""
{text['rooz']}:{text['tarikh']}
""")
        user_step[cid] = "DO"
    else:
        default_message(message)

@bot.message_handler(func= lambda message: message.text in [text["reservation"]])
def reservetion_handler(message):
    cid = message.chat.id
    markup = InlineKeyboardMarkup()
    categories = get_category_data()
    buttons = []
    for category in categories:
        buttons.append(InlineKeyboardButton(f'{category["NAME"]}',callback_data=f'category_{category["NAME"]}'))
    markup.add(*buttons)
    send_message(cid, text['choose_line'], reply_markup = markup)

@bot.message_handler(func= lambda message: message.text in [text['cancel_reserve']])
def cancel_reserve_handler(message):
    global known_users
    cid = message.chat.id
    known_users = get_known_user()
    today = datetime.date.today()
    turn_data = get_taking_turn_date(cust_id=cid)
    for date,status in turn_data.items():
        if cid in known_users:
            if date > today and status == 'reserved':
                markup = InlineKeyboardMarkup()
                markup.add(InlineKeyboardButton('❌',callback_data='no'),
                        InlineKeyboardButton('✅', callback_data='yes'))
                send_message(cid, text['ask_laqv'], reply_markup=markup)
            else:
                send_message(cid, text['no_cancel'])
        else:
            send_message(cid, text['no_cancel'])

@bot.message_handler(func= lambda message: message.text in [text["call_us"]])
def call_us_handler(message):
    cid = message.chat.id
    bot.copy_message(cid, channel_cid, message_ids[text["call_us"]])

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'AC')
def user_step_AC_hanlder(message):
    cid = message.chat.id
    category = message.text
    category_info = category.split('\n')
    category_name = category_info[0].split(':',1)[-1]
    category_id = insert_category_data(name=category_name)
    send_message(cid, f'{text['insert_category'].format(category_id)}')
    user_step.pop(cid)

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'AS')
def user_step_AS_handler(message):
    cid = message.chat.id
    service = message.text
    service_info = service.split('\n')
    category_name = service_info[0].split(':',1)[-1]
    service_name = service_info[1].split(':',1)[-1]
    duration = service_info[2].split(':',1)[-1]
    category_id = get_category_id(name=category_name)
    service_id = insert_service_data(categ_id=category_id, name=service_name, duration=duration)
    send_message(cid, f'{text['insert_service'].format(service_id)}')
    user_step.pop(cid)

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'AP')
def user_step_AP_handler(message):
    cid = message.chat.id
    personnel = message.text
    personnel_info = personnel.split('\n')
    personnel_name = personnel_info[0].split(':',1)[-1]
    service_name = personnel_info[1].split(':',1)[-1].split(',')
    service_names = [name for name in service_name]
    personnel_id = insert_personnel_data(name=personnel_name)
    for service_name in service_names:
        service_id = get_service_id(name=service_name)
        personnel_service = insert_personnel_service_data(pers_id=personnel_id,serv_id=service_id)
    send_message(cid, f'{text['insert_personnel'].format(personnel_id)}')
    user_step.pop(cid)

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'PC')
def user_step_PC_handler(message):
    cid = message.chat.id
    capacity = message.text
    capacity_info = capacity.split('\n')
    personnel_name = capacity_info[0].split(':',1)[-1]
    service_name = capacity_info[1].split(':',1)[-1]
    date = capacity_info[2].split(':',1)[-1]
    date1 = jdatetime.date.strptime(date, '%Y_%m_%d')
    date2 = date1.togregorian()
    max_capacity = capacity_info[3].split(':',1)[-1]
    personnel_id = get_personnel_id(name=personnel_name)
    service_id = get_service_id(name=service_name)
    pers_serv_id = get_personnel_service_data(pers_id=personnel_id,serv_id=service_id)
    capacity_id = insert_capacity_data(pers_serv_id=pers_serv_id,date=date2,max_capacity=int(max_capacity))
    send_message(cid, f'{text['insert_capacity'].format(capacity_id)}')
    user_step.pop(cid)

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'DO')
def user_step_DO_handler(message):
    cid = message.chat.id
    date = message.text
    date_info = date.split(':',1)[-1]
    days_off = date_info
    print(days_off)

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'FN')
def user_step_FN_handler(message):
    cid = message.chat.id
    full_name = message.text
    if cid not in user_data:
        user_data[cid] = {}
    user_data[cid]['name'] = full_name
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text['phone_number'], request_contact=True))
    send_message(cid, text['share_phone_number'], reply_markup=keyboard)

@bot.message_handler(func= lambda message: user_step.get(message.chat.id) == 'BD')
def user_step_BD_handler(message):
    cid = message.chat.id
    birth = message.text
    birth1 = jdatetime.date.strptime(birth, '%Y_%m_%d')
    if cid not in user_data:
        user_data[cid] = {}
    user_data[cid]['birth'] = birth1
    name = user_data[cid]['name']
    service = user_data[cid]['service']
    date = user_data[cid]['date']
    hour = user_data[cid]['hour']
    personnel = user_data[cid]['personnel']
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('❌', callback_data='cancel'),
               InlineKeyboardButton('✅', callback_data='ok'))
    send_message(cid, text['reserv_message'].format(name,service,date,hour,personnel),reply_markup=markup)
    user_step.pop(cid)

@bot.message_handler(content_types=['contact'])
def content_contact_handler(message):
    cid = message.chat.id
    contact = message.contact
    phone_number = message.contact.phone_number
    if cid == contact.user_id:
        if cid not in user_data:
            user_data[cid] = {}
        user_data[cid]['number'] = phone_number
        sent_message = send_message(cid, text['button_number'], reply_markup=hideboard)
        bot.delete_message(cid, sent_message.message_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text['next'], callback_data='next_step'))
        send_message(cid, text['birth_date'], reply_markup=markup)
        user_step[cid] = 'BD'

    elif cid != contact.user_id :
        send_message(cid, text['own_number'])

@bot.message_handler(func= lambda message: True, content_types=['text'])
def default_message(message):
    bot.reply_to(message.text , text['default_message'])

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)