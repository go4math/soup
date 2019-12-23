''' helper functions '''
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from django.template.loader import render_to_string
from django.core.mail import send_mail

from soup.settings import BASE_URL

def pagination_helper(object_list, page, items_per_page=3):
    paginator = Paginator(object_list, items_per_page)
    items = paginator.get_page(page) # page is a string of number
    paginator_of_paginator=Paginator(paginator.page_range,8) # 8 is better looked on small screen
    page_of_paginator = paginator_of_paginator.get_page((int(page)-1)//8+1)
    return items, page_of_paginator


def confirm_required(login_url=None):

    actual_decorator = user_passes_test(
            lambda u: u.confirmed,
            login_url=login_url,
        )

    return actual_decorator

def send_confirmation_mail(user):

    token = user.generate_confirmation_token()
    confirm_link_external = 'http://'+BASE_URL+'confirm/'+token

    msg = "{}, 你好!\n感谢你的注册, 请在24小时内点击下面链接确认你的邮箱:\n{}\nSoup Team 致敬".format(user.username, confirm_link_external)
    html_msg = render_to_string('mail/confirmation.html',{'name': user.username, 'link':confirm_link_external})
    return send_mail('[Soup] 请确认你的邮箱',msg,'pjltest@outlook.com',
                [user.email], html_message=html_msg)
