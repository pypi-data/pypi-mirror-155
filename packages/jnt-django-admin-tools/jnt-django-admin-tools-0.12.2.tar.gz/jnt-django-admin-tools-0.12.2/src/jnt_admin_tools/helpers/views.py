from functools import update_wrapper

from django.contrib import admin
from django.contrib.admin.utils import unquote
from django.http import HttpResponse
from django.views import View


def wrap_model_instance_admin_view(
    model_admin: admin.ModelAdmin,
    view: View,
) -> HttpResponse:
    """Wraps view to use at instance admin pages."""

    def wrap():
        def wrapper(request, object_id, **kwargs):
            instance = model_admin.get_object(request, unquote(object_id))
            if instance is None:
                return model_admin._get_obj_does_not_exist_redirect(
                    request,
                    model_admin.model._meta,
                    object_id,
                )

            return model_admin.admin_site.admin_view(
                view.as_view(
                    model_admin=model_admin,
                    instance=instance,
                )
            )(request, **kwargs)

        return update_wrapper(wrapper, view)

    return wrap()


def wrap_model_list_admin_view(
    model_admin: admin.ModelAdmin,
    view: View,
) -> HttpResponse:
    """Wraps view to use at models list admin pages."""

    def wrap():
        def wrapper(request, **kwargs):
            return model_admin.admin_site.admin_view(
                view.as_view(
                    model_admin=model_admin,
                )
            )(request, **kwargs)

        return update_wrapper(wrapper, view)

    return wrap()
