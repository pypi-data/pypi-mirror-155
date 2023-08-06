# coding=utf-8
from enum import Enum

from alas_ce0.common.client_base import EntityClientBase
from alas_ce0.management.task import TaskClient


def get_delivery_order_process_type_dic():
    return {
        2: "Recepción Física TL (Viejo Formato)",
        8: "Agendamiento de Entrega",
        9: "Ingreso a Ce0",
        10: "Recepción Física TL (Nuevo Formato)",
    }
    
def get_delivery_order_status_dic():
    return {
        1: "Planificación",
        2: "Planificación Modificada",
        3: "Planificación Aprobada",
        4: "Recibida Virtual",
        5: "Recibida Físico",
        6: "En Maquilado",
        7: "Rechazado B2B",
        8: "Espera TI",
        9: "Viajando a SER",
        10: "Recibido SER",
        11: "Espera Reemplazo",
        12: "Entrega Confirmada",
        13: "Entrega No Confirmada",
        14: "Entrega Aplazada",
        15: "Entrega Rechazada",
        16: "Entrega Ruteada",
        17: "Viajando B2C",
        18: "Entregada",
        19: "No Entregada",
        20: "PackagingIssueReturned",
        21: "ODFReturned",
        22: "ODSFReturned",
        23: "Pending",
        24: "PrioritizedPending",
        25: "No Entregable",
        26: "B2BReturning",
        27: "B2BReturned",
        28: "Evaluada B2C",
        29: "Rechazada en Terreno",
        30: "Reagendada",
        31: "Intento de Contacto",
        32: "Recibido CD",
        33: "Recibido Mensajero",
        34: "Recuperada",
        35: "Rechazado Cliente",
        36: "Rechazado Alas"
    }


class DeliveryOrderProcessType(Enum):
    B2bDelivery = 1
    B2bReception = 2
    Packaging = 3
    CarrierDispatch = 4
    CarrierDelivery = 5
    SerReception = 6
    VehicleLoad = 7
    B2cDelivery = 8
    Ce0Reception = 9
    # Inboxs
    B2bReceived = 10
    DcReceived = 11
    CarrierReceived = 12
    SerReceived = 13
    CourierReceived = 14


class DeliveryOrderStakeholderType(Enum):
    Sender = 1
    Receiver = 2
    ReceiverEmployee = 3
    PackagerEmployee = 4
    DispatcherEmployee = 5
    IntermediateCarrier = 6
    RegionalPartner = 7
    SchedulerEmployee = 8
    ControllerEmployee = 9
    MessengerEmployee = 10
    DeliveryManager = 11


class DeliveryOrderStatusType(Enum):
    Planning = 1
    PlanningChanged = 2
    PlanningApproved = 3
    VirtuallyReceived = 4
    PhysicallyReceived = 5
    Packaging = 6
    B2BReceptionRejected = 7
    TIReceptionWaiting = 8
    SERTravelling = 9
    SERReceived = 10
    ReplacementWaiting = 11
    DeliveryConfirmed = 12
    DeliveryNotConfirmed = 13
    DeliveryPostponed = 14
    DeliveryRejected = 15
    DeliveryScheduled = 16
    B2CTraveling = 17
    Delivered = 18
    NotDelivered = 19
    PackagingIssueReturned = 20
    ODFReturned = 21
    ODSFReturned = 22
    Pending = 23
    PrioritizedPending = 24
    NotDeliverable = 25
    B2BReturning = 26
    B2BReturned = 27
    B2CEvaluated = 28
    B2CRejected = 29
    DeliveryRescheduled = 30
    ContactAttempt = 31
    DistributionCenterReceived = 32
    DeliveryCourierReceived = 33
    Recovered = 34
    B2CReceptionRejected = 35
    ALASRejected = 36
    
    
