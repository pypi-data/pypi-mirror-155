from p360_export.exceptions.exporter import UnsetKeyException


class ExporterUtils:
    @staticmethod
    def get_custom_name(config: dict) -> str:
        persona_name = config.get("personas")[0].get("persona_name")
        persona_id = config.get("personas")[0].get("persona_id")
        return f"{persona_name}-{persona_id}"

    @staticmethod
    def check_user_variables(export_destination, keys):
        for key_name, key_value in keys.items():
            if not key_value:
                raise UnsetKeyException(f"p360.{export_destination}.{key_name} not set")
