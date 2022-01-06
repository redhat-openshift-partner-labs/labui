from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# Vertical 

class LightSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Light Sidebar", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-light-sidebar.html', greeting)


class CompactSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Compact Sidebar", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-compact-sidebar.html', greeting)


class IconSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Icon Sidebar", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-icon-sidebar.html', greeting)


class BoxWidthSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Boxed Width", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-boxed-width-sidebar.html', greeting)


class PreloaderSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Preloader ", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-preloader-sidebar.html', greeting)


class ColoredSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Colored Sidebar", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-colored-sidebar.html', greeting)


class ScrollableSidebarView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Scrollable ", 'pageview': "Layouts"}
        return render(request, 'layout/vertical/layout-scrollable-sidebar.html', greeting)


# Horizontal

class HorizontalView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Horizontal Layout", 'pageview': "Layouts"}
        return render(request, 'layout/horizontal/layout-horizontal.html', greeting)


class LightTopbarHoriView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Horizontal Topbar Light", 'pageview': "Layouts"}
        return render(request, 'layout/horizontal/layout-hori-topbar-light.html', greeting)


class BoxedWidthHoriView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Horizontal Boxed Width", 'pageview': "Layouts"}
        return render(request, 'layout/horizontal/layout-hori-boxed-width.html', greeting)


class PreloaderHoriView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Horizontal Preloader Layout", 'pageview': "Layouts"}
        return render(request, 'layout/horizontal/layout-hori-preloader.html', greeting)


class ColoredheaderHoriView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Horizontal Topbar Colored", 'pageview': "Layouts"}
        return render(request, 'layout/horizontal/layout-hori-colored-header.html', greeting)


class ScrollableHoriView(LoginRequiredMixin, View):
    def get(self, request):
        greeting = {'heading': "Horizontal Scrollable Layout", 'pageview': "Layouts"}
        return render(request, 'layout/horizontal/layout-hori-scrollable.html', greeting)
