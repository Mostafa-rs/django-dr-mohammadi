"""
Accounts Views
Mostafa Rasouli
mostafarasooli54@gmail.com
feb 2024
"""

import random
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.contrib import messages

from accounts.models import User, UserOtp
from accounts.forms import UserLoginForm, OtpForm
from utils import sms
from log.defines import save_log


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def get(self, request):
        ctx = {
            'form': self.form_class()
        }

        return render(request, self.template_name, ctx)

    def post(self, request):
        try:
            form = self.form_class(request.POST)

            if form.is_valid():
                phone = form.cleaned_data['phone']
                if not User.objects.filter(phone=phone).exists():
                    User.objects.create(phone=phone)

                if otps := UserOtp.objects.filter(phone=phone):
                    otps.delete()

                otp = random.randint(111111, 999999)
                response = sms.send_otp(phone, otp)

                if response:
                    UserOtp.objects.create(phone=phone, otp=otp, date=timezone.now(),
                                           expire=timezone.now() + timezone.timedelta(minutes=3))
                    request.session['user_phone'] = f'{phone}'

                    messages.add_message(request, 200, f'{otp}', 'success')
                    return redirect('accounts:login_confirm')

                save_log(request, 'ERR_POST_SMS_RES', 'UserLoginView', response)
                messages.add_message(request, 200, f'خطایی رخ داده! لطفا مجدد تلاش نمایید', 'warning')
                return redirect('accounts:login')

            ctx = {
                'form': form
            }
            save_log(request, 'ERR_POST_VALIDATION', 'UserLoginView', form.errors)
            return render(request, self.template_name, ctx)

        except Exception as e:
            save_log(request, 'ERR_POST', 'UserLoginView', e)
            messages.add_message(request, 200, f'خطایی رخ داده! لطفا مجدد تلاش نمایید', 'warning')
            return redirect('accounts:login')
            

class UserLoginConfirmView(View):
    form_class = OtpForm
    template_name = 'accounts/login-confirm.html'

    def get(self, request):
        ctx = {
            'form': self.form_class()
        }

        return render(request, self.template_name, ctx)

    def post(self, request):
        try:
            form = self.form_class(request.POST)

            if phone := request.session.get('user_phone'):
                if otp_obj := UserOtp.objects.filter(phone=phone, used_date__isnull=True).order_by('-date').first():
                    if form.is_valid():
                        otp = form.cleaned_data['otp']

                        if otp_obj.otp != otp:
                            messages.add_message(request, 200,
                                                 'کد تایید اشتباه است!', 'warning')
                            return redirect('accounts:login_confirm')

                        otp_obj.used_date = timezone.now()
                        otp_obj.save()

                        if timezone.now() >= otp_obj.expire:
                            messages.add_message(request, 200,
                                                 'کد تایید منقضی شده است!', 'warning')
                            otp_obj.delete()
                            del request.session['user_phone']
                            return redirect('accounts:login')

                        if user := User.objects.filter(phone=phone).first():
                            login(request, user)
                            messages.add_message(request, 200, 'با موفقیت وارد شدید!', 'success')
                            otp_obj.delete()
                            print(request.session.get('user_phone'))
                            del request.session['user_phone']

                            return redirect('accounts:login')

                        messages.add_message(request, 200, 'کاربر مورد نظر یافت نشد', 'warning')
                        save_log(request, 'ERR_POST_USER', 'UserLoginConfirmView', f'{phone} - user not found')
                        return redirect('accounts:login')

                    ctx = {
                        'form': form
                    }
                    save_log(request, 'ERR_POST_VALIDATION', 'UserLoginConfirmView', form.errors)
                    return render(request, self.template_name, ctx)

                messages.add_message(request, 200, f'خطایی رخ داده! لطفا مجدد تلاش نمایید', 'warning')
                return redirect('accounts:login')

            messages.add_message(request, 200, f'خطایی رخ داده! لطفا مجدد تلاش نمایید', 'warning')
            return redirect('accounts:login')

        except Exception as e:
            save_log(request, 'ERR_POST', 'UserLoginConfirmView', e)
            messages.add_message(request, 200, f'خطایی رخ داده! لطفا مجدد تلاش نمایید', 'warning')
            return redirect('accounts:login_confirm')

