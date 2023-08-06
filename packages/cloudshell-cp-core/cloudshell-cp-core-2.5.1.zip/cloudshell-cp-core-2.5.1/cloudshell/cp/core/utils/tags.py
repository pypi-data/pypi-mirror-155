class BaseTagsManager:
    class DefaultTagNames:
        created_by = "CreatedBy"
        owner = "Owner"
        blueprint = "Blueprint"
        sandbox_id = "SandboxId"
        domain = "Domain"

    class DefaultTagValues:
        created_by = "CloudShell"
        blueprint_name_from_saved_reservation = "CloudShell Saved Sandbox"

    def __init__(self, reservation_info, resource_config):
        self._reservation_info = reservation_info
        self._resource_config = resource_config

    def get_default_tags(self):
        """Get pre-defined CloudShell tags."""
        bp_name = self._reservation_info.blueprint
        if not bp_name:
            # when restoring from saved sandbox blueprint name is empty
            bp_name = self.DefaultTagValues.blueprint_name_from_saved_reservation

        return {
            self.DefaultTagNames.created_by: self.DefaultTagValues.created_by,
            self.DefaultTagNames.owner: self._reservation_info.owner,
            self.DefaultTagNames.blueprint: bp_name,
            self.DefaultTagNames.sandbox_id: self._reservation_info.reservation_id,
            self.DefaultTagNames.domain: self._reservation_info.domain,
        }
