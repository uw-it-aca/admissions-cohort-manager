# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.views.generic import TemplateView


class PurpleGoldEmbed(TemplateView):
    template_name = "purplegold_embed.html"
