import json

def get_google_places_query(trip_data: dict) -> dict:
    """
    Transforms collected trip data into a structured query for the Google Places API.

    This function takes a dictionary of trip planning details (as collected by a chatbot)
    and constructs a more specific query string suitable for searching points of interest
    using the Google Places API.

    Args:
        trip_data (dict): A dictionary containing comprehensive trip details,
                          expected to have keys like:
                          - "destination" (str)
                          - "interests" (list of str)
                          - "budget" (str)
                          - "dietary_needs" (str)
                          - "accessibility_needs" (str)
                          - "age_group_of_travelers" (str)
                          - "how_packed_trip" (str)
                          - "ok_with_walking" (bool)
                          - "trip_type" (str)

    Returns:
        dict: A dictionary representing the structured query for Google Places API.
              It will primarily contain a 'query' string, and can be extended
              with 'locationBias', 'rankPreference', etc., if needed for more
              advanced API calls.

    Example Places API query structure (simplified):
    {
        "query": "restaurants in Paris with vegan options, budget-friendly, family-friendly",
        "fields": ["displayName", "formattedAddress", "editorialSummary", "photos", "rating", "types"]
    }
    """

    # Extract relevant information from the trip_data
    destination = trip_data.get("destination", "").strip()
    interests = trip_data.get("interests", [])
    budget = trip_data.get("budget", "").strip()
    dietary_needs = trip_data.get("dietary_needs", "").strip()
    accessibility_needs = trip_data.get("accessibility_needs", "").strip()
    age_group = trip_data.get("age_group_of_travelers", "").strip()
    how_packed_trip = trip_data.get("how_packed_trip", "").strip()
    ok_with_walking = trip_data.get("ok_with_walking", None)
    trip_type = trip_data.get("trip_type", "").strip()

    # Build the primary query string
    query_parts = []

    if destination:
        query_parts.append(f"things to do in {destination}")
    else:
        # If no destination, a general query might not be very useful for Places API.
        # This scenario should ideally be prevented by the chatbot ensuring a destination.
        query_parts.append("places of interest")

    # Add interests
    if interests:
        query_parts.append(f"interested in: {', '.join(interests)}")

    # Add budget considerations
    if budget:
        if "low" in budget.lower() or "cheap" in budget.lower():
            query_parts.append("budget-friendly")
        elif "luxury" in budget.lower() or "high" in budget.lower():
            query_parts.append("luxury options")

    # Add dietary needs
    if dietary_needs:
        query_parts.append(f"with {dietary_needs} options")

    # Add accessibility needs
    if accessibility_needs:
        query_parts.append(f"{accessibility_needs} friendly")

    # Add age group considerations
    if age_group:
        if "family" in age_group.lower() or "children" in age_group.lower():
            query_parts.append("family-friendly")
        elif "adults" in age_group.lower() or "seniors" in age_group.lower():
            query_parts.append("suitable for adults/seniors")
        elif "young" in age_group.lower() or "solo" in age_group.lower():
            query_parts.append("good for young adults/solo travelers")


    # Add trip pace
    if how_packed_trip:
        if "relaxed" in how_packed_trip.lower() or "leisurely" in how_packed_trip.lower():
            query_parts.append("relaxed pace activities")
        elif "packed" in how_packed_trip.lower() or "fast" in how_packed_trip.lower():
            query_parts.append("efficient itinerary")

    # Add walking preference
    if ok_with_walking is False:
        query_parts.append("minimal walking required")

    # Add trip type
    if trip_type:
        query_parts.append(f"for a {trip_type} trip")


    # Construct the final query string
    final_query_string = ", ".join(filter(None, query_parts)) # Filter out empty strings

    # Define the fields to retrieve from Places API for a comprehensive result
    # These are common and useful fields. You can adjust based on specific needs.
    places_api_fields = [
        "displayName",           # The localized display name for the place.
        "formattedAddress",      # The human-readable address of the place.
        "editorialSummary",      # A summary of the place.
        "photos",                # Photos of the place.
        "rating",                # The overall rating, based on user reviews.
        "userRatingCount",       # The total number of ratings for the place.
        "types",                 # A list of types for the place (e.g., restaurant, museum).
        "websiteUri",            # The business's primary website.
        "internationalPhoneNumber", # The international phone number of the place.
        "priceLevel",            # The price level of the place.
        "businessStatus",        # The operational status of the place.
        "plusCode",              # A plus code for the place.
        "currentOpeningHours",   # Current opening hours.
        "accessibilityOptions",  # Accessibility options.
        "reservable",            # Whether the place is reservable.
        "servesCuisine",         # What cuisines the restaurant serves (for dining places).
        "attributions"           # Required attributions for the place data.
    ]

    # Construct the structured output for Google Places API
    structured_query = {
        "query": final_query_string,
        "fields": places_api_fields
        # locationBias can be added here if 'starting_location' is geocoded
        # For example:
        # "locationBias": {
        #     "circle": {
        #         "center": {"latitude": 34.052235, "longitude": -118.243683},
        #         "radius": 50000.0
        #     }
        # }
        # You might also add 'rankPreference' like 'DISTANCE' if a locationBias is provided
    }

    return structured_query