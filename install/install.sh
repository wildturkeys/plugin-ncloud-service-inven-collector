spacectl exec register repo -p name=Private -p repository_type=local
spacectl exec create repository.Schema -f ncloud_schema.yaml
spacectl exec create provider -f ncloud_provider.yaml
spacectl exec register repository.Plugin -f ncloud_inventory_plugin.yaml