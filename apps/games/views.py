from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from decimal import Decimal
from .services import WheelService

@login_required
def wheel_page(request):
    # Initialize demo balance if not present
    if 'demo_balance' not in request.session:
        request.session['demo_balance'] = 1000
    return render(request, 'games/wheel.html')

@login_required
def spin_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)

    bet_str = request.POST.get('bet_amount')
    if not bet_str:
        return JsonResponse({'error': 'Bet amount is required'}, status=400)

    try:
        bet_amount = Decimal(bet_str)
    except:
        return JsonResponse({'error': 'Invalid bet amount format'}, status=400)

    # Check demo mode from session
    demo_mode = request.session.get('demo_mode', False)

    try:
        result = WheelService.spin(request.user, bet_amount, demo_mode=demo_mode, request=request)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def toggle_demo(request):
    # Toggle demo mode
    request.session['demo_mode'] = not request.session.get('demo_mode', False)
    # Reset demo balance if enabling demo
    if request.session['demo_mode']:
        request.session['demo_balance'] = 1000
    return redirect('games:wheel')
