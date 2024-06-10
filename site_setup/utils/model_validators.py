from django.core.exceptions import ValidationError


def validate_png(image):
    if not image.name.lower().endswith('.png'):
        raise ValidationError('Image needs to be .png')
