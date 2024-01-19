from .models import Profile


def profile_side_bar(request):
    profile = None
    if request.user.is_authenticated:
        profile = request.user.profile
    return {"profile": profile}
    ...
