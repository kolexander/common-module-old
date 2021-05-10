from django.core.management.base import BaseCommand
from django.db import connections, utils
from psycopg2.extras import NamedTupleCursor
from django.conf import settings
from common.models import Account, User


class Command(BaseCommand):
    help = 'Sync Account Models'
    def handle(self, *args, **options):
        conn = connections['hhukr']
        conn.ensure_connection()

        self.load_account(conn)
        self.load_user(conn)

    def load_account(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' select *
                            from account ''')
            rows = cursor.fetchall()

            for account in rows:
                try:
                    Account.objects.create(pk=account.hhid,
                                           disabled=account.disabled,
                                           created_at=account.creation_time,
                                           updated_at=account.last_modification_time,
                                           primary_email=account.primary_email,
                                           first_name=account.first_name,
                                           middle_name=account.mid_name,
                                           last_name=account.last_name)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_user(self, conn):
        user_type =getattr(settings, 'USER_TYPE', 0)
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(f'select * from hhuser where type = {user_type}')
            rows = cursor.fetchall()

            for user in rows:
                try:
                    User.objects.create(pk=user.user_id,
                                        created_at=user.creation_time,
                                        area_id=user.area_id,
                                        description=user.description,
                                        account_id=user.hhid,
                                        language=user.lang)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()
