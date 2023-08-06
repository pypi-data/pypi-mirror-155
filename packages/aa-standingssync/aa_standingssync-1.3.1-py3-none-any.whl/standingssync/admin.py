from django.contrib import admin

from . import tasks
from .models import SyncedCharacter, SyncManager


@admin.register(SyncedCharacter)
class SyncedCharacterAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "character_name",
        "version_hash",
        "_sync_ok",
        "last_sync",
        "last_error",
        "manager",
    )
    list_filter = (
        "last_error",
        "version_hash",
        "last_sync",
        "character_ownership__user",
        "manager",
    )
    actions = ["start_sync_contacts"]
    list_display_links = None

    @admin.display(boolean=True)
    def _sync_ok(self, obj) -> bool:
        return obj.is_sync_ok

    def has_add_permission(self, request):
        return False

    def user(self, obj):
        return obj.character_ownership.user

    def character_name(self, obj):
        return obj.__str__()

    @admin.display(description="Sync selected characters")
    def start_sync_contacts(self, request, queryset):
        names = list()
        for obj in queryset:
            tasks.run_character_sync.delay(sync_char_pk=obj.pk, force_sync=True)
            names.append(str(obj))
        self.message_user(request, "Started syncing for: {}".format(", ".join(names)))


@admin.register(SyncManager)
class SyncManagerAdmin(admin.ModelAdmin):
    list_display = (
        "alliance_name",
        "contacts_count",
        "synced_characters_count",
        "user",
        "character_name",
        "version_hash",
        "_sync_ok",
        "last_sync",
        "last_error",
    )
    list_display_links = None
    actions = ["start_sync_managers"]

    @admin.display(boolean=True)
    def _sync_ok(self, obj) -> bool:
        return obj.is_sync_ok

    def has_add_permission(self, request):
        return False

    def user(self, obj):
        return obj.character_ownership.user if obj.character_ownership else None

    def character_name(self, obj):
        return obj.__str__()

    def alliance_name(self, obj):
        return obj.alliance.alliance_name

    def contacts_count(self, obj):
        return "{:,}".format(obj.contacts.count())

    def synced_characters_count(self, obj):
        return "{:,}".format(obj.synced_characters.count())

    @admin.display(description="Sync selected managers")
    def start_sync_managers(self, request, queryset):
        names = list()
        for obj in queryset:
            tasks.run_manager_sync.delay(manager_pk=obj.pk, force_sync=True)
            names.append(str(obj))
        text = "Started syncing for: {} ".format(", ".join(names))
        self.message_user(request, text)
