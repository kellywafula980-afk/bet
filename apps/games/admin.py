from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import WheelSpin, GameSetting

@admin.register(WheelSpin)
class WheelSpinAdmin(admin.ModelAdmin):
    list_display = ('user', 'bet_amount', 'multiplier', 'win_amount', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('user__phone_number',)

@admin.register(GameSetting)
class GameSettingAdmin(admin.ModelAdmin):
    fields = ('demo_first', 'demo_second', 'demo_third', 'live_forced_multiplier')
    
    def has_add_permission(self, request):
        # Only allow adding if no instance exists
        return not GameSetting.objects.exists()

    def get_actions(self, request):
        # Remove delete action
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def changelist_view(self, request, extra_context=None):
        # If no instance exists, redirect to add view
        if not GameSetting.objects.exists():
            return redirect('admin:games_gamesetting_add')
        # Otherwise redirect to the change view of the first object
        obj = GameSetting.objects.first()
        return redirect(f'admin:games_gamesetting_change', object_id=str(obj.pk))

    def response_add(self, request, obj, post_url_continue=None):
        # After adding, redirect to the change view of the new object
        return redirect('admin:games_gamesetting_change', object_id=str(obj.pk))

    def response_change(self, request, obj):
        # After saving, stay on the change view
        return redirect('admin:games_gamesetting_change', object_id=str(obj.pk))

    # Remove the "Add" button from the admin index
    def has_module_permission(self, request):
        return True
