from django.db import migrations, models


def ensure_breed_column_exists(apps, schema_editor):
    connection = schema_editor.connection
    Pet = apps.get_model('pets', 'Pet')
    table_name = Pet._meta.db_table

    existing_tables = set(connection.introspection.table_names())
    if table_name not in existing_tables:
        return

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(cursor, table_name)
        }

    if 'breed' in columns:
        return

    breed_field = models.CharField(max_length=100, default='')
    breed_field.set_attributes_from_name('breed')
    schema_editor.add_field(Pet, breed_field)


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0003_pet_image'),
    ]

    operations = [
        migrations.RunPython(ensure_breed_column_exists, migrations.RunPython.noop),
    ]