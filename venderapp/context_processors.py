def user_type_processor(request):
    user = request.user
    if user.is_authenticated:
        if hasattr(user, "multivendors"):
            user_type = 'vendor'
        elif hasattr(user, "registrationdetails"):
            user_type = 'customer'
        else:
            user_type = 'unknown'
    else:
        user_type = 'anonymous'
    
    return {'user_type': user_type}
