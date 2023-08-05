import abc

from django.contrib import admin
from django.db import models
from django.http import HttpRequest
from django.utils.html import format_html


class BaseChangeformSubmit(abc.ABC):
    """
    Changeform submit button.

    name must start from underscore as django save submits.
    """

    name: str
    title: str
    confirm: str = ""

    def __init__(self, model_admin: admin.ModelAdmin) -> None:
        self.model_admin = model_admin

    def has_permission(
        self,
        request: HttpRequest,
        instance: models.Model,
    ) -> bool:
        return True

    @abc.abstractmethod
    def handle_submit(
        self,
        request: HttpRequest,
        instance: models.Model,
    ) -> None:
        """Handle submit."""

    def get_content(self) -> str:
        onclick = (
            "return confirm('{0}')".format(self.confirm)
            if self.confirm
            else None
        )

        button_attrs = {
            "type": "submit",
            "value": self.title,
            "name": self.name,
            "onclick": onclick,
        }

        return format_html(
            "<input {0}/>".format(
                " ".join(
                    (
                        '{0}="{1}"'.format(tag_attr, tag_value)
                        for tag_attr, tag_value in button_attrs.items()
                        if tag_value
                    ),
                ),
            ),
        )
