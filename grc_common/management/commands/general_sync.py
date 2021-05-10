from django.core.management.base import BaseCommand
from django.db import connections, utils
from psycopg2.extras import NamedTupleCursor

from common.models import Language, Industry, ProfessionalArea, Specialization, KeySkill, Currency, Area

class Command(BaseCommand):
    help = 'Sync General Models'

    # TODO params
    def handle(self, *args, **options):
        conn = connections['hhukr']
        conn.ensure_connection()

        self.load_language(conn)
        self.load_industry(conn)
        self.load_professional_area(conn)
        self.load_specialization(conn)
        self.load_key_skill(conn)
        self.load_currency(conn)
        self.load_area(conn)

    def load_language(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('''SELECT language_id,
               t_en.value as en,
               t_ru.value as ru,
               t_ua.value as ua,
               iso_code
        FROM language
                 left join translation t_ru on 'language.'||split_part(language.name, '.', 2) = t_ru.name and t_ru.lang = 'RU'
                 left join translation t_en on 'language.'||split_part(language.name, '.', 2) = t_en.name and t_en.lang = 'EN'
                 left join translation t_ua on 'language.'||split_part(language.name, '.', 2) = t_ua.name and t_ua.lang = 'UA' ''')
            rows = cursor.fetchall()

            for language in rows:
                try:
                    Language.objects.create(id=language.language_id, name_en=language.en, name_ru=language.ru,
                                            name_uk=language.ua, code=language.iso_code)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_industry(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('''SELECT industry_id,
       t_en.value as en,
       t_ru.value as ru,
       t_ua.value as ua,
       hidden,
       parent_id
FROM industry
         left join translation t_en on industry.name = t_en.name and t_en.lang = 'EN'
         left join translation t_ru on industry.name = t_ru.name and t_ru.lang = 'RU'
         left join translation t_ua on industry.name = t_ua.name and t_ua.lang = 'UA'
order by industry_id ''')
            rows = cursor.fetchall()

            for industry in rows:
                try:
                    Industry.objects.create(id=industry.industry_id, name_en=industry.en, name_ru=industry.ru,
                                            name_uk=industry.ua, parent_id=industry.parent_id,
                                            is_hidden=industry.hidden)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_professional_area(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('''SELECT professional_area_id,
   t_en.value as en,
   t_ru.value as ru,
   t_ua.value as ua,
   visible
from professional_area
     left join translation t_en on professional_area.name = t_en.name and t_en.lang = 'EN'
     left join translation t_ru on professional_area.name = t_ru.name and t_ru.lang = 'RU'
     left join translation t_ua on professional_area.name = t_ua.name and t_ua.lang = 'UA' ''')
            rows = cursor.fetchall()

            for profarea in rows:
                try:
                    ProfessionalArea.objects.create(id=profarea.professional_area_id, name_en=profarea.en,
                                                    name_ru=profarea.ru,
                                                    name_uk=profarea.ua,
                                                    is_visible=profarea.visible)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_specialization(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute('''SELECT specialization_id,
       professional_area_id,
       t_en.value as en,
       t_ru.value as ru,
       t_ua.value as ua,
       visible
FROM specialization
    left join translation t_en on specialization.name = t_en.name and t_en.lang = 'EN'
    left join translation t_ru on specialization.name = t_ru.name and t_ru.lang = 'RU'
    left join translation t_ua on specialization.name = t_ua.name and t_ua.lang = 'UA' ''')
            rows = cursor.fetchall()

            for spec in rows:
                try:
                    Specialization.objects.create(id=spec.specialization_id,
                                                  professional_area_id=spec.professional_area_id, name_en=spec.en,
                                                  name_ru=spec.ru,
                                                  name_uk=spec.ua,
                                                  is_visible=spec.visible)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_key_skill(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' SELECT * FROM key_skill order by key_skill_id ''')
            rows = cursor.fetchall()

            for skill in rows:
                try:
                    KeySkill.objects.create(id=skill.key_skill_id,
                                            general=skill.general, name=skill.name,
                                            parent_id=skill.parent_id, searchable=skill.searchable)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_currency(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' SELECT * FROM currency''')
            rows = cursor.fetchall()

            for currency in rows:
                try:
                    Currency.objects.create(code=currency.code, updated_at=currency.last_rate_change_time,
                                            rate=currency.rate)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()

    def load_area(self, conn):
        with conn.connection.cursor(cursor_factory=NamedTupleCursor) as cursor:
            cursor.execute(''' SELECT  area_id,
                                       t_en.value as en,
                                       t_ru.value as ru,
                                       t_ua.value as ua,
                                       type,
                                       parent_id
                                FROM area
                                         left join translation t_en on area.name = t_en.name and t_en.lang = 'EN'
                                         left join translation t_ru on area.name = t_ru.name and t_ru.lang = 'RU'
                                         left join translation t_ua on area.name = t_ua.name and t_ua.lang = 'UA'
                                ORDER BY parent_id ''')
            rows = cursor.fetchall()

            for area in rows:
                try:
                    Area.objects.create(parent_id=area.parent_id if area.parent_id != 0 else None,
                                        name_ru=area.ru,
                                        name_uk=area.ua,
                                        name_en=area.en,
                                        pk=area.area_id,
                                        type=area.type)
                except utils.IntegrityError as e:
                    print(e)
            cursor.close()
