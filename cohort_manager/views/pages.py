from django.conf import settings
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.clickjacking import xframe_options_exempt
from uw_saml.decorators import group_required
from uw_saml.utils import get_user


class PageView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['netid'] = get_user(self.request)
        context['aat_env'] = settings.AAT_ENV
        return context


@method_decorator(login_required(),
                  name='dispatch')
@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
@method_decorator(xframe_options_exempt, name='dispatch')
class LandingView(PageView):
    template_name = "landing.html"

    def dispatch(self, *args, **kwargs):
        response = super(LandingView, self).dispatch(*args, **kwargs)
        response['Content-Security-Policy'] = "frame-ancestors *.uw.edu"
        return response


@method_decorator(login_required(),
                  name='dispatch')
@method_decorator(group_required(settings.ALLOWED_USERS_GROUP),
                  name='dispatch')
class AdminView(PageView):
    template_name = "admin.html"

    def get_context_data(self, **kwargs):
        context = {}
        context['major_url'] = \
            self.request.build_absolute_uri('/iframe/bulk_view/1')
        context['cohort_url'] = \
            self.request.build_absolute_uri('/iframe/bulk_view/2')
        context['debug'] = settings.DEBUG
        return context
