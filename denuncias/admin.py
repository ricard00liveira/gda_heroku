from django.contrib import admin
from .models import Denuncia, StatusHistorico, Anexo


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'municipio', 'status', 'prioridade', 'data', 'anonima')
    search_fields = ('numero', 'descricao', 'infrator', 'municipio__nome')
    list_filter = ('status', 'prioridade', 'anonima', 'municipio')
    ordering = ('-data',)
    fieldsets = (
        (None, {
            'fields': (
                'denunciante', 'anonima', 'descricao', 'endereco', 'nr_endereco',
                'ponto_referencia', 'status', 'municipio', 'fato', 'subfato',
                'responsavel', 'is_deleted', 'infrator', 'prioridade',
                'localizacao',
            )
        }),
    )

@admin.register(StatusHistorico)
class StatusHistoricoAdmin(admin.ModelAdmin):
    list_display = ('denuncia', 'status', 'data_alteracao')
    list_filter = ('status',)


@admin.register(Anexo)
class AnexoAdmin(admin.ModelAdmin):
    list_display = ('denuncia', 'descricao', 'data_upload')
