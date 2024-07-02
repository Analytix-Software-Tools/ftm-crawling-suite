from s3pipeline import S3Pipeline


class S3ExporterPipeline(S3Pipeline):

    """
    Custom S3 Exporter pipeline which will tag metadata for
    chunks.
    """

    def __init__(self, settings, stats):
        super().__init__(settings, stats)
