from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock

class TitleAndTextBlock(blocks.StructBlock):
       
    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')
    richText = blocks.RichTextBlock(required=False, help_text='Add additional rich text')
    
    class Meta:
        template = "streams/title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"
    
    
    
class RichtextBlock(blocks.RichTextBlock):
        
        class Meta:
            template = "streams/richtext_block.html"
            icon = "doc-full"
            label = "Rich Text Paragraph"
            
                
        
class CardsBlock(blocks.StructBlock):
    
    title = blocks.CharBlock(required=True, help_text='Add your title')
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("title", blocks.CharBlock(required=True, max_length=40)),
                ("body", blocks.TextBlock(required=True, help_text="Enter the body text")),
                ("image", ImageChooserBlock(required=False)),
                ("button_page", blocks.PageChooserBlock(required=False, help_text="Choose a page")),
                ("button_url", blocks.URLBlock(required=False, help_text="\"Button Page\" field and \"Button Url\" field are mutally exclusive")),
            ]
        )
    )
    
    class Meta:
        template = "streams/cards_block.html"
        icon = "grip"
        label = "Cards List"