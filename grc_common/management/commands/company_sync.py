from django.core.management.base import BaseCommand
from django.db import connections, utils
from psycopg2.extras import NamedTupleCursor

from common.models import Company, CompanyIndustry, CompanyManager


class Command(BaseCommand):
    help = 'Sync Company Models'
    def handle(self, *args, **options):
        conn = connections['hhukr']
        conn.ensure_connection()

        # self.load_company(conn)
        # self.load_company_industry(conn)
        self.load_company_manager(conn)

    def load_company(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' select *
                            from employer ''')
            rows = cursor.fetchall()

            for employer in rows:
                try:
                    Company.objects.create(pk=employer.employer_id,
                                           manager_id=employer.manager_id,
                                           creation_time=employer.creation_time,
                                           area_id=employer.area_id,
                                           name=employer.name,
                                           category=employer.category,
                                           url=employer.url,
                                           small_logo_url=employer.small_logo_url,
                                           state=employer.state)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_company_industry(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' select *
                               from employer_industry ''')
            rows = cursor.fetchall()

            for employer in rows:
                try:
                    CompanyIndustry.objects.create(company_id=employer.employer_id,
                                                   industry_id=employer.industry_id)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_company_manager(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' select *
                               from employer_manager ''')
            rows = cursor.fetchall()

            for employer in rows:
                try:
                    CompanyManager.objects.create(pk=employer.employer_manager_id,
                                                  user_id=employer.user_id,
                                                  company_id=employer.employer_id,
                                                  type=employer.type,
                                                  phone=employer.phone,
                                                  additional_phone=employer.additional_phone)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()
