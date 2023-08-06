__all__ = ('ActionDescriptionPoint', 'NewUserActionPoint', 'FirstLoanActionPoint', 'CreateProfileActionPoint')

from expressmoney.api import *

SERVICE = 'partners'
APP = 'actions'


class ActionDescriptionReadContract(Contract):
    NEW_USER = 'NEW_USER'
    CREATE_PROFILE = 'CREATE_PROFILE'
    FIRST_LOAN = 'FIRST_LOAN'
    NAME_CHOICES = (
        (NEW_USER, NEW_USER),
        (CREATE_PROFILE, CREATE_PROFILE),
        (FIRST_LOAN, FIRST_LOAN),
    )
    RU = 'RU'
    __ = '-'
    COUNTRY_CHOICES = (
        (__, __),
        (RU, RU),
    )
    updated = serializers.DateTimeField()
    name = serializers.ChoiceField(choices=NAME_CHOICES)
    country = serializers.ChoiceField(choices=COUNTRY_CHOICES)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)


class NewUserActionCreateContract(Contract):
    pass


class NewUserActionReadContract(Contract):
    created = serializers.DateTimeField()
    is_approved = serializers.BooleanField()
    referral = serializers.IntegerField(min_value=1)
    amount = serializers.DecimalField(max_digits=16, decimal_places=0)
    balance = serializers.DecimalField(max_digits=16, decimal_places=0)
    total = serializers.IntegerField(min_value=1)


class FirstLoanActionCreateContract(Contract):
    pass


class FirstLoanActionReadContract(NewUserActionReadContract):
    pass


class CreateProfileActionCreateContract(Contract):
    pass


class CreateProfileActionReadContract(NewUserActionReadContract):
    pass


class ActionDescriptionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'action_description'


class NewUserActionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'new_user_action'


class FirstLoanActionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'first_loan_action'


class CreateProfileActionID(ID):
    _service = SERVICE
    _app = APP
    _view_set = 'create_profile_action'


class ActionDescriptionPoint(ListPointMixin, ContractPoint):
    _point_id = ActionDescriptionID()
    _read_contract = ActionDescriptionReadContract
    _sort_by = 'updated'


class NewUserActionPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = NewUserActionID()
    _create_contract = NewUserActionCreateContract
    _read_contract = NewUserActionReadContract
    _sort_by = 'created'


class FirstLoanActionPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = FirstLoanActionID()
    _create_contract = FirstLoanActionCreateContract
    _read_contract = FirstLoanActionReadContract
    _sort_by = 'created'


class CreateProfileActionPoint(ListPointMixin, CreatePointMixin, ContractPoint):
    _point_id = CreateProfileActionID()
    _create_contract = CreateProfileActionCreateContract
    _read_contract = CreateProfileActionReadContract
    _sort_by = 'created'
