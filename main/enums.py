MALE, FEMALE, OTHER = 'male', 'female', 'other'

GENDER = (
    (MALE, MALE),
    (FEMALE, FEMALE),
    (OTHER, OTHER)
)

# USER_TYPE = [
#     (False, 'Individual'),
#     (True, 'Agent'),
# ]


AGENT, CUSTOMER,  SUPER_ADMIN = (
    "agent",
    "customer",
    "super_admin",
)

USER_TYPE = (
    (AGENT, AGENT),
    (CUSTOMER, CUSTOMER),
    (SUPER_ADMIN, SUPER_ADMIN),
)