def get_macro_status(delivery_order):
    in_route_amount = len(filter(lambda x: x == 17, delivery_order['statuses']))
    status = get_delivery_order_status_dic()

    if delivery_order['status'] in [
        DeliveryOrderStatusType.VirtuallyReceived.value,
        DeliveryOrderStatusType.PhysicallyReceived.value,
        DeliveryOrderStatusType.B2BReceptionRejected.value,
        DeliveryOrderStatusType.Delivered.value] or delivery_order['status'] >= DeliveryOrderStatusType.ALASRejected.value:
        return status[delivery_order['status']]
    elif delivery_order['status'] in [
        DeliveryOrderStatusType.DeliveryRejected.value,
        DeliveryOrderStatusType.B2CRejected.value,
        DeliveryOrderStatusType.B2CReceptionRejected.value]:
        return 'Rechazado Cliente'
    elif delivery_order['status'] == DeliveryOrderStatusType.B2CTraveling.value:
        return 'En Ruta {0}'.format(in_route_amount)
    elif delivery_order['status'] == DeliveryOrderStatusType.NotDeliverable.value:
        return 'Rechazado 3 Intentos'
    else:
        if in_route_amount > 0:
            return 'Pendiente Ruta {0}'.format(in_route_amount + 1)
    return 'En Planta'

def get_b2c_delivery_events(delivery_order):
    return filter(
        lambda x: (x['status'] == 15 and 'b2c_delivery_actual' in x['info']) or
                    x['status'] == 18 or
                    x['status'] == 19 or
                    x['status'] in [29, 35, 36],
        delivery_order['events_info']
    )
    
def get_not_delivered_reason(event_info):
    reasons = ['No hay quien reciba', 'Dirección Incompleta', 'Problema Documentación', 'Siniestro', 'Merma']

    if 'not_delivered_3_reason' in event_info and event_info['not_delivered_3_reason']:
        return reasons[event_info['not_delivered_3_reason'] - 1]
    if 'not_delivered_2_reason' in event_info and event_info['not_delivered_2_reason']:
        return reasons[event_info['not_delivered_2_reason'] - 1]
    if 'not_delivered_1_reason' in event_info and event_info['not_delivered_1_reason']:
        return reasons[event_info['not_delivered_1_reason'] - 1]
    return None
    
def get_b2c_delivery_status(b2c_delivery_events, b2c_delivery_date, attempt):
    if b2c_delivery_date:
        if b2c_delivery_events[attempt-1]['status'] in [29, 35] \
                or (b2c_delivery_events[attempt-1]['status'] == 15
                    and 'b2c_delivery_actual' in b2c_delivery_events[attempt-1]['info']):
            return 'Rechazado Cliente'
        elif b2c_delivery_events[attempt-1]['status'] == 18:
            return 'Entregado'
        else:
            reason = get_not_delivered_reason(b2c_delivery_events[attempt-1]['info'])
            return 'No Entregado' if not reason else reason
    return ''


class DeliveryOrderRequestClient(EntityClientBase):
    entity_endpoint_base_url = '/delivery/delivery-order-requests/'

    def __init__(self, country_code='cl', **kwargs):
        super(DeliveryOrderRequestClient, self).__init__(**kwargs)
        self.entity_endpoint_base_url += country_code + '/'


