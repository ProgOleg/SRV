import json
from collections import Counter

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from srvbd import models


class Command(BaseCommand):
    help = 'Insert data into the database in a transaction'

    def _get_manufacturer(self, data: list):
        manufacturer = "China"
        if data and all((isinstance(el, dict) for el in data)):
            a = [key for dictionary in data for key in dictionary]
            counter = Counter(a)
            manufacturer = counter.most_common()[0][0]
        return manufacturer

    def populate(self, path, type_appliances):
        with open(path) as f:
            inp = json.loads(f.read())
            try:
                with transaction.atomic():
                    record_appliances, created = models.TypeAppliances.objects.get_or_create(
                        type_appliances=type_appliances
                    )
                    record_appliances.save()
                    for key, data in inp.items():
                        title = data["title"]
                        record_spar_part, created = models.TypeSparPart.objects.get_or_create(type_spar_part=title)
                        record_spar_part.save()
                        for detail in data["details"]:
                            manufacturer = self._get_manufacturer(detail["original_codes"])
                            record_manufacturer, created = models.Manufacturer.objects.get_or_create(
                                manufacturer=manufacturer
                            )
                            if created:
                                record_manufacturer.save()
                            part_nums = list({value for item in detail["original_codes"] for value in item.values()}) or []
                            record_spart = models.SparPart.objects.create(
                                name=detail["name"],
                                part_num=part_nums,
                                specification=detail["description"],
                                attachment_part=record_spar_part,
                                attachment_appliances=record_appliances,
                                attachment_manufacturer=record_manufacturer,
                                image_link=detail.get("photo_link", {}).get("src")
                            )
                            record_spart.save()
            except Exception as ex:
                transaction.rollback()
                raise ex

    def handle(self, *args, **options):
        files = [
            ("/Users/guest1/PycharmProjects/pet/srv/srv/WashingMachines.json", "Стиральные машины"),
            ("/Users/guest1/PycharmProjects/pet/srv/srv/Refrigerator.json", "Холодильники")
        ]
        for file in files:
            self.populate(*file)
