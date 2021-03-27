from .models import Tag

def menu(request):
    nav_tags = Tag.objects.all()[:4]
    return { 'nav_tags' : nav_tags,
    }