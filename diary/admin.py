from django.contrib import admin
from .models import Record, RecordType, AbstractRecordType, CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        ('Info', {'fields': ('email', 'password', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    readonly_fields = ('date_joined',)
    search_fields = ('email',)
    ordering = ('email',)


@admin.register(AbstractRecordType)
class AbstractRecordTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']
    list_filter = ['id']
    readonly_fields = ['id']


class AbstractRecordTypeInline(admin.StackedInline):
    model = AbstractRecordType.children.through

@admin.register(RecordType)
class RecordTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']
    search_fields = ['name']
    list_filter = ['id']
    readonly_fields = ['id']
    inlines = [AbstractRecordTypeInline]


class RecordTypeInline(admin.StackedInline):
    model = RecordType.records.through

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'is_important', 'create_date', 'edit_date']
    list_filter = ['create_date', 'edit_date', 'is_important']
    search_fields = ['name', 'id']
    readonly_fields = ['create_date', 'edit_date', 'id']
    list_display_links = ['name']
    list_editable = ['is_important']
    inlines = [RecordTypeInline]
