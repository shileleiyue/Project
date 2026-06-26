import requests
import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import WeChatAccount, SyncLog
from core.models import Contact, Message, Conversation


@login_required
def account_list(request):
    accounts = WeChatAccount.objects.all()
    return render(request, 'wechat_accounts.html', {'accounts': accounts})


@login_required
def account_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        platform = request.POST.get('platform')
        if platform == 'wechat_work':
            corp_id = request.POST.get('corp_id')
            corp_secret = request.POST.get('corp_secret')
            config = {
                'corp_id': corp_id,
                'corp_secret': corp_secret,
            }
        elif platform == 'personal':
            config = {}
        elif platform == 'official_account':
            app_id = request.POST.get('app_id')
            app_secret = request.POST.get('app_secret')
            config = {
                'app_id': app_id,
                'app_secret': app_secret,
            }
        else:
            config = {}
        account = WeChatAccount.objects.create(
            name=name,
            platform=platform,
            config=config,
        )
        messages.success(request, f'微信账户「{name}」已创建')
        return redirect('wechat_bridge:account_list')
    return render(request, 'wechat_account_form.html')


@login_required
def account_edit(request, account_id):
    account = get_object_or_404(WeChatAccount, id=account_id)
    if request.method == 'POST':
        account.name = request.POST.get('name', account.name)
        if account.platform == 'wechat_work':
            account.config['corp_id'] = request.POST.get('corp_id', account.config.get('corp_id', ''))
            account.config['corp_secret'] = request.POST.get('corp_secret', account.config.get('corp_secret', ''))
        elif account.platform == 'official_account':
            account.config['app_id'] = request.POST.get('app_id', account.config.get('app_id', ''))
            account.config['app_secret'] = request.POST.get('app_secret', account.config.get('app_secret', ''))
        account.save()
        messages.success(request, f'微信账户「{account.name}」已更新')
        return redirect('wechat_bridge:account_list')
    return render(request, 'wechat_account_form.html', {'account': account})


@login_required
def account_delete(request, account_id):
    account = get_object_or_404(WeChatAccount, id=account_id)
    if request.method == 'POST':
        account.delete()
        messages.success(request, '微信账户已删除')
        return redirect('wechat_bridge:account_list')
    return render(request, 'wechat_account_confirm_delete.html', {'account': account})


@login_required
def test_connection(request, account_id):
    account = get_object_or_404(WeChatAccount, id=account_id)
    result = {'success': False, 'message': ''}
    
    if account.platform == 'wechat_work':
        corp_id = account.config.get('corp_id', '')
        corp_secret = account.config.get('corp_secret', '')
        if not corp_id or not corp_secret:
            result['message'] = '请填写企业微信 CorpID 和 Secret'
        else:
            try:
                url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}'
                response = requests.get(url, timeout=10)
                data = response.json()
                if data.get('errcode') == 0:
                    result['success'] = True
                    result['message'] = f'连接成功！AccessToken 获取成功'
                    account.status = 'online'
                else:
                    result['message'] = f'连接失败: {data.get("errmsg", "未知错误")}'
                    account.status = 'error'
            except Exception as e:
                result['message'] = f'连接异常: {str(e)}'
                account.status = 'error'
            account.save()
    
    elif account.platform == 'personal':
        result['success'] = True
        result['message'] = '个人微信连接测试成功（需手动扫码登录）'
        account.status = 'online'
        account.save()
    
    elif account.platform == 'official_account':
        app_id = account.config.get('app_id', '')
        app_secret = account.config.get('app_secret', '')
        if not app_id or not app_secret:
            result['message'] = '请填写公众号 AppID 和 AppSecret'
        else:
            try:
                url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}'
                response = requests.get(url, timeout=10)
                data = response.json()
                if 'access_token' in data:
                    result['success'] = True
                    result['message'] = '连接成功！AccessToken 获取成功'
                    account.status = 'online'
                else:
                    result['message'] = f'连接失败: {data.get("errmsg", "未知错误")}'
                    account.status = 'error'
            except Exception as e:
                result['message'] = f'连接异常: {str(e)}'
                account.status = 'error'
            account.save()
    
    return JsonResponse(result)


