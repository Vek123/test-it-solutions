__all__ = ()

from django.core.exceptions import ValidationError
from django.test import TestCase

from catalog import models


class RecordTests(TestCase):
    fixtures = ('records.json',)

    def test_valid_create_status(self):
        existed_statuses_count = models.RecordStatus.objects.count()
        new_status = models.RecordStatus(name='New status')
        new_status.full_clean()
        new_status.save()
        self.assertEqual(
            existed_statuses_count + 1,
            models.RecordStatus.objects.count(),
        )

    def test_valid_create_type(self):
        existed_types_count = models.RecordType.objects.count()
        new_type = models.RecordType(name='New type')
        new_type.full_clean()
        new_type.save()
        self.assertEqual(
            existed_types_count + 1,
            models.RecordType.objects.count(),
        )

    def test_valid_create_category(self):
        existed_categories_count = models.RecordCategory.objects.count()
        record_type = models.RecordType.objects.all()[0]
        new_category = models.RecordCategory(name='New category')
        new_category.full_clean()
        new_category.save()
        new_category.record_types.add(record_type)
        self.assertEqual(
            existed_categories_count + 1,
            models.RecordCategory.objects.count(),
        )

    def test_valid_create_sub_category(self):
        existed_sub_categories_count = models.RecordSubCategory.objects.count()
        category = models.RecordCategory.objects.all()[0]
        new_sub_category = models.RecordSubCategory(name='New sub category')
        new_sub_category.full_clean()
        new_sub_category.save()
        new_sub_category.categories.add(category)
        self.assertEqual(
            existed_sub_categories_count + 1,
            models.RecordSubCategory.objects.count(),
        )

    def test_valid_min_create_record(self):
        existed_records_count = models.Record.objects.count()
        sub_category = models.RecordSubCategory.objects.all()[0]
        category = sub_category.categories.all()[0]
        record_type = category.record_types.all()[0]
        new_record = models.Record(
            total=0,
            record_type=record_type,
            category=category,
            sub_category=sub_category,
        )
        new_record.full_clean()
        new_record.save()
        self.assertEqual(
            existed_records_count + 1,
            models.Record.objects.count(),
        )

    def test_valid_max_create_record(self):
        existed_records_count = models.Record.objects.count()
        sub_category = models.RecordSubCategory.objects.all()[0]
        category = sub_category.categories.all()[0]
        record_type = category.record_types.all()[0]
        status = models.RecordStatus.objects.all()[0]
        new_record = models.Record(
            comment='comment',
            created_at='2025-05-10',
            total=1000,
            record_type=record_type,
            category=category,
            sub_category=sub_category,
            status=status,
        )
        new_record.full_clean()
        new_record.save()
        self.assertEqual(
            existed_records_count + 1,
            models.Record.objects.count(),
        )

    def test_invalid_created_at_future_create_record(self):
        existed_records_count = models.Record.objects.count()
        sub_category = models.RecordSubCategory.objects.all()[0]
        category = sub_category.categories.all()[0]
        record_type = category.record_types.all()[0]
        new_record = models.Record(
            created_at='20000-05-10',
            total=1000,
            record_type=record_type,
            category=category,
            sub_category=sub_category,
        )
        with self.assertRaises(ValidationError):
            new_record.full_clean()
            new_record.save()

        self.assertEqual(
            existed_records_count,
            models.Record.objects.count(),
        )

    def test_invalid_negative_total_create_record(self):
        existed_records_count = models.Record.objects.count()
        sub_category = models.RecordSubCategory.objects.all()[0]
        category = sub_category.categories.all()[0]
        record_type = category.record_types.all()[0]
        new_record = models.Record(
            created_at='2025-05-10',
            total=-1000,
            record_type=record_type,
            category=category,
            sub_category=sub_category,
        )
        with self.assertRaises(ValidationError):
            new_record.full_clean()
            new_record.save()

        self.assertEqual(
            existed_records_count,
            models.Record.objects.count(),
        )

    def test_invalid_sub_category_not_from_category_create_record(self):
        existed_records_count = models.Record.objects.count()
        sub_category = models.RecordSubCategory.objects.all()[0]
        category = models.RecordCategory.objects.exclude(
            sub_categories__in=[sub_category],
        )[0]
        record_type = category.record_types.all()[0]
        new_record = models.Record(
            created_at='2025-05-10',
            total=1000,
            record_type=record_type,
            category=category,
            sub_category=sub_category,
        )
        with self.assertRaises(ValidationError):
            new_record.full_clean()
            new_record.save()

        self.assertEqual(
            existed_records_count,
            models.Record.objects.count(),
        )

    def test_invalid_category_not_from_record_type_create_record(self):
        existed_records_count = models.Record.objects.count()
        record_types = models.RecordType.objects.all()
        record_type = record_types[1]
        category = record_type.categories.all()[1]
        sub_category = category.sub_categories.all()[0]
        record_type = record_types[0]
        new_record = models.Record(
            created_at='2025-05-10',
            total=1000,
            record_type=record_type,
            category=category,
            sub_category=sub_category,
        )
        with self.assertRaises(ValidationError):
            new_record.full_clean()
            new_record.save()

        self.assertEqual(
            existed_records_count,
            models.Record.objects.count(),
        )
