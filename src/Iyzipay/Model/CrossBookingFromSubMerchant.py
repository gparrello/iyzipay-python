from src.Iyzipay.HttpClient import HttpClient
from src.Iyzipay.IyzipayResource import IyzipayResource
from src.Iyzipay.JsonBuilder import JsonBuilder
from src.Iyzipay.RequestStringBuilder import RequestStringBuilder


class CrossBookingFromSubMerchant(IyzipayResource):
    @classmethod
    def create(cls, request, options):
        json_encoded_request = cls.get_json_object(request)
        pki_string_request = cls.to_pki_request_string(request)
        raw_result = HttpClient.create().post(options['base_url'] + "/crossbooking/send",
                                              IyzipayResource.get_http_header(pki_string_request, options),
                                              json_encoded_request)
        json_result = raw_result.json()
        return json_result

    @classmethod
    def get_json_object(cls, request):
        json_object = JsonBuilder.from_json_object(super(CrossBookingFromSubMerchant, cls).get_json_object(request)) \
            .add("subMerchantKey", request.get('sub_merchant_key', None)) \
            .add_price("price", request.get('price', None)) \
            .add("reason", request.get('reason', None)) \
            .get_object()
        return JsonBuilder.json_encode(json_object)

    @classmethod
    def to_pki_request_string(cls, request):
        return RequestStringBuilder.create().append_super(
            super(CrossBookingFromSubMerchant, cls).to_pki_request_string(request)) \
            .append("subMerchantKey", request.get('sub_merchant_key', None)) \
            .append_price("price", request.get('price', None)) \
            .append("reason", request.get('reason', None)) \
            .get_request_string()