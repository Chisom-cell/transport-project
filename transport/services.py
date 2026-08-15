from django.core.exceptions import ValidationError

def validate_trip_stops(
    trip,
    boarding_stop,
    destination_stop,
):
    
    """ 
    Validate that both stops belong to the trip's route and that the destination comes after the boarding stop.
    """
    
    boarding_route_stop = (
        trip.route.route_stops.filter(bus_stop=boarding_stop).first()
    )
    
    destination_route_stop = (
        trip.route.route_stops.filter(bus_stop=destination_stop).first()
    )
    
    if boarding_route_stop is None:
        raise ValidationError(
            "The boarding stop is not part of this route."
        )
        
    if destination_route_stop is None:
        raise ValidationError(
            "The destination stop is not part of this route."
        )
        
    if (
        boarding_route_stop.stop_order >= destination_route_stop.stop_order
    ):
        raise ValidationError(
            "The destination stop must come after the boarding stop."
        )
        
    return True 
    
    
    
    