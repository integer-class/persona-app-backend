from django.core.management.base import BaseCommand
from api.models import Face_shape, Hair_styles, Accessories, Recommendations, Recommendations_hair_styles, Recommendations_accessories, Feedback, History

class Command(BaseCommand):
    help = 'Seeds the database with initial data'
    
    def handle(self, *args, **options):
        Face_shape.objects.create(name='Oval')
        Face_shape.objects.create(name='Round')
        Face_shape.objects.create(name='Square')
        Face_shape.objects.create(name='Heart')
        Face_shape.objects.create(name='Oblong')
        
        
        Hair_styles.objects.create(name='Comma Hair', image='images/hair_styles/comma_hair.jpg')
        
        Accessories.objects.create(name='Glasses', image='images/accessories/glasses.jpg')
        
        Recommendations.objects.create(Face_shape_id=1)
        
        Recommendations_hair_styles.objects.create(Recommendations_id=1, Hair_styles_id=1)
        
        Recommendations_accessories.objects.create(Recommendations_id=1, Accessories_id=1)
        
        Feedback.objects.create(Recommendations_id=1, user_id=1, comment='This is a comment', rating=5)
        
        History.objects.create(Recommendations_id=1, user_id=1)