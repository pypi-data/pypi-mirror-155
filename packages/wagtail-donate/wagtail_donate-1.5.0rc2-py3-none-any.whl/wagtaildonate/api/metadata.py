from rest_framework import metadata


class HiddenMetadata(metadata.BaseMetadata):
    def determine_metadata(self, request, view):
        return {}
