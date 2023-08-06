from datetime import datetime
from .dates import localize
from .init_creds import init_mongo
from .dates import today_argentina

db = init_mongo()


def member_unsubscribe(member, reason, unsubscribe_request=False):
    """ Da de baja un socio modificando los parámetros necesarios

       :param member: objeto de cliente a dar de baja
       :type receiver: dict
       :param reason: motivo de la baja
       :type template: str
       :param unsubscribe_request: es True si el cliente es 'baja' y puede seguir ingresando
       :type unsubscribe_request: bool, optional
       :return: None
       :rtype: None
       """

    history = {
        "subscription_date": member["last_subscription_date"],
        "unsubscribe_date": today_argentina(),
        "unsubscribe_reason": reason,
        "plan": member["active_plan_id"],
        "discounts": member["discounts"]
    }

    status = "inactivo" if not unsubscribe_request else "baja"

    db.clientes.update_one({"_id": member["_id"]},
                           {"$push": {"history": history}, "$set": {"next_payment_date": None, "status": status}})

    db.boletas.update_many({"member_id": member["_id"],
                                        "status": {"$in": ["error", "rejected"]}},
                                        {"$set": {"status": "expired"}})
