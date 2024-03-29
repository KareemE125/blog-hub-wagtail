# Generated by Django 5.0 on 2024-01-03 21:13

import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flex', '0004_alter_flexpage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flexpage',
            name='content',
            field=wagtail.fields.StreamField([('title_and_text', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Add your title', required=True)), ('text', wagtail.blocks.TextBlock(help_text='Add additional text', required=True)), ('richText', wagtail.blocks.RichTextBlock(help_text='Add additional rich text', required=False))])), ('cards_list', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(help_text='Add your title', required=True)), ('cards', wagtail.blocks.ListBlock(wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=40, required=True)), ('body', wagtail.blocks.TextBlock(help_text='Enter the body text', required=True)), ('image', wagtail.images.blocks.ImageChooserBlock(required=False)), ('button_page', wagtail.blocks.PageChooserBlock(help_text='Choose a page', required=False)), ('button_url', wagtail.blocks.URLBlock(help_text='"Button Page" field and "Button Url" field are mutally exclusive', required=False))])))]))], blank=True, null=True, use_json_field=True),
        ),
    ]
