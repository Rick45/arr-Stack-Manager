import constants
# Create a dictionary to store the media status

#Availability of the media. 1 = UNKNOWN, 2 = PENDING, 3 = PROCESSING, 4 = PARTIALLY_AVAILABLE, 5 = AVAILABLE
#Status of the request. 1 = PENDING APPROVAL, 2 = APPROVED, 3 = DECLINED
mediaAvailability = {
    1: "UNKNOWN",
    2: "PENDING",
    3: "PROCESSING",
    4: "PARTIALLY_AVAILABLE",
    5: "AVAILABLE"
}

requestsStatus = {
    1: "PENDING APPROVAL",
    2: "APPROVED",
    3: "DECLINED"
}
