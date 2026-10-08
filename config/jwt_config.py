from datetime import timedelta
from decouple import config

# create your JWT config hare


SIMPLE_JWT = {
    # jwt config
    **{
        "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15), # max_time = 15mn
        "REFRESH_TOKEN_LIFETIME": timedelta(days=7), # max_time = 7day
        "USER_ID_FIELD": "uuid", # user ke jokhon akta token deya hobe tokhon user ke ki vabe cinbe ata akta user , karon shobar tohh kono na kono unique name lagbe , tai uuid diye protita user ke alada alada kore cinbe
        "USER_ID_CLAIM": "user_id", # karon ami je user ar jonno backend a uuid use korsi seta tohh r fontend a deya jaina , tai akta shoddobeshi name 
        "BLACKLIST_AFTER_ROTATION": True,
    },
    
    # cookie config
    **{
        "AUTH_COOKIE_PATH": "/", 
        "AUTH_COOKIE": "access_token",
        "AUTH_COOKIE_REFRESH": "refresh_token",
        "AUTH_COOKIE_HTTP_ONLY": True,
        "AUTH_COOKIE_SAMESITE": "Lax",
        # "AUTH_COOKIE_SECURE": True,
    },
    
    # update with password change validation
    **{
        "CHECK_REVOKE_TOKEN": True,
        "REVOKE_TOKEN_CLAIM": "pw_hash",
    },
}




# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(config("JWT_ACCESS_TOKEN_LIFETIME"))), # max_time = 15mn
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=int(config("JWT_REFRESH_TOKEN_LIFETIME"))), # max_time = 7day
#     "USER_ID_FIELD": "uuid", # user ke jokhon akta token deya hobe tokhon user ke ki vabe cinbe ata akta user , karon shobar tohh kono na kono unique name lagbe , tai uuid diye protita user ke alada alada kore cinbe
#     "USER_ID_CLAIM" : "user_id", # karon ami je user ar jonno backend a uuid use korsi seta tohh r fontend a deya jaina , tai akta shoddobeshi name 
#     "BLACKLIST_AFTER_ROTATION": True,
    
#     # configure jwt token 
#     "AUTH_COOKIE_PATH": "/", # "/" ar mane holo jekono link ba route ar sathe cookie jabe jodi "/home" kortam tahole shudhu matro /home a user click kore cookie backend a ashto , onno kono link a click korle astona :) tai / root a rakhai bhalo 
#     "AUTH_COOKIE": "access_token",
#     "AUTH_COOKIE_REFRESH": "refresh_token",
#     "AUTH_COOKIE_HTTP_ONLY": True,
#     "AUTH_COOKIE_SAMESITE" : "Lax",
#     # "AUTH_COOKIE_SECURE": True, # shudhu matro https ar khetre kajj korbe 
# }


# # add password change validation
# SIMPLE_JWT.update({
#     "CHECK_REVOKE_TOKEN": True,   #  এইটা enable করতেই হবে
#     "REVOKE_TOKEN_CLAIM": "pw_hash",  # claim name (default এটিই)
# })
