from django.conf import settings
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from uw_saml.decorators import group_required
from uw_saml.utils import get_user


# @method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
#                   name='dispatch')
class PageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['netid'] = get_user(self.request)
        return context


class LandingView(PageView):
    template_name = "landing.html"