class DeliveryOrderClient(EntityClientBase):
    entity_endpoint_base_url = '/delivery/delivery-orders/'

    def __init__(self, country_code='cl', **kwargs):
        super(DeliveryOrderClient, self).__init__(**kwargs)
        self.entity_endpoint_base_url += country_code + '/'
        self.headers['Authorization'] = self.headers['Authorization'].replace("\n", "")

    def create_from_request(self, delivery_order_request_id, pasync=True):
        params = {
            'delivery_order_request_id': delivery_order_request_id
        }

        if pasync:
            return TaskClient(**self.args).enqueue('delivery-order-create', params)
        else:
            return self.http_post_json(self.entity_endpoint_base_url + "_create-from-request", params)

    def create_delivery_order_label_sync(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_create-delivery-order-label-sync", params)

    def get_agenda(self, date_from, date_to, process_types, stakeholder_types=None):
        param = {
            'date_from': date_from,
            'date_to': date_to,
            'process_types': process_types,
            'stakeholder_types': stakeholder_types
        }

        return self.http_post_json(self.entity_endpoint_base_url + "_agenda", param)

    def change_status(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_change-status".format(id), params)

    def change_planning(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_change-planning".format(id), params)

    def upload_file(self, user_name, sender_code, base64_content, file_format="txt", file_name=None, family=1):
        params = {
            'user_name': user_name,
            'sender_code': sender_code,
            'base64_content': base64_content,
            'format': file_format,
            'file_name': file_name,
            'family': family
        }
        return self.http_post_json(self.entity_endpoint_base_url + "_upload-file", params)

    def validate_customer(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_validate-customer".format(id), params)

    def confirm_b2c_delivery(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_confirm-b2c-delivery".format(id), params)

    def search_for_daily_planning(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_search-for-daily-planning", params)

    def start_planning(self, id):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_start-planning".format(id), {})

    def search_for_route_creation(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_search-for-route-creation", params)

    def get_items(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_get-items", params)

    def send_notification(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_send-notification".format(id), params)

    def change_b2c_delivery(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_change-b2c-delivery".format(id), params)

    def masive_change_b2c_delivery(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_masive_change-b2c-delivery", params)

    def change_destination(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_change-destination".format(id), params)

    def set_b2c_informed_geo_location(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_set-b2c-informed-geo-location".format(id), params)

    def route_now(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_route-now".format(id), params)

    def get_document_content(self, id, doc_type):
        return self.http_get(
            self.entity_endpoint_base_url + "{0}/document/{1}/_content".format(id, doc_type)
        )

    def get_attachment_content(self, id, att_file_name):
        return self.http_get(
            self.entity_endpoint_base_url + "{0}/attachment/{1}".format(id, att_file_name)
        )

    def get_delivery_form(self, id):
        return self.http_get_json(
            self.entity_endpoint_base_url + "{0}/_delivery-form".format(id)
        )

    def set_delivery_form(self, id, delivery_form):
        return self.http_post_json(
            self.entity_endpoint_base_url + "{0}/_delivery-form".format(id), delivery_form
        )

    def force_b2c_contact(self, id):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_force-b2c-contact".format(id), {})

    def validate_package(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_validate-package".format(id), params)

    def process_create_labels_by_ids(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_process-create-labels-by-ids", params)

    def create_label_sync(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_create-label-sync".format(id), params)

    def process_physical_reception(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_process-physical-reception", params)
    
    def slack_report_send(self, params):
        return self.http_post_json(self.entity_endpoint_base_url + "_slack-report-send", params)

    def physically_receive(self, id, event_info, pasync=True):
        if pasync:
            return TaskClient(**self.args).enqueue('delivery-order-physically-receive', {
                'delivery_order_id': id,
                'event_info': event_info
            })
        else:
            return self.http_post_json(self.entity_endpoint_base_url + "{0}/_physically-receive".format(id), event_info)

    # region added by new project inboxs
    def distribution_center_receive(self, id, event_info, pasync=True):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_distribution-center-receive".format(id), event_info)

    def ser_travelling_receive(self, id, event_info, pasync=True):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_ser-travelling-receive".format(id), event_info)

    def ser_received_receive(self, id, event_info, pasync=True):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_ser-received-receive".format(id), event_info)

    def delivery_courier_receive(self, id, event_info, pasync=True):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_delivery-courier-receive".format(id), event_info)
    # endregion

    def search_batch(self, search_info):
        return self.http_post_json(self.entity_endpoint_base_url + "_search-batch", search_info)

    def get_device_assigned(self, id):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_device-assigned".format(id), {})

    def recover(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_recover".format(id), params)

    def submit_form(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_submit-form".format(id), params)

    def update_documents(self, id, params):
        return self.http_post_json(self.entity_endpoint_base_url + "{0}/_update-documents".format(id), params)


class DeliveryOrderMessagingClient(EntityClientBase):
    entity_endpoint_base_url = '/delivery/delivery-orders-messaging/'


class DeliveryOrdersForRouteClient(EntityClientBase):
    entity_endpoint_base_url = '/delivery/delivery-orders-for-route/'


class DeliveryOrderIntegrationAuditClient(EntityClientBase):
    entity_endpoint_base_url = '/delivery/delivery-orders-integration-audit/'
