from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_count = 0
        for form in self.forms:
            data = form.cleaned_data
            if data.get('DELETE'):
                continue
            if data.get('is_main'):
                main_count += 1
            if main_count > 1:
                raise ValidationError('Должен быть выбран ровно один основной тег')
        if main_count == 0:
            raise ValidationError('Выберите основной раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass