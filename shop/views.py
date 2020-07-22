from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect, reverse
#from django.views.decorators.cache import cache_page
from django.contrib.auth.models import AnonymousUser
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import timezone

from django.views.generic import (
	TemplateView, ListView, 
	DetailView, UpdateView, View
)

#Address,
from .models import (
	Category,
    Product,
    OrderItem,
    Order,
    Payment,
    Refund,
)

from .forms import RefundForm
from users.models import UserProfile
from users.forms import ProfileForm


from .filter import ProductFilter

import random
import string
import stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


def create_ref_code():
	return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))

def is_valid_form(values):
	valid = True
	for field in values:
		if field == '':
			valid = False
	return valid

def consulta(id):
	try:
		return Product.objects.get(id=id)
	except:
		return None




def AdminOrderDetail(request, order_id):
	order = get_object_or_404(Order, id=order_id)
	user_id = order.user_id
	user_info = UserProfile.objects.get(user_id=user_id)
	return render(request,
		'admin/order_detail.html',
		{'order': order,
		'user_info': user_info,})



#@staff_member_required
# class AdminOrderDetail(View):
	
# 	def get(self, *args, **kwargs):
# 		#order = Order.objects.get(user=self.request.user, ordered=False)
# 		order = get_object_or_404(Order, id=order_id)
		
# 		user_id = order.user_id
# 		user_info = UserProfile.objects.get(user_id=user_id)
# 		context = {
# 			'order': order,
# 			'user_info': user_info,

# 		}
# 		return render(self.request, 'admin/order_detail.html', context)


class HomePageView(ListView):
	model = Product
	template_name = 'shop/index.html'
	context_object_name = 'products'

	def get_context_data(self, **kwargs):
		categories = Category.objects.all().order_by('id')[:3]
		featured = Product.objects.filter(featured=True,)[:7]
		try:
			profile = UserProfile.objects.get_or_create(user=self.request.user)
		except:
			profile = None

		context = super().get_context_data(**kwargs)
		context['categories'] = categories
		context['featured'] = featured
		context['profile'] = profile
		return context


class ProfilePageView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	model = UserProfile
	success_url = reverse_lazy('shop:home')
	form_class = ProfileForm
	success_message = "Profile updated successfully"
	template_name = 'account/profile.html'


	def get_queryset(self):
		queryset = UserProfile.objects.filter(user=self.request.user)
		return queryset

	def dispatch(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj.user != self.request.user:
			raise PermissionDenied
		return super().dispatch(request, *args, **kwargs)

	# def form_valid(self, form):
	# 	form.instance.user = self.request.user
	# 	return super().form_valid(form)

	def get_context_data(self, *args, **kwargs):
		form = ProfileForm()
		context = super().get_context_data(**kwargs)

		try:
			same_address_billing = UserProfile.objects.filter(
				user=self.request.user,
				same_address_billing=True
			)

			if same_address_billing.exists():
				context.update(
					{'same_address_for_billing': same_address_billing[0],})
	
			else:
				same_address_billing = UserProfile.objects.filter(
					user=self.request.user,
					same_address_billing=False
				)
				context.update(
					{'same_address_for_billing': same_address_billing[0]})
			
			return context		
		except ObjectDoesNotExist:
			messages.error(self.request, "Something else happened")
			return redirect("shop:home")

		
class CategoryListView(FilterView):
	template_name = 'shop/category.html'
	paginate_by = 10

	def get(self, request, slug, *args, **kwargs):
		f = ProductFilter(request.GET, queryset=Product.objects.filter(category__slug=slug))
		context = {
			'filter': f
		}
		return render(request, 'shop/category.html', context)


class ProductListView(FilterView):
	filterset_class = ProductFilter
	template_name = 'shop/shop.html'
	paginate_by = 10


class ServicesPageView(TemplateView):
	template_name = "shop/services.html"


class ProductDetailView(DetailView):
	model = Product
	template_name = 'shop/shop-single.html'

	def get_context_data(self, **kwargs):
		featured = Product.objects.filter(featured=True,)[:7]
		context = super().get_context_data(**kwargs)
		context['featured'] = featured
		return context


class PaymentView(View):
	def get(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False) # Para dar dinamismo, ver min:2:35:41 // https://www.youtube.com/watch?v=YZvRrldjf1Y&t=9279s

			
		context = {
			'order': order 
		}
		return render(self.request, 'shop/payment.html', context)

	def post(self, *args, **kwargs):
		order = Order.objects.get(user=self.request.user, ordered=False)
		token = self.request.POST.get('stripeToken')
		amount = int(order.get_total() * 100)

		try:
			# Use Stripe's library to make requests...
			charge = stripe.Charge.create(
				amount=amount,
				currency="usd",
				source=token
			)

			# Create the payment
			payment = Payment()
			payment.stripe_charge_id = charge['id']
			payment.user = self.request.user
			payment.amount = order.get_total()
			payment.save()


			# Assign the paymet to the order
			order_items = order.items.all()
			order_items.update(ordered=True)
			for item in order_items:
				item.save()

			order.ordered = True
			order.payment = payment
			# TODO: reference Code
			order.ref_code = create_ref_code()
			order.save()

			messages.success(self.request, "Your order was successful!")
			return redirect("/")

		except stripe.error.CardError as e:
			# Since it's a decline, stripe.error.CardError will be caught
			body = e.json_body
			err = body.get('error', {})
			messages.error(self.request, f"{err.get('message')}")
			return redirect("/")
  
		except stripe.error.RateLimitError as e:            
			# Too many requests made to the API too quickly         
			messages.error(self.request, 'Rate limit error')            
			return redirect("/")

		except stripe.error.InvalidRequestError as e:
			# Invalid parameters were supplied to Stripe's API           
			print(e)
			messages.error(self.request, 'Invalid parameters')
			return redirect("/")

		except stripe.error.AuthenticationError as e:
			# Authentication with Stripe's API failed
			# (maybe you changed API keys recently)
			messages.error(self.request, 'Not authenticated')
			return redirect("/")

		except stripe.error.APIConnectionError as e:
			# Network communication with Stripe failed
			#print(e)
			messages.error(self.request, 'Network error')
			return redirect("/")

		except stripe.error.StripeError as e:
			# Display a very generic error to the user, and maybe send
			# yourself an email
			messages.error(self.request, 'Something  try againwent wrong. You were not charget. Please')
			return redirect("/")

		except Exception as e:
			# Something else happened, completely unrelated to Stripe
			#print(e)
			messages.error(self.request, 'A serius error accourred. We have been notified')
			return redirect("/")


class CheckoutView(View):

	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			form = ProfileForm()
			context = {
				'form': form,
				'order': order,
			}

			user_profile_address = UserProfile.objects.get(user=self.request.user)

			if user_profile_address.shipping_address == None:
				user_profile_address = False

			if user_profile_address:
				context.update(
					{'user_profile_address': user_profile_address}
				)
			else:
				context.update(
					{'form': form}
				)

			return render(self.request, "shop/checkout.html", context)
		except ObjectDoesNotExist:
			messages.info(self.request, "You do not have an active order")
			return redirect("shop:cart")
		

	def post(self, *args, **kwargs):
		form = ProfileForm(self.request.POST or None)

		try:
			order = Order.objects.get(user=self.request.user, ordered=False)
			user_profile_address = UserProfile.objects.get(user=self.request.user)

			if user_profile_address.shipping_address == None:
				user_profile_address = False

			if form.is_valid():
				order_items = order.items.all()

				if user_profile_address and len(order_items) != 0:
					# If user have address info in his profile
					print('User will be used their profile info')
					order.shipping_billing_info = user_profile_address
					order.user_billing_same_shipping = user_profile_address.same_address_billing
					order.save()

					payment_option = form.cleaned_data.get('payment_option')
					# if payment_option == 'S':
					# 	return redirect('shop:payment', payment_option='stripe')
					# elif payment_option == 'P':
					# 	return redirect('shop:payment', payment_option='paypal')
					# else:
					# 	messages.warning(self.request, "Invalid payment option selected")
					# 	return redirect('shop:checkout')
				elif user_profile_address and len(order_items) == 0:
					messages.warning(self.request, "You do not have an active order")
					return redirect("shop:cart")


				else:
					print("User is entering a new shipping address")
					shipping_address = form.cleaned_data.get(
						'shipping_address')
					shipping_address2 = form.cleaned_data.get(
						'shipping_address2')
					shipping_country = form.cleaned_data.get(
						'shipping_country')
					shipping_zip = form.cleaned_data.get(
						'shipping_zip')

					if is_valid_form([shipping_address, shipping_country, shipping_zip,]):
						shipping_billing_info = UserProfile.objects.get(user=self.request.user)
						shipping_billing_info.shipping_address = shipping_address
						shipping_billing_info.shipping_address2 = shipping_address2
						shipping_billing_info.shipping_country = shipping_country
						shipping_billing_info.shipping_zip = shipping_zip
						#shipping_billing_info.save() 

						order.shipping_billing_info = shipping_billing_info
						order.save()

					else:
						messages.info(
							self.request, "Please fill in the required shipping address fields")
						return redirect('shop:checkout')


				same_billing_address = form.cleaned_data.get(
							'same_billing_address')
				set_default_shipping = form.cleaned_data.get(
							'set_default_shipping')

				if set_default_shipping:
					user_profile_address = UserProfile.objects.get(user=self.request.user)
					user_profile_address.shipping_address = shipping_address
					user_profile_address.shipping_address2 = shipping_address2
					user_profile_address.shipping_country = shipping_country
					user_profile_address.shipping_zip = shipping_zip
					user_profile_address.save()
				
				if same_billing_address:
					shipping_billing_info = UserProfile.objects.get(user=self.request.user)
					shipping_billing_info.billing_address = shipping_billing_info.shipping_address
					shipping_billing_info.billing_address2 = shipping_billing_info.shipping_address2
					shipping_billing_info.billing_country = shipping_billing_info.shipping_country
					shipping_billing_info.billing_zip = shipping_billing_info.shipping_zip
					shipping_billing_info.save()

				else:
					billing_address = form.cleaned_data.get(
						'billing_address')
					billing_address2 = form.cleaned_data.get(
						'billing_address2')
					billing_country = form.cleaned_data.get(
						'billing_country')
					billing_zip = form.cleaned_data.get(
						'billing_zip')

					if is_valid_form([billing_address, billing_country, billing_zip,]):
						shipping_billing_info = UserProfile.objects.get(user=self.request.user)
						shipping_billing_info.billing_address = billing_address
						shipping_billing_info.billing_address2 = billing_address2
						shipping_billing_info.billing_country = billing_country
						shipping_billing_info.billing_zip = billing_zip
						#shipping_billing_info.save()

						order.shipping_billing_info = shipping_billing_info
						order.save()

						set_default_billing = form.cleaned_data.get(
							'set_default_billing')
						if set_default_billing:
							user_profile_address = UserProfile.objects.get(user=self.request.user)
							user_profile_address.billing_address = billing_address
							user_profile_address.billing_address2 = billing_address2
							user_profile_address.billing_country = billing_country
							user_profile_address.billing_zip = billing_zip
							user_profile_address.save()

					else:
						messages.info(
							self.request, "Please fill in the required shipping address fields")
						#return redirect('shop:checkout')


				payment_option = form.cleaned_data.get('payment_option')

				if payment_option == 'S':
					return redirect('shop:payment', payment_option='stripe')
				elif payment_option == 'P':
					return redirect('shop:payment', payment_option='paypal')
				else:
					messages.warning(self.request, "Invalid payment option selected")
					return redirect('shop:checkout')

		except ObjectDoesNotExist:
			messages.warning(self.request, "You do not have an active order")
			return redirect("shop:cart")


class CartPageView(LoginRequiredMixin, View):
	def get(self, *args, **kwargs):
		try:
			order = Order.objects.get(user=self.request.user, ordered=False)

			context = {

				'object': order,

			}
			return render(self.request, 'shop/cart.html', context)
		except ObjectDoesNotExist:
			messages.error(self.request, "You do not have an active order")
			return redirect("/")


class RequestRefundView(View):
	def get(self, *args, **kwargs):
		form = RefundForm()
		context = {
			'form': form
		}
		return render(self.request, "shop/request_refund.html", context)


	def post(self, *args, **kwargs):
		form = RefundForm(self.request.POST)
		if form.is_valid():
			ref_code = form.cleaned_data.get('ref_code')
			message = form.cleaned_data.get('message')
			email = form.cleaned_data.get('email')
			# edit the order
			try:
				order = Order.objects.get(ref_code=ref_code)
				order.refund_request = True
				order.save()

				# store the refund
				refund = Refund()
				refund.order = order
				refund.reason = message
				refund.email = email
				refund.save()

				messages.info(self.request, "Your request was received.")
				return redirect("shop:request-refund")

			except ObjectDoesNotExist:
				messages.info(self.request, "This order does not exist.")
				return redirect("shop:request-refund")



def Erro404View(request, exception):
	return render(request, 'shop/404.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:cart")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:cart")


@login_required
def remove_from_cart(request, slug):
	item = get_object_or_404(Product, slug=slug)

	order_qs = Order.objects.filter(
		user=request.user, 
		ordered=False
	)


	if order_qs.exists():
		order = order_qs[0]
		# Check if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
				item=item,
				user=request.user,
				ordered=False,
			)[0]


			order.items.remove(order_item)
			order_item.delete()
			messages.info(request, "This item was removed from your cart.")
			return redirect("shop:cart")
		else:
			messages.info(request, "This item not in your cart.")
			return redirect("shop:produtc-detail", slug=slug)
	else:
		messages.info(request, "You do not have an activate order.")
		return redirect("shop:produtc-detail", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
	item = get_object_or_404(Product, slug=slug)

	order_qs = Order.objects.filter(
			user=request.user, 
			ordered=False
	)


	if order_qs.exists():
		order = order_qs[0]
		# Check if the order item is in the order
		if order.items.filter(item__slug=item.slug).exists():
			order_item = OrderItem.objects.filter(
											item=item,
											user=request.user,
											ordered=False
			)[0]

			if order_item.quantity > 1:
				order_item.quantity -= 1
				order_item.save()
			else:
				 order.items.remove(order_item)
			messages.info(request, "This item quantity was updated from your cart.")
			return redirect("shop:cart")
		else:
			messages.info(request, "This item not in your cart.")
			return redirect("shop:produtc-detail", slug=slug)
	else:
		messages.info(request, "You do not have an activate order.")
		return redirect("shop:produtc-detail", slug=slug)

