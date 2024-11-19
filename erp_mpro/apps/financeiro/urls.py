# -*- coding: utf-8 -*-

from django.urls import re_path
from . import views

app_name = 'financeiro'
urlpatterns = [
    # Lancamentos
    re_path(r'gerarlancamento/$', views.GerarLancamentoView.as_view(), name='gerarlancamento'),
    re_path(r'lancamentos/$', views.LancamentoListView.as_view(), name='listalancamentoview'),

    # Contas a pagar
    re_path(r'contapagar/adicionar/$', views.AdicionarContaPagarView.as_view(), name='addcontapagarview'),
    re_path(r'contapagar/listacontapagar/$', views.ContaPagarListView.as_view(), name='listacontapagarview'),
    re_path(r'contapagar/editar/(?P<pk>[0-9]+)/$', views.EditarContaPagarView.as_view(), name='editarcontapagarview'),
    re_path(r'contapagar/listacontapagar/atrasadas/$', views.ContaPagarAtrasadasListView.as_view(), name='listacontapagaratrasadasview'),
    re_path(r'contapagar/listacontapagar/hoje/$', views.ContaPagarHojeListView.as_view(), name='listacontapagarhojeview'),

    # Contas a receber
    re_path(r'contareceber/adicionar/$', views.AdicionarContaReceberView.as_view(), name='addcontareceberview'),
    re_path(r'contareceber/listacontareceber/$', views.ContaReceberListView.as_view(), name='listacontareceberview'),
    re_path(r'contareceber/editar/(?P<pk>[0-9]+)/$', views.EditarContaReceberView.as_view(), name='editarcontareceberview'),
    re_path(r'contareceber/listacontareceber/atrasadas/$', views.ContaReceberAtrasadasListView.as_view(), name='listacontareceberatrasadasview'),
    re_path(r'contareceber/listacontareceber/hoje/$', views.ContaReceberHojeListView.as_view(), name='listacontareceberhojeview'),

    # Pagamentos
    re_path(r'pagamento/adicionar/$', views.AdicionarSaidaView.as_view(), name='addpagamentoview'),
    re_path(r'pagamento/listapagamento/$', views.SaidaListView.as_view(), name='listapagamentosview'),
    re_path(r'pagamento/editar/(?P<pk>[0-9]+)/$', views.EditarSaidaView.as_view(), name='editarpagamentoview'),

    # Recebimentos
    re_path(r'recebimento/adicionar/$', views.AdicionarEntradaView.as_view(), name='addrecebimentoview'),
    re_path(r'recebimento/listarecebimento/$', views.EntradaListView.as_view(), name='listarecebimentosview'),
    re_path(r'recebimento/editar/(?P<pk>[0-9]+)/$', views.EditarEntradaView.as_view(), name='editarrecebimentoview'),

    # Faturar Pedidos
    re_path(r'faturarpedidovenda/(?P<pk>[0-9]+)/$', views.FaturarPedidoVendaView.as_view(), name='faturarpedidovenda'),
    re_path(r'faturarpedidocompra/(?P<pk>[0-9]+)/$', views.FaturarPedidoCompraView.as_view(), name='faturarpedidocompra'),

    # Plano de contas
    re_path(r'planodecontas/$', views.PlanoContasView.as_view(), name='planocontasview'),
    re_path(r'planodecontas/adicionargrupo/$', views.AdicionarGrupoPlanoContasView.as_view(), name='addgrupoview'),
    re_path(r'planodecontas/editargrupo/(?P<pk>[0-9]+)/$', views.EditarGrupoPlanoContasView.as_view(), name='editargrupoview'),

    # Fluxo de caixa
    re_path(r'fluxodecaixa/$', views.FluxoCaixaView.as_view(), name='fluxodecaixaview'),
]
