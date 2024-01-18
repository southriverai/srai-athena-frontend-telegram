from srai_athena_frontend_telegram.service_stabilityai import ServiceStabilityai

ServiceStabilityai.initialize()
ServiceStabilityai.get_instance().get_text_to_image("linedrawing of two lovers getting of the train")
