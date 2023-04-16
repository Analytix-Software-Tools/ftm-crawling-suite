from scrapy.exceptions import DropItem


class ValidateProductFields:

    def process_item(self, item, spider):
        """
        Ensure all fields are present in an item.
        """
        for field in item:
            if field is None:
                raise DropItem(f"Error: field {field} cannot be None.")
            elif field == 'attributeValues' and not isinstance(field, list) or len(field) == 0:
                raise DropItem(f"Field 'attributeValues' must be a list of length >= 1! Dropping item...")
            if field == 'attributeValues':
                for attribute_value in field:
                    if not attribute_value['attributePid'] or not attribute_value['attributeValue']:
                        raise DropItem(f"Invalid attributeValue! Dropping item.")
