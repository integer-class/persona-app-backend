from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from api.models import FaceShape, HairStyle, Accessory, Recommendation, Feedback, History

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        # Create Face Shapes
        oval = FaceShape.objects.create(name='Oval')
        round_face = FaceShape.objects.create(name='Round')
        square = FaceShape.objects.create(name='Square')
        heart = FaceShape.objects.create(name='Heart')
        oblong = FaceShape.objects.create(name='Oblong')

        # Create Hair Styles
        
        # MALE
        # oval face
        # this also fit with heart face
        pompadour = HairStyle.objects.create(name='Pompadour', image='images/hair_styles/pompadour.jpg', description='This uber-popular cut is perfect for oval faces because it brings style and drama without dropping any locks in your face. Heart faces can also pull off this look.', gender='male')
        undercut = HairStyle.objects.create(name='Undercut', image='images/hair_styles/undercut.jpg', description='An under-cut hairstyle is a throwback to the early 1900s and really never goes out of style. it features a long, side-parted top with buzzed sides.', gender='male')
        comb_over = HairStyle.objects.create(name='Comb-over fade', image='images/hair_styles/comb_over_fade.jpg', description='A mid or taper fade with a comb-over is the perfect pick for the oval face because it creates some bold shape and definition while keeping the hair out your eyes.', gender='male')
        # this also fit with square face
        man_bun = HairStyle.objects.create(name='Man bun', image='images/hair_styles/man_bun.jpg', description='Oval faces are uniquely well-suited to the man bun because they are one of the few shapes that can handle that much top volume. Square faces can also pull off this look.', gender='male')
        
        # round face
        french_crop = HairStyle.objects.create(name='French crop', image='images/hair_styles/french_crop.jpg', description='The french crop is a shorter hairstyle marked by a taper fade or undercut with longer fringe on top. This look gives you the top volume while avoiding any side bulk that could add a rounder appearance.', gender='male')
        high_skin_fade = HairStyle.objects.create(name='High skin fade', image='images/hair_styles/high_skin_fade.jpg', description='The high skin fade is the more modern, neat version of the French crop. It features super-short sides with longer strands on the side, creating a dramatic contrast between the two.', gender='male')
        # this also fit with rectangle face
        side_part = HairStyle.objects.create(name='Side part', image='images/hair_styles/side_part.jpg', description='The side part is a simple, close-clipped cut marked by a dramatic quiff contrasted by a shorter cut on the other side of the part. The contrast between short and long creates the illusion of more volume.', gender='male')
        flat_top = HairStyle.objects.create(name='Flat top', image='images/hair_styles/flat_top.jpg', description='Another classic look marked by short sides and length on top, the flat top is a military-inspired do that brings a bit of a retro vibe. Ask your barber to go for a rounded, rather than square, shape for a modern look.', gender='male')
        
        # square
        side_swept_brush_up = HairStyle.objects.create(name='Side-swept brush-up', image='images/hair_styles/side_swept_brush_up.jpg', description='If you are going for a bit of length, try a side-swept brush-up, which is short on the sides with an even top for volume. Similarly, a high fade with a swept-back top will give the same appearance with more movement.', gender='male')
        buzzcut = HairStyle.objects.create(name='Buzzcut', image='images/hair_styles/buzzcut.jpg', description='Volume, texture and length arent the only ways to go with square faces. For a bold, dramatic look, consider the classic buzzcut. By highlighting your face angles, this style piles on the strong and authoritative vibes.', gender='male')
        
        # rectangle
        crew_cut = HairStyle.objects.create(name='Crew cut', image='images/hair_styles/crew_cut.jpg', description='We are not talking about the classic, close-clipped crew here. We are talking about a side-swept crew cut that adds some texture and personality on top without the inches that could elongate your face.', gender='male')
        
        # heart
        shoulder_length_hair = HairStyle.objects.create(name='Shoulder-length hair', image='images/hair_styles/shoulder_length_hair.jpg', description='Especially ideal for guys who have a pointy chin but dont want to grow any facial hair, a shoulder-length grow-out can help even out the width of your face for a more even appearance.', gender='male')
        textured_quiff = HairStyle.objects.create(name='Textured Quiff', image='images/hair_styles/textured_quiff.jpg', description='This cut is like a pompadour mixed with a faux hawk and a flattop. The reason why we love it for the inverted triangle face is because it elongates the face ever-so-slightly, dialing down the pointed chin.', gender='male')
        
        # FEMALE
        
        # oval
        long_layers = HairStyle.objects.create(name='Long layers',image='images/hair_styles/long_layers.jpg', description='Long layers are perfect for oval faces. They add volume and movement to the hair, creating a soft and feminine look.', gender='female')
        bob_cut = HairStyle.objects.create(name='Bob cut', image='images/hair_styles/bob_cut.jpg', description='A classic bob works well with oval shaped faces, drawing attention to the jawline and cheekbones.', gender='female')
        side_swept_bangs = HairStyle.objects.create(name='Side-swept bangs', image='images/hair_styles/side_swept_bangs.jpg', description='These can add a touch of sophistication while framing the face beautifully, without obscuring the proportions of the oval shape.', gender='female')
        # round
        long_layers_volume_top = HairStyle.objects.create(name='Long layers with volume on top', image='images/hair_styles/long_layers_volume_top.jpg', description='Adding height at the corwn elongates the face, creating the illusion of an oval shape.', gender='female')
        asymmetrical_bob = HairStyle.objects.create(name='Asymmetrical Bob', image='images/hair_styles/asymmetrical_bob.jpg', description='This style, which is longer in the front and shorter in the back, helps to elongate the face while addings angles that counteract the roundness.', gender='female')
        pixie_cut_volume = HairStyle.objects.create(name='Pixie Cut with Volume', image='images/hair_styles/pixie_cut_volume.jpg', description='A pixie cut with volume at the top can create the appearance of a longer face, balancing out the roundness.', gender='female')
        # square & rectangular
        soft_wispy_bangs = HairStyle.objects.create(name='Soft, wispy bangs', image='images/hair_styles/wispy_bangs.jpg', description='These can soften the angles of the face, especially the strong jawline creating a more rounded appearance.', gender='female')
        long_soft_layers = HairStyle.objects.create(name='Long, Soft layers', image='images/hair_styles/soft_layers.jpg', description='Long layers that start below the jaw can add softness and movement, reducing the emphasis on the squareness of the face.', gender='female')
        side_part_styles = HairStyle.objects.create(name='Side-parted styles', image='images/hair_styles/side_part_styles.jpg', description='A deep side part can break up the symmetry of a square face, adding softness and shifting focus away from the jawline.', gender='female')
        # heart 
        long_side_swept_bangs = HairStyle.objects.create(name='Long, side-swept bangs', image='images/hair_styles/side_swept_bangs.jpg', description='Long, side-swept bangs can help to balance out the width of the forehead, creating a more oval appearance.', gender='female')
        chin_length_bob = HairStyle.objects.create(name='Chin-length bob', image='images/hair_styles/chin_bob.jpg', description='A bob that hits right at the chin helps to add width to the lower part of the face, balancing the narrow chin with the broader forehead.', gender='female')
        wavy_lob = HairStyle.objects.create(name='wavy lob (long bob)', image='images/hair_styles/wavy_lob.jpg', description='A wavy lob can add volume and width around the jawline, balancing out the face shape.', gender='female')
        
        ## Glasses is Unisex
        # round face & oval
        transparent_frames = Accessory.objects.create(name='Transparent frames', image='images/accessories/transparent_frames.jpg', description='These frames add definition to the face without overpowering the soft curves of a round face.', category='glasses')
        full_rimmed_frames = Accessory.objects.create(name='Full-rimmed frames', image='images/accessories/full_rimmed_frames.jpg', description='The bold design of these glasses adds structure to a round face, creating a striking look.', category='glasses')
        wooden_frames = Accessory.objects.create(name='Wooden frames', image='images/accessories/wooden_frames.jpg', description='The natural texture of these frames adds a touch of warmth to a round face, creating a harmonious look.', category='glasses')
        # this also fit with heart face
        square_glasses = Accessory.objects.create(name='Square glasses', image='images/accessories/square_glasses.jpg', description='The angular design of square glasses can add definition to the soft curves of a round face, creating a balanced look.', category='glasses')
        
        # square face & rectangular
        round_glasses = Accessory.objects.create(name='Round glasses', image='images/accessories/round_glasses.jpg', description='These glasses soften the angular features of a square face, adding a touch of elegance.', category='glasses')
        browline_glasses = Accessory.objects.create(name='Browline glasses', image='images/accessories/browline_glasses.jpg', description='The bold upper frame of these glasses draws attention to the eyes, balancing the jawline.', category='glasses')
        colored_oval_glasses = Accessory.objects.create(name='Colored oval glasses', image='images/accessories/colored_oval_glasses.jpg', description='The soft curves of these glasses contrast the straight lines of a square face, adding a touch of sophistication.', category='glasses')
        
        # heart face
        oval_glasses = Accessory.objects.create(name='Oval glasses', image='images/accessories/oval_glasses.jpg', description='Oval glasses fit heart shape faces perfectly. They help soften and balance out the angles of faces so they better resemble a base-up triangle face.', category='glasses')
        semi_rimless = Accessory.objects.create(name='Semi-rimless and Rimless', image='images/accessories/semi_rimless_rimless.jpg', description='These glasses are perfect for heart-shaped faces because they help to balance out the width of the forehead and the narrowness of the chin.', category='glasses')
        rectangular_glasses = Accessory.objects.create(name='Rectangular glasses', image='images/accessories/rectangular_glasses.jpg', description='Rectangular glasses balance out the curves of you rheart shape face withput drawing too much attention to its width.', category='glasses')
        
        ## EARRINGS JUST FOR FEMALE
        
        # oval
        hoops_earrings = Accessory.objects.create(name='Hoop earrings', image='images/accessories/hoops_earrings.jpg', description='Whether petite or statement-sized, hoops beautifully echo the symmetry of an oval face.', category='earrings')
        # this also fit with round face
        teardrop_earrings = Accessory.objects.create(name='Teardrop earrings', image='images/accessories/teardrop_earrings.jpg', description='While they shine on round faces, they also spotlight the beauty of oval faces, drawing attention to the cheekbones.', category='earrings')
        # this also fit with round face
        geometric_earrings = Accessory.objects.create(name='Geometrics earrings', image='images/accessories/geometrics_earrings.jpg', description='Be it squares, triangles, or other shapes. they add a dash of intrigue without overpowering the face natural harmony.', category='earrings')
        # this also fit with round face
        long_dangle_earrings = Accessory.objects.create(name='long or dangle earrings', image='images/accessories/dangle_earrings.jpg', description='These impart an elegant and sophisticated touch, striking a flawless balance with the chin and forehead.', category='earrings')
        # round
        seet_clear_earrings = Accessory.objects.create(name='Seet clear of circular earrings', image='images/accessories/circular_earrings.jpg', description='Though chic, round earrings can emphasize the roundness of the face even more', category='earrings')
        # square
        round_hoops_earrings = Accessory.objects.create(name='Round or hoops earrings', image='images/accessories/hoops_earrings.jpg', description='These earrings create a stark contrast with the straight lines of a square face, introduing a gentle touch that complements and softens, like pearl stud earrings.', category='earrings')
        long_slender_earrings = Accessory.objects.create(name='Long and slender earrings', image='images/accessories/long_and_slender_earrings.jpg', description='They work magic in visually stretching the face, offering a more elongated and refined look.', category='earrings')
        teardrop_earrings_curved = Accessory.objects.create(name='Teardop earrings or those with curved details', image='images/accessories/teardrop_earrings.jpg', description='The gentle curves in these designs offset the angular structure of square faces', category='earrings')
        avoid_overly_square = Accessory.objects.create(name='Avoid overly square or angular earrings', image='images/accessories/over_square_earrings.jpg', description='They might just amplify the straight lines characteristic of this face shape.', category='earrings')
        # rectangular/elongated/oblong face
        wide_hoops_earrings = Accessory.objects.create(name='Wide hoop earrings', image='images/accessories/wide_hoop_earrings.jpg', description='Large, wide hoops offer a horizontal contrast, lessening the face perceived length.', category='earrings')
        wide_cascading_earrings = Accessory.objects.create(name='Wide cascading detail earrings', image='images/accessories/wide_cascading_earrings.jpg', description='Designs that broaden outward give the cheeks a fuller feel.', category='earrings')
        curved_circular = Accessory.objects.create(name='Curved and circular earrings', image='images/accessories/curved_circular_earrings.jpg', description='These style disrupt the straight lines of a rectangular face, softening its overall look.', category='earrings')
        avoid_overly_long = Accessory.objects.create(name='Avoid overly long or linear earrings', image='images/accessories/over_long_earrings.jpg', description='These can emphasize the face length even more.', category='earrings')
        # heart
        chandelier_earrings = Accessory.objects.create(name='Chandelier earrings', image='images/accessories/chandelier_earrings.jpg', description='Their broader design at the base complements the forehead width, while the elongation creates the illusion of a more elongated, gracefully shaped face.', category='earrings')
        triangle_earrings = Accessory.objects.create(name='Triangle Earrings', image='images/accessories/triangle_earrings.jpg', description='The geometric shape helps to add definition to the jawline while also balancing out the wider forehead. These earrings can range from simple and sleek to intricate and detailed designs, providing plenty of options for any occasion.', category='earrings')
        stud_earrings = Accessory.objects.create(name='Stud Earrings', image='images/accessories/stud_earrings.jpg', description='Opt for larger studs to add volume and balance, and give the illusion of width.', category='earrings')
        
        # Create Recommendations for Oval Face Shape
        recommendation_oval_male = Recommendation.objects.create(face_shape=oval, gender='male')
        recommendation_oval_male.hair_styles.set([pompadour, undercut, comb_over, man_bun]) 
        recommendation_oval_male.accessories.set([transparent_frames, full_rimmed_frames, wooden_frames, square_glasses])

        recommendation_oval_female = Recommendation.objects.create(face_shape=oval, gender='female')
        recommendation_oval_female.hair_styles.set([long_layers, bob_cut, side_swept_bangs])
        recommendation_oval_female.accessories.set([transparent_frames, full_rimmed_frames, wooden_frames, square_glasses, hoops_earrings, teardrop_earrings, geometric_earrings, long_dangle_earrings])
        
        # Create Recommendations for Round Face Shape
        recommendation_round_male = Recommendation.objects.create(face_shape=round_face, gender='male')
        recommendation_round_male.hair_styles.set([french_crop, high_skin_fade, side_part, flat_top])
        
        recommendation_round_female = Recommendation.objects.create(face_shape=round_face, gender='female')
        recommendation_round_female.hair_styles.set([long_layers_volume_top, asymmetrical_bob, pixie_cut_volume])
        recommendation_round_female.accessories.set([transparent_frames, full_rimmed_frames, wooden_frames, square_glasses, teardrop_earrings, geometric_earrings, long_dangle_earrings, seet_clear_earrings])

        # Create Recommendations for Square Face Shape
        recommendation_square_male = Recommendation.objects.create(face_shape=square, gender='male')
        recommendation_square_male.hair_styles.set([side_swept_brush_up, buzzcut, man_bun])
        recommendation_square_male.accessories.set([round_glasses, browline_glasses, colored_oval_glasses])
        
        recommendation_square_female = Recommendation.objects.create(face_shape=square, gender='female')
        recommendation_square_female.hair_styles.set([soft_wispy_bangs, long_soft_layers, side_part_styles])
        recommendation_square_female.accessories.set([round_glasses, browline_glasses, colored_oval_glasses, round_hoops_earrings, long_slender_earrings, teardrop_earrings_curved, avoid_overly_square])
        
        # Create Recommendations for Rectangle Face Shape
        recommendation_rectangle_male = Recommendation.objects.create(face_shape=oblong, gender='male')
        recommendation_rectangle_male.hair_styles.set([crew_cut, side_part])
        recommendation_rectangle_male.accessories.set([round_glasses, browline_glasses, colored_oval_glasses])
        
        recommendation_rectangle_female = Recommendation.objects.create(face_shape=oblong, gender='female')
        recommendation_rectangle_female.hair_styles.set([soft_wispy_bangs, long_soft_layers, side_part_styles])
        recommendation_rectangle_female.accessories.set([round_glasses, browline_glasses, colored_oval_glasses, wide_hoops_earrings, wide_cascading_earrings, curved_circular, avoid_overly_long])

        # Create Recommendations for Heart Face Shape
        recommendation_heart_male = Recommendation.objects.create(face_shape=heart, gender='male')
        recommendation_heart_male.hair_styles.set([shoulder_length_hair, textured_quiff, pompadour])
        recommendation_heart_male.accessories.set([oval_glasses, semi_rimless, rectangular_glasses,square_glasses])
        
        recommendation_heart_female = Recommendation.objects.create(face_shape=heart, gender='female')
        recommendation_heart_female.hair_styles.set([long_side_swept_bangs, chin_length_bob, wavy_lob])
        recommendation_heart_female.accessories.set([oval_glasses, semi_rimless, rectangular_glasses, chandelier_earrings, triangle_earrings, stud_earrings])

        # user = User.objects.get(id=2)
        
        # # Create Feedback
        # feedback = Feedback.objects.create(recommendation=recommendation_oval_male, user=user, comment='Great recommendation!', rating=5)

        # # Create History
        # history = History.objects.create(recommendation=recommendation_oval_male, user=user)

        self.stdout.write(self.style.SUCCESS('Database seeded successfully'))