@login_required
def sync_contacts(request, account_id):
    account = get_object_or_404(WeChatAccount, id=account_id)
    log = SyncLog.objects.create(
        account=account,
        sync_type='contacts',
        status='running',
        started_at=datetime.now(),
    )
    
    try:
        if account.platform == 'wechat_work':
            corp_id = account.config.get('corp_id', '')
            corp_secret = account.config.get('corp_secret', '')
            if not corp_id or not corp_secret:
                log.status = 'failed'
                log.message = '缺少企业微信配置'
                log.finished_at = datetime.now()
                log.save()
                return JsonResponse({'success': False, 'message': '缺少企业微信配置'})
            
            token_url = f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={corp_id}&corpsecret={corp_secret}'
            token_response = requests.get(token_url, timeout=10)
            token_data = token_response.json()
            if token_data.get('errcode') != 0:
                log.status = 'failed'
                log.message = f'获取 Token 失败: {token_data.get("errmsg")}'
                log.finished_at = datetime.now()
                log.save()
                return JsonResponse({'success': False, 'message': '获取 Token 失败'})
            
            access_token = token_data['access_token']
            user_list_url = f'https://qyapi.weixin.qq.com/cgi-bin/user/list?access_token={access_token}&department_id=1&fetch_child=1'
            user_response = requests.get(user_list_url, timeout=10)
            user_data = user_response.json()
            
            if user_data.get('errcode') == 0:
                count = 0
                for user in user_data.get('userlist', []):
                    contact, created = Contact.objects.get_or_create(
                        wx_id=user.get('userid', user.get('openid', '')),
                        defaults={
                            'name': user.get('name', ''),
                            'remark': user.get('alias', ''),
                            'contact_type': 'personal',
                        }
                    )
                    if created:
                        count += 1
                log.status = 'success'
                log.message = f'成功同步 {count} 个联系人'
                messages.success(request, f'成功同步 {count} 个联系人')
            else:
                log.status = 'failed'
                log.message = f'同步失败: {user_data.get("errmsg")}'
        
        else:
            log.status = 'success'
            log.message = '非企业微信账户，跳过联系人同步'
        
        log.finished_at = datetime.now()
        log.save()
        
    except Exception as e:
        log.status = 'failed'
        log.message = str(e)
        log.finished_at = datetime.now()
        log.save()
        return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': True, 'message': log.message})


@login_required
def sync_logs(request, account_id):
    account = get_object_or_404(WeChatAccount, id=account_id)
    logs = account.sync_logs.all()[:20]
    return render(request, 'wechat_sync_logs.html', {'account': account, 'logs': logs})


@login_required
def personal_login(request, account_id):
    from .client import wechat_client
    account = get_object_or_404(WeChatAccount, id=account_id)
    if account.platform != 'personal':
        return JsonResponse({'success': False, 'message': '仅支持个人微信登录'})
    
    qr_base64 = wechat_client.login(account_id)
    if qr_base64:
        return JsonResponse({'success': True, 'qr_code': qr_base64})
    else:
        return JsonResponse({'success': False, 'message': '获取二维码失败，请稍后重试'})


@login_required
def personal_login_status(request, account_id):
    from .client import wechat_client
    status = wechat_client.get_status()
    account = get_object_or_404(WeChatAccount, id=account_id)
    return JsonResponse({
        'is_logged_in': status['is_logged_in'],
        'account_id': status['account_id'],
        'status': account.status,
    })


@login_required
def personal_logout(request, account_id):
    from .client import wechat_client
    wechat_client.logout()
    account = get_object_or_404(WeChatAccount, id=account_id)
    account.status = 'offline'
    account.save()
    return JsonResponse({'success': True, 'message': '已登出'})


@login_required
def send_message(request):
    from .client import wechat_client
    if request.method == 'POST':
        wx_id = request.POST.get('wx_id')
        content = request.POST.get('content')
        success, message = wechat_client.send_message(wx_id, content)
        return JsonResponse({'success': success, 'message': message})
    return JsonResponse({'success': False, 'message': 'Method not allowed'})