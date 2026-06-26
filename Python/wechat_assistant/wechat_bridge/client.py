import itchat
import threading
import time
import os
import base64
from django.conf import settings
from .models import WeChatAccount
from core.models import Contact, Message, Conversation

class WeChatClient:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        self.is_logged_in = False
        self.login_qr_data = None
        self.account_id = None
        self.login_thread = None
        self.qr_event = threading.Event()
        self.self_username = ''

    def get_qr_base64(self):
        if self.login_qr_data:
            return base64.b64encode(self.login_qr_data).decode('utf-8')
        qr_path = os.path.join(settings.BASE_DIR, 'static', 'qr_code.png')
        if os.path.exists(qr_path):
            with open(qr_path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        return None

    def login(self, account_id):
        self.account_id = account_id
        self.login_qr_data = None
        self.qr_event.clear()
        self.login_thread = threading.Thread(target=self._login_thread, daemon=True)
        self.login_thread.start()
        self.qr_event.wait(timeout=30)
        return self.get_qr_base64()

    def _login_thread(self):
        @itchat.msg_register(itchat.content.TEXT)
        def text_msg_handler(msg):
            self._handle_message(msg)

        @itchat.msg_register(itchat.content.IMAGE)
        def image_msg_handler(msg):
            self._handle_message(msg)

        @itchat.msg_register(itchat.content.FILE)
        def file_msg_handler(msg):
            self._handle_message(msg)

        @itchat.msg_register(itchat.content.LINK)
        def link_msg_handler(msg):
            self._handle_message(msg)

        @itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
        def group_text_handler(msg):
            self._handle_message(msg, is_group=True)

        try:
            itchat.auto_login(
                hotReload=True,
                enableCmdQR=False,
                qrCallback=self._qr_callback,
                loginCallback=self._login_callback,
                exitCallback=self._exit_callback,
            )
            itchat.run()
        except Exception as e:
            print(f"Login error: {e}")

    def _qr_callback(self, uuid, status, qrcode):
        self.login_qr_data = qrcode
        self.qr_event.set()
        qr_path = os.path.join(settings.BASE_DIR, 'static', 'qr_code.png')
        os.makedirs(os.path.dirname(qr_path), exist_ok=True)
        try:
            with open(qr_path, 'wb') as f:
                f.write(qrcode)
        except Exception as e:
            print(f"Save QR code error: {e}")

    def _login_callback(self):
        self.is_logged_in = True
        try:
            account = WeChatAccount.objects.get(id=self.account_id)
            account.status = 'online'
            account.save()
            self.self_username = itchat.originInstance.loginInfo['User']['UserName']
            self._sync_contacts()
        except Exception as e:
            print(f"Update account status error: {e}")

    def _exit_callback(self):
        self.is_logged_in = False
        try:
            account = WeChatAccount.objects.get(id=self.account_id)
            account.status = 'offline'
            account.save()
        except Exception as e:
            print(f"Update account status error: {e}")

    def _sync_contacts(self):
        friends = itchat.get_friends(update=True)
        for friend in friends:
            Contact.objects.get_or_create(
                wx_id=friend['UserName'],
                defaults={
                    'name': friend['NickName'],
                    'remark': friend['RemarkName'],
                    'contact_type': 'personal',
                }
            )
        rooms = itchat.get_chatrooms(update=True)
        for room in rooms:
            Contact.objects.get_or_create(
                wx_id=room['UserName'],
                defaults={
                    'name': room['NickName'],
                    'contact_type': 'group',
                }
            )

    def _handle_message(self, msg, is_group=False):
        try:
            contact_type = 'group' if is_group else 'personal'

            contact, _ = Contact.objects.get_or_create(
                wx_id=msg['FromUserName'],
                defaults={
                    'name': msg.get('NickName', ''),
                    'contact_type': contact_type,
                }
            )

            msg_type_map = {
                itchat.content.TEXT: 'text',
                itchat.content.IMAGE: 'image',
                itchat.content.FILE: 'file',
                itchat.content.LINK: 'link',
            }

            msg_type = msg_type_map.get(msg['Type'], 'text')

            content = ''
            if msg['Type'] == itchat.content.TEXT:
                content = msg['Text']
            elif msg['Type'] == itchat.content.LINK:
                content = f"{msg.get('Text', '')} - {msg.get('Url', '')}"

            message = Message.objects.create(
                msg_id=msg['MsgId'],
                contact=contact,
                msg_type=msg_type,
                content=content,
                timestamp=msg['CreateTime'],
                is_from_self=msg['FromUserName'] == getattr(self, 'self_username', ''),
            )

            conversation, _ = Conversation.objects.get_or_create(
                contact=contact,
                defaults={'last_message': message}
            )
            conversation.last_message = message
            if not message.is_from_self:
                conversation.unread_count = conversation.unread_count + 1
            conversation.save()

        except Exception as e:
            print(f"Save message error: {e}")

    def send_message(self, wx_id, content):
        if not self.is_logged_in:
            return False, "Not logged in"
        try:
            itchat.send(content, toUserName=wx_id)
            return True, "Success"
        except Exception as e:
            return False, str(e)

    def logout(self):
        if self.is_logged_in:
            itchat.logout()
            self.is_logged_in = False

    def get_status(self):
        return {
            'is_logged_in': self.is_logged_in,
            'account_id': self.account_id,
        }


wechat_client = WeChatClient()