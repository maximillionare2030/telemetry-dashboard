class BadQueryException(Exception):
    """ 
    Handle bad queries to InfluxDB
    """
    def __init__(self, message="Query to InfluxDB failed"):
        self.message = message
        super().__init__(self.message)