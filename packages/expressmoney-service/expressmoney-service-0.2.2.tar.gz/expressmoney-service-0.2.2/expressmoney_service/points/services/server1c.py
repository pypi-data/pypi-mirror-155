__all__ = ('NoLoanPoint',)

from expressmoney_service.api import *

_SERVICE = 'services'
_APP = 'server1c'


class _NoLoanCreateContract(Contract):
    passport_serial = serializers.CharField(max_length=4)
    passport_number = serializers.CharField(max_length=6)


class _NoLoanResponseContract(Contract):
    is_no_loan = serializers.BooleanField()


class _NoLoanID(ID):
    _service = _SERVICE
    _app = _APP
    _view_set = 'no_loan'


class NoLoanPoint(ResponseMixin, CreatePointMixin, ContractPoint):
    _point_id = _NoLoanID()
    _create_contract = _NoLoanCreateContract
    _response_contract = _NoLoanResponseContract
