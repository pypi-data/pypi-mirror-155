import json
from django.conf import settings
from django.conf.urls import url
from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from django_filters import rest_framework as filters
from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.utils import BadRequestError, page_models_from_string
from wagtail.contrib.sitemaps.views import sitemap as wagtail_sitemap
from wagtail.contrib.redirects.models import Redirect
from wagtail.core.models import Site, Page
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import RedirectSerializer
from .utils import exclude_page_type, hash_draft_code


def filter_page_type(queryset, page_models):
    qs = queryset.none()

    for model in page_models:
        qs |= queryset.type(model)

    return qs


class SPAExtendedPagesAPIEndpoint(PagesAPIViewSet):
    """
    Wagtail preview doesn't work with a JS client

    This tweaked Pages API will serve the latest draft version of a page when
    `?draft=[draft_code]` is set.

    Added `site` (id) and `site_hostname` query parameters to filter by site.

    Added `exclude_type` to exclude wagtail page types
    """
    known_query_parameters = PagesAPIViewSet.known_query_parameters.union([
        'site',
        'site_hostname',
        'exclude_type',
    ])

    def check_valid_draft_code(self, page_id=None):
        """ Check computed hashes for the Date + PREVIEW_DRAFT_CODE + Page ID """
        settings_draft_code = getattr(settings, 'PREVIEW_DRAFT_CODE', None)
        if settings_draft_code:
            user_draft_code = self.request.GET.get('draft')
            if page_id is None:
                page_id = self.request.parser_context['kwargs'].get('pk')
            if user_draft_code and page_id:
                settings_draft_code_hash = hash_draft_code(settings_draft_code, page_id)
                if user_draft_code == settings_draft_code_hash:
                    return True
        return False

    def detail_view(self, request, pk):
        if self.check_valid_draft_code(pk):
            # Get all, not just live
            instance = get_object_or_404(Page.objects.all(), pk=pk).specific
            instance = instance.get_latest_revision_as_page()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super().detail_view(request, pk)

    def find_view(self, request):
        """
        Override to append preview GET param to redirect url
        """
        url = super().find_view(request).url
        draft_code = request.GET.get('draft')
        draft_code = getattr(settings, 'PREVIEW_DRAFT_CODE', None)
        if draft_code and request.GET.get('draft') == draft_code:
            url += f"?draft={draft_code}"
        return redirect(url)
    
    def route(self, page, request, path_components):
        """ Alternative version of Page.route that supports draft pages """
        if path_components:
            # request is for a child of this page
            child_slug = path_components[0]
            remaining_components = path_components[1:]

            # Look for page slug first.
            # Luckily, wagtail admin will not allow even a draft to have a slug that matches a published page
            subpage = page.get_children().filter(slug=child_slug).first()
            if not subpage:
                # Look in revisions if page slug not found
                slug_json = '"slug": "{}",'.format(child_slug)
                # It's possible that multiple revision slugs exist for two different pages.
                # In such a case, it picks the page with the most recent revision. The hash will then fail and 404. This is a limitation.
                # In theory we could work around this by returning all matching pages and checking the draft hash of each one
                # Merge requests welcome
                subpage = page.get_descendants().filter(revisions__content_json__contains=slug_json).order_by('-revisions__created_at').first()
                if not subpage:
                    raise Http404

                # Confirm exact revision slug data (contains is not exact enough)
                revision_slug = json.loads(subpage.get_latest_revision().content_json).get("slug")
                if revision_slug != child_slug:
                    raise Http404

            return self.route(subpage, request, remaining_components)
        return page


    def detail_by_path_view(self, request):
        """
        This should work similar to find_view except that it returns the detail response instead
        of a redirect. It also supports draft codes.
        This can be useful with node, which has complications when handling redirects in a
        different manner than a web browser.
        """
        queryset = self.get_queryset()

        if request.GET.get('draft'):
            queryset = self.get_queryset(include_drafts=True)
            # We have to reimplement some of wagtail's logic to include unpublished pages
            site = self.filter_by_site()
            root_page = site.root_page.specific
            path = request.GET['html_path']
            path_components = [component for component in path.split('/') if component]
            obj = self.route(root_page, request, path_components)
            if obj and self.check_valid_draft_code(obj.id):
                self.kwargs['pk'] = obj.pk
                return self.detail_view(request, obj.pk)

        try:
            obj = self.find_object(queryset, request)

            if obj is None:
                raise self.model.DoesNotExist

        except self.model.DoesNotExist:
            raise Http404("not found")

        self.kwargs['pk'] = obj.pk
        return self.detail_view(request, obj.pk)

    def get_queryset(self, include_drafts=False):
        """
        Override this to allow for providing drafts

        This non working shows a better intent of what we want to do

        def get_queryset(self):
            self.filter_by_site()
            queryset = super().get_queryset()
            queryset = self.exclude_page_types(queryset)
            if self.check_valid_draft_code():
                # We can't remove from a queryset
                queryset = queryset.include_drafts_instead_of_live_public()
            return queryset
        """
        # Allow pages to be filtered to a specific type
        try:
            models = page_models_from_string(self.request.GET.get('type', 'wagtailcore.Page'))
        except (LookupError, ValueError):
            raise BadRequestError("type doesn't exist")

        if not models:
            models = [Page]

        if len(models) == 1:
            queryset = models[0].objects.all()
        else:
            queryset = Page.objects.all()

            # Filter pages by specified models
            queryset = filter_page_type(queryset, models)

        # Get live pages that are not in a private section
        if not self.check_valid_draft_code() and include_drafts is False:  # Unless draft code
            queryset = queryset.public().live()

        # Filter by site
        site = self.filter_by_site()
        if site:
            queryset = queryset.descendant_of(site.root_page, inclusive=True)
        else:
            # No sites configured
            queryset = queryset.none()

        queryset = self.exclude_page_types(queryset)
        return queryset

    def exclude_page_types(self, queryset):
        exclude_type = self.request.GET.get('exclude_type', None)
        if exclude_type is not None:
            try:
                models = page_models_from_string(exclude_type)
            except (LookupError, ValueError):
                raise BadRequestError("type doesn't exist")
            queryset = exclude_page_type(queryset, models)
        return queryset

    def filter_by_site(self):
        """
        Allow API consumer to manually specify the site
        Set query parameter `site` to the site id
        or set query parameter `site_hostname` to the hostname such as www.example.com 
        """
        site = None
        site_id = self.request.GET.get('site', None)
        if site_id:
            try:
                site = Site.objects.get(id=site_id)
            except Site.DoesNotExist:
                raise BadRequestError("Site not found")
        site_hostname = self.request.GET.get('site_hostname', None)
        if site_hostname:
            try:
                site = Site.objects.get(hostname=site_hostname)
            except Site.DoesNotExist:
                raise BadRequestError("Site not found")
        if site is None:
            site = Site.find_for_request(self.request)
        self.request._wagtail_site = site
        return site

    @classmethod
    def get_urlpatterns(cls):
        urlpatterns = super().get_urlpatterns()
        urlpatterns.append(
            url(r'^detail_by_path/$',
                cls.as_view({'get': 'detail_by_path_view'}), name='detail_by_path')
        )
        return urlpatterns


class RedirectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Redirect.objects.all()
    serializer_class = RedirectSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('old_path', 'site')
    model = Redirect

    @classmethod
    def get_urlpatterns(cls):
        """
        This returns a list of URL patterns for the endpoint
        """
        return [
            url(r'^$', cls.as_view({'get': 'list'})),
        ]


def sitemap(request, sitemaps=None, **kwargs):
    """ Extended wagtail sitemap view. Adds `site` query parameter to site site ID """
    site_id = request.GET.get('site', None)
    if site_id:
        try:
            request._wagtail_site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            pass

    return wagtail_sitemap(request, sitemaps=sitemaps, **kwargs)
