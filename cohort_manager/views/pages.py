from django.views.generic import TemplateView


class PageView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['netid'] = self.request.user.username
        return context


class LandingView(PageView):
    template_name = "landing.html"
