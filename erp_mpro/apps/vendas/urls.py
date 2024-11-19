# -*- coding: utf-8 -*-

from django.urls import re_path
from . import views

app_name = 'vendas'

urlpatterns = [
    # Orçamentos de Venda
    re_path(r'^orcamentovenda/adicionar/$', views.AdicionarOrcamentoVendaView.as_view(), name='addorcamentovendaview'),
    re_path(r'^orcamentovenda/listaorcamentovenda/$', views.OrcamentoVendaListView.as_view(), name='listaorcamentovendaview'),
    re_path(r'^orcamentovenda/editar/(?P<pk>[0-9]+)/$', views.EditarOrcamentoVendaView.as_view(), name='editarorcamentovendaview'),
    re_path(r'^orcamentovenda/listaorcamentovenda/vencidos/$', views.OrcamentoVendaVencidosListView.as_view(), name='listaorcamentovendavencidoview'),
    re_path(r'^orcamentovenda/listaorcamentovenda/hoje/$', views.OrcamentoVendaVencimentoHojeListView.as_view(), name='listaorcamentovendahojeview'),

    # Pedidos de Venda
    re_path(r'^pedidovenda/adicionar/$', views.AdicionarPedidoVendaView.as_view(), name='addpedidovendaview'),
    re_path(r'^pedidovenda/listapedidovenda/$', views.PedidoVendaListView.as_view(), name='listapedidovendaview'),
    re_path(r'^pedidovenda/editar/(?P<pk>[0-9]+)/$', views.EditarPedidoVendaView.as_view(), name='editarpedidovendaview'),
    re_path(r'^pedidovenda/listapedidovenda/atrasados/$', views.PedidoVendaAtrasadosListView.as_view(), name='listapedidovendaatrasadosview'),
    re_path(r'^pedidovenda/listapedidovenda/hoje/$', views.PedidoVendaEntregaHojeListView.as_view(), name='listapedidovendahojeview'),

    # Condição de Pagamento
    re_path(r'^pagamento/adicionar/$', views.AdicionarCondicaoPagamentoView.as_view(), name='addcondicaopagamentoview'),
    re_path(r'^pagamento/listacondicaopagamento/$', views.CondicaoPagamentoListView.as_view(), name='listacondicaopagamentoview'),
    re_path(r'^pagamento/editar/(?P<pk>[0-9]+)/$', views.EditarCondicaoPagamentoView.as_view(), name='editarcondicaopagamentoview'),

    # Views AJAX
    re_path(r'^infocondpagamento/$', views.InfoCondicaoPagamento.as_view(), name='infocondpagamento'),
    re_path(r'^infovenda/$', views.InfoVenda.as_view(), name='infovenda'),

    # Gerar PDF
    re_path(r'^gerarpdforcamentovenda/(?P<pk>[0-9]+)/$', views.GerarPDFOrcamentoVenda.as_view(), name='gerarpdforcamentovenda'),
    re_path(r'^gerarpdfpedidovenda/(?P<pk>[0-9]+)/$', views.GerarPDFPedidoVenda.as_view(), name='gerarpdfpedidovenda'),

    # Operações de Venda
    re_path(r'^gerarpedidovenda/(?P<pk>[0-9]+)/$', views.GerarPedidoVendaView.as_view(), name='gerarpedidovenda'),
    re_path(r'^copiarorcamentovenda/(?P<pk>[0-9]+)/$', views.GerarCopiaOrcamentoVendaView.as_view(), name='copiarorcamentovenda'),
    re_path(r'^copiarpedidovenda/(?P<pk>[0-9]+)/$', views.GerarCopiaPedidoVendaView.as_view(), name='copiarpedidovenda'),
    re_path(r'^cancelarorcamentovenda/(?P<pk>[0-9]+)/$', views.CancelarOrcamentoVendaView.as_view(), name='cancelarorcamentovenda'),
    re_path(r'^cancelarpedidovenda/(?P<pk>[0-9]+)/$', views.CancelarPedidoVendaView.as_view(), name='cancelarpedidovenda'),
]
