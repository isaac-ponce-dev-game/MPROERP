# -*- coding: utf-8 -*-

from django.urls import re_path
from . import views

app_name = 'estoque'
urlpatterns = [
    # Consulta de estoque
    re_path(r'consultaestoque/$', views.ConsultaEstoqueView.as_view(),
            name='consultaestoqueview'),

    # Local de estoque
    re_path(r'local/saida/adicionar/$',
            views.AdicionarLocalEstoqueView.as_view(), name='addlocalview'),
    re_path(r'local/listalocal/$', views.LocalEstoqueListView.as_view(),
            name='listalocalview'),
    re_path(r'local/editar/(?P<pk>[0-9]+)/$',
            views.EditarLocalEstoqueView.as_view(), name='editarlocalview'),

    # Movimento de estoque
    re_path(r'movimentos/$', views.MovimentoEstoqueListView.as_view(),
            name='listamovimentoestoqueview'),

    # EntradaEstoque
    re_path(r'movimento/adicionarentrada/$',
            views.AdicionarEntradaEstoqueView.as_view(), name='addentradaestoqueview'),
    re_path(r'movimento/listaentradas/$', views.EntradaEstoqueListView.as_view(),
            name='listaentradasestoqueview'),
    re_path(r'movimento/editarentrada/(?P<pk>[0-9]+)/$',
            views.DetalharEntradaEstoqueView.as_view(), name='detalharentradaestoqueview'),

    # SaidaEstoque
    re_path(r'movimento/adicionarsaida/$',
            views.AdicionarSaidaEstoqueView.as_view(), name='addsaidaestoqueview'),
    re_path(r'movimento/listasaidas/$', views.SaidaEstoqueListView.as_view(),
            name='listasaidasestoqueview'),
    re_path(r'movimento/editarsaida/(?P<pk>[0-9]+)/$',
            views.DetalharSaidaEstoqueView.as_view(), name='detalharsaidaestoqueview'),

    # TransferenciaEstoque
    re_path(r'movimento/adicionartransferencia/$',
            views.AdicionarTransferenciaEstoqueView.as_view(), name='addtransferenciaestoqueview'),
    re_path(r'movimento/listatransferencias/$', views.TransferenciaEstoqueListView.as_view(),
            name='listatransferenciasestoqueview'),
    re_path(r'movimento/editartransferencia/(?P<pk>[0-9]+)/$',
            views.DetalharTransferenciaEstoqueView.as_view(), name='detalhartransferenciaestoqueview'),
]
