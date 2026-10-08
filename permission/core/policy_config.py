
from school.rules.permission_policy import policy_config


ACCESS_POLICY = {
    "user": {
        "admin": {
            "*": True
        },
        "staff": {
            "list": {"manager", "register"},
            "retrieve": {"manager", "register"},
            "create": {"manager",},
            "update": {"manager",},
            "partial_update": {"manager",}
            # "destroy": {"manager"},
        },
        "teacher": {
            "list": True,
            "retrieve": True, 
        },
        "student": {
            "retrieve": True,
        },
    },



    "profile": {
        "admin": {
            "*": True
        },

        "staff":{
            "list": {"manager", "register"},
            "retrieve": {"manager", "register"},
            "create": {"manager"},
            "update": {"manager"},
            "partial_update": {"manager"}
        },
        "teacher": {
            "list": True,
            "retrieve": True
        },
        "student": {
            "retrieve": True
        }

    },




    "audit": {
        "admin": {
            "list": True,
            "retrieve": True
        }
    },

    # school permission policy
    **policy_config,
    


}
