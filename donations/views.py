from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from .forms import MakePaymentForm, OrderForm
import stripe

stripe.api_key = settings.STRIPE_SECRET

@login_required()
def donations(request):
    if request.method=="POST":
        order_form = OrderForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if order_form.is_valid() and payment_form.is_valid():
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            try:
                customer = stripe.Charge.create(
                    amount = 500, 
                    currency = "EUR",
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'],
                    )
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "You have successfully paid")
                return redirect("/")
            else:
                messages.error(request, "Unable to take payment")
        else: 
            print(payment_form.errors)
            messages.error(request, "We were unable to take a payment with that card!")
    else:
        order_form = OrderForm()
        payment_form = MakePaymentForm()

        return render(request, "donations/donations.html", {"order_form" : order_form, "payment_form" : payment_form, "publishable" : settings.STRIPE_PUBLISHABLE})