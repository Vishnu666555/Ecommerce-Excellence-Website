from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-this-in-production'

# Products from suppliers with categories
products = [
    # Electronics Category
    {
        "id": 1,
        "name": "Wireless Earbuds Pro",
        "description": "High-quality wireless earbuds with noise cancellation. 20hrs battery life, fast charging, IPX4 water resistant.",
        "price": 1899,
        "supplier_price": 1200,
        "profit": 699,
        "image": "https://images.unsplash.com/photo-1590658165737-15a047b8b5e6?w=400",
        "category": "Electronics",
        "category_slug": "electronics",
        "supplier_name": "Tech Distributors Pvt Ltd",
        "supplier_phone": "+91 98765 43210",
        "supplier_email": "orders@techdistributors.com",
        "stock": 50,
        "featured": True
    },
    {
        "id": 5,
        "name": "Smart Fitness Tracker",
        "description": "Track heart rate, steps, sleep with smartphone sync. Water resistant, 7-day battery life.",
        "price": 2799,
        "supplier_price": 1800,
        "profit": 999,
        "image": "https://images.unsplash.com/photo-1576243345690-4e4b79b63288?w=400",
        "category": "Electronics",
        "category_slug": "electronics",
        "supplier_name": "Gadget World",
        "supplier_phone": "+91 98765 43214",
        "supplier_email": "orders@gadgetworld.com",
        "stock": 40,
        "featured": True
    },
    {
        "id": 7,
        "name": "Bluetooth Speaker",
        "description": "Portable wireless speaker with 360° sound, 12hrs playtime, waterproof.",
        "price": 2499,
        "supplier_price": 1600,
        "profit": 899,
        "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400",
        "category": "Electronics",
        "category_slug": "electronics",
        "supplier_name": "Audio Technologies",
        "supplier_phone": "+91 98765 43220",
        "supplier_email": "orders@audiotech.com",
        "stock": 35,
        "featured": False
    },

    # Groceries Category
    {
        "id": 2,
        "name": "Premium Kerala Spices Set",
        "description": "Authentic Kerala spice box with 6 organic spices including cardamom, pepper, cinnamon, cloves, nutmeg, and turmeric.",
        "price": 849,
        "supplier_price": 500,
        "profit": 349,
        "image": "https://images.unsplash.com/photo-1563636619-e9143da7973b?w=400",
        "category": "Groceries",
        "category_slug": "groceries",
        "supplier_name": "Kerala Spice Exports",
        "supplier_phone": "+91 98765 43211",
        "supplier_email": "orders@keralaspice.com",
        "stock": 100,
        "featured": True
    },
    {
        "id": 6,
        "name": "Organic Coconut Oil",
        "description": "Cold-pressed virgin coconut oil, 1 liter. Pure, natural, and chemical-free.",
        "price": 450,
        "supplier_price": 280,
        "profit": 170,
        "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400",
        "category": "Groceries",
        "category_slug": "groceries",
        "supplier_name": "Kerala Farmers Co-op",
        "supplier_phone": "+91 98765 43215",
        "supplier_email": "orders@keralafarmers.com",
        "stock": 200,
        "featured": True
    },
    {
        "id": 8,
        "name": "Organic Honey Jar",
        "description": "Pure, unprocessed organic honey from Western Ghats, 500g.",
        "price": 599,
        "supplier_price": 350,
        "profit": 249,
        "image": "https://images.unsplash.com/photo-1587049352846-4a222e784d38?w=400",
        "category": "Groceries",
        "category_slug": "groceries",
        "supplier_name": "Natural Farms",
        "supplier_phone": "+91 98765 43221",
        "supplier_email": "orders@naturalfarms.com",
        "stock": 150,
        "featured": False
    },

    # Fashion Category
    {
        "id": 3,
        "name": "Handloom Cotton Saree",
        "description": "Traditional Kerala handloom saree with golden border. Pure cotton, comfortable and elegant. Includes blouse piece.",
        "price": 3499,
        "supplier_price": 2200,
        "profit": 1299,
        "image": "https://images.unsplash.com/photo-1583391721169-ca5c72cb3ab4?w=400",
        "category": "Fashion",
        "category_slug": "fashion",
        "supplier_name": "Weavers Village Collective",
        "supplier_phone": "+91 98765 43212",
        "supplier_email": "orders@weaversvillage.com",
        "stock": 30,
        "featured": True
    },
    {
        "id": 9,
        "name": "Men's Casual Shirt",
        "description": "Premium cotton casual shirt, regular fit, available in multiple colors.",
        "price": 1299,
        "supplier_price": 800,
        "profit": 499,
        "image": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=400",
        "category": "Fashion",
        "category_slug": "fashion",
        "supplier_name": "Fashion Hub",
        "supplier_phone": "+91 98765 43222",
        "supplier_email": "orders@fashionhub.com",
        "stock": 60,
        "featured": False
    },
    {
        "id": 10,
        "name": "Women's Kurti Set",
        "description": "Cotton blend kurti with palazzo and dupatta, ethnic wear.",
        "price": 1899,
        "supplier_price": 1200,
        "profit": 699,
        "image": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400",
        "category": "Fashion",
        "category_slug": "fashion",
        "supplier_name": "Ethnic Collection",
        "supplier_phone": "+91 98765 43223",
        "supplier_email": "orders@ethniccollection.com",
        "stock": 45,
        "featured": False
    },

    # Wellness Category
    {
        "id": 4,
        "name": "Ayurvedic Wellness Kit",
        "description": "Complete Ayurvedic kit with oils, soaps, and supplements for overall wellness. Includes 5 products.",
        "price": 1999,
        "supplier_price": 1300,
        "profit": 699,
        "image": "https://images.unsplash.com/photo-1559056199-641a0ac8b55e?w=400",
        "category": "Wellness",
        "category_slug": "wellness",
        "supplier_name": "Kerala Ayurveda Ltd",
        "supplier_phone": "+91 98765 43213",
        "supplier_email": "orders@ayurveda.com",
        "stock": 75,
        "featured": True
    },
    {
        "id": 11,
        "name": "Yoga Mat Set",
        "description": "Eco-friendly yoga mat with carry bag and strap. Non-slip surface.",
        "price": 899,
        "supplier_price": 550,
        "profit": 349,
        "image": "https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=400",
        "category": "Wellness",
        "category_slug": "wellness",
        "supplier_name": "Wellness Store",
        "supplier_phone": "+91 98765 43224",
        "supplier_email": "orders@wellnessstore.com",
        "stock": 80,
        "featured": False
    },

    # Household Items Category
    {
        "id": 12,
        "name": "Stainless Steel Cookware Set",
        "description": "5-piece stainless steel cookware set including pans and utensils.",
        "price": 2999,
        "supplier_price": 2000,
        "profit": 999,
        "image": "https://images.unsplash.com/photo-1584990347449-a5d2f4d4b9e4?w=400",
        "category": "Household",
        "category_slug": "household",
        "supplier_name": "Home Essentials",
        "supplier_phone": "+91 98765 43225",
        "supplier_email": "orders@homeessentials.com",
        "stock": 40,
        "featured": True
    },
    {
        "id": 13,
        "name": "Bedsheet Set",
        "description": "Cotton bedsheet set with 2 pillow covers, king size, multiple designs.",
        "price": 1499,
        "supplier_price": 900,
        "profit": 599,
        "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=400",
        "category": "Household",
        "category_slug": "household",
        "supplier_name": "Home Decor",
        "supplier_phone": "+91 98765 43226",
        "supplier_email": "orders@homedecor.com",
        "stock": 55,
        "featured": False
    }
]

# Services for B2B clients - UPDATED WITH DETAILED DESCRIPTIONS FOR EACH SERVICE PAGE
services = [
    {
        "id": 1,
        "icon": "fa-solid fa-pen-to-square",
        "title": "Bulk Data Entry",
        "short_desc": "High-volume product data entry with 99.9% accuracy",
        "description": "Our bulk data entry service handles thousands of products with precision. We specialize in processing complex product information, specifications, pricing, and inventory data into any ecommerce platform.",
        "full_description": "Our Bulk Data Entry service is designed for businesses looking to scale their product catalog quickly and accurately. We handle large volumes of product data with meticulous attention to detail. Our process includes data cleaning, formatting, validation, and upload. Whether you have 100 or 100,000 products, our team ensures error-free data entry with quick turnaround times. We work with all major ecommerce platforms including Shopify, WooCommerce, Magento, and custom databases. Our dedicated team of data entry specialists ensures your product catalog is accurate, consistent, and ready for sale. We provide regular quality reports and maintain 99.9% accuracy across all projects.",
        "features": [
            "High-volume data processing (up to 10,000 products/week)",
            "99.9% accuracy guarantee",
            "Multi-format support (Excel, CSV, XML, JSON)",
            "Image processing and optimization",
            "Price and inventory synchronization",
            "Category mapping and organization",
            "Bulk updates and modifications",
            "Quality checks at every stage"
        ],
        "benefits": [
            "Save up to 70% on operational costs",
            "Reduce errors with professional data entry",
            "Faster time-to-market for your products",
            "Scalable solutions that grow with your business",
            "Dedicated account manager for your project"
        ],
        "process": [
            "Data audit and validation",
            "Format standardization",
            "Data cleaning and deduplication",
            "Platform-specific formatting",
            "Multi-level quality checks",
            "Final upload and verification"
        ],
        "price_starting": "₹15,000/month",
        "turnaround": "24-48 hours",
        "team_size": "Dedicated team of 5-10 specialists",
        "free_trial": "3 days",
        "ideal_for": "Ecommerce stores, Marketplaces, Dropshippers, Manufacturers",
        "faq": [
            {
                "question": "What types of data can you handle?",
                "answer": "We handle all types of product data including descriptions, specifications, pricing, inventory levels, images, and variations. We support Excel, CSV, XML, JSON, and many other formats."
            },
            {
                "question": "How do you ensure data accuracy?",
                "answer": "We have a multi-level quality check process. Each entry is verified by at least two team members before final approval. Our accuracy rate is consistently above 99.9%."
            },
            {
                "question": "What is your turnaround time?",
                "answer": "For standard projects, we deliver within 24-48 hours. For large volumes (10,000+ products), we provide a detailed timeline based on your specific requirements."
            }
        ]
    },
    {
        "id": 2,
        "icon": "fa-solid fa-cart-shopping",
        "title": "Ecommerce Services",
        "short_desc": "Complete ecommerce management and optimization",
        "description": "End-to-end ecommerce services including catalog management, marketplace integration, inventory synchronization, and order processing.",
        "full_description": "Our comprehensive Ecommerce Services cover every aspect of your online store operations. From setting up your product catalog on multiple marketplaces to managing inventory across platforms, we ensure your ecommerce business runs smoothly. Our team of experts handles marketplace integration (Amazon, Flipkart, eBay, etc.), product listing optimization, inventory synchronization, and order processing. We also provide regular performance reports and insights to help you make data-driven decisions. Our services include competitive analysis, price monitoring, and seasonal campaign management to help you stay ahead of the competition. With our 24/7 support and dedicated account managers, your ecommerce operations are in safe hands.",
        "features": [
            "Multi-platform integration (Amazon, Flipkart, eBay, etc.)",
            "Inventory synchronization across all channels",
            "Automated order processing",
            "Product listing optimization",
            "Price monitoring and adjustments",
            "Competitor analysis",
            "Performance analytics and reporting",
            "Seasonal campaign management"
        ],
        "benefits": [
            "Manage all platforms from one dashboard",
            "Never oversell with real-time inventory sync",
            "Increase sales with optimized listings",
            "Save time with automated order processing",
            "Make data-driven decisions with analytics"
        ],
        "process": [
            "Platform audit and analysis",
            "Integration setup",
            "Catalog synchronization",
            "Order workflow automation",
            "Regular performance reviews",
            "Continuous optimization"
        ],
        "price_starting": "₹25,000/month",
        "turnaround": "48-72 hours",
        "team_size": "Dedicated team of 8-12 specialists",
        "free_trial": "5 days",
        "ideal_for": "Multi-channel sellers, Brands, D2C businesses",
        "faq": [
            {
                "question": "Which marketplaces do you integrate with?",
                "answer": "We integrate with all major marketplaces including Amazon, Flipkart, eBay, Etsy, Shopify, WooCommerce, Magento, and more."
            },
            {
                "question": "How does inventory synchronization work?",
                "answer": "When a sale happens on any platform, inventory is automatically updated across all your channels in real-time. This prevents overselling and stockouts."
            },
            {
                "question": "Do you provide analytics?",
                "answer": "Yes, we provide comprehensive monthly reports including sales analytics, inventory reports, and platform performance metrics."
            }
        ]
    },
    {
        "id": 3,
        "icon": "fa-solid fa-code",
        "title": "Web Development",
        "short_desc": "Custom ecommerce websites built for performance",
        "description": "Professional ecommerce website development services. We build custom, responsive, and SEO-friendly online stores that are optimized for conversions.",
        "full_description": "Our Web Development team creates stunning, high-performance ecommerce websites tailored to your brand and business goals. We specialize in custom ecommerce solutions using the latest technologies and best practices. From simple storefronts to complex multi-vendor marketplaces, we deliver websites that not only look great but also drive sales. Our development process focuses on user experience, mobile responsiveness, fast loading times, and SEO optimization. We use modern frameworks and technologies including React, Vue.js, Python, and Node.js. Every website we build includes secure payment gateway integration, user-friendly admin panel, and comprehensive analytics. We provide ongoing maintenance and support to ensure your website always performs at its best.",
        "features": [
            "Custom ecommerce website design",
            "Mobile-responsive development",
            "SEO-optimized architecture",
            "Fast loading and performance optimized",
            "Secure payment gateway integration",
            "User-friendly admin panel",
            "Multi-vendor marketplace support",
            "Ongoing maintenance and support"
        ],
        "benefits": [
            "Stand out with unique, custom design",
            "Convert more visitors with optimized UX",
            "Rank higher with SEO-friendly code",
            "Scale easily as your business grows",
            "24/7 technical support included"
        ],
        "process": [
            "Requirements gathering",
            "UI/UX design and prototyping",
            "Development and coding",
            "Testing and quality assurance",
            "Deployment and launch",
            "Post-launch support"
        ],
        "price_starting": "₹50,000 (one-time)",
        "turnaround": "4-8 weeks",
        "team_size": "Dedicated team of 4-6 developers",
        "free_trial": "Free consultation",
        "ideal_for": "Startups, Growing brands, Enterprise businesses",
        "faq": [
            {
                "question": "Which technologies do you use?",
                "answer": "We use modern technologies including Python (Flask/Django), Node.js, React, Vue.js, and various ecommerce platforms like Shopify, WooCommerce, and Magento."
            },
            {
                "question": "Do you provide hosting?",
                "answer": "Yes, we provide reliable hosting options and can help you choose the best plan based on your traffic and requirements."
            },
            {
                "question": "Is maintenance included?",
                "answer": "We offer various maintenance packages including security updates, backups, and feature enhancements. You can choose what works best for you."
            }
        ]
    },
    {
        "id": 4,
        "icon": "fa-solid fa-headset",
        "title": "Customer Support",
        "short_desc": "24/7 customer service outsourcing",
        "description": "Round-the-clock customer support services. Our trained professionals handle customer inquiries, complaints, and support tickets with professionalism.",
        "full_description": "Our Customer Support service ensures your customers always have someone to turn to. We provide 24/7 support across multiple channels including email, chat, phone, and social media. Our trained support agents handle everything from product inquiries and order status updates to returns and complaints. We follow your brand guidelines and maintain a professional, friendly tone in all interactions. With our service, you can focus on growing your business while we take care of your customers. Our support team is trained in conflict resolution, product knowledge, and customer satisfaction techniques. We provide detailed reports on customer interactions, response times, and satisfaction ratings. Our multi-lingual support team can handle customers from around the world in their preferred language.",
        "features": [
            "24/7 support across all time zones",
            "Multi-channel support (email, chat, phone, social)",
            "Ticket management system",
            "Returns and refunds processing",
            "Order tracking and updates",
            "Product information and recommendations",
            "Complaint resolution",
            "Customer feedback collection"
        ],
        "benefits": [
            "Never miss a customer inquiry",
            "Improve customer satisfaction scores",
            "Reduce response times dramatically",
            "Handle peak seasons effortlessly",
            "Focus on core business activities"
        ],
        "process": [
            "Brand voice training",
            "System integration",
            "Agent onboarding",
            "Live support handover",
            "Quality monitoring",
            "Monthly performance reviews"
        ],
        "price_starting": "₹20,000/month",
        "turnaround": "24/7 availability",
        "team_size": "Dedicated team of 10-15 agents",
        "free_trial": "7 days",
        "ideal_for": "Ecommerce stores, SaaS companies, Service businesses",
        "faq": [
            {
                "question": "What channels do you support?",
                "answer": "We support all major channels including email, live chat, phone, WhatsApp, Facebook Messenger, Instagram, and Twitter."
            },
            {
                "question": "How quickly do you respond?",
                "answer": "Our average response time is under 2 minutes for chat, 1 hour for email, and we answer all calls immediately during business hours."
            },
            {
                "question": "Do you provide support in multiple languages?",
                "answer": "Yes, our team supports English, Hindi, Malayalam, Tamil, and Kannada. We can arrange support in other languages as needed."
            }
        ]
    }
]

# Get unique categories
categories = []
for product in products:
    if product['category'] not in categories:
        categories.append(product['category'])

# Store orders in memory
orders = []


@app.route('/')
def index():
    """Homepage - Show both services and featured products"""
    featured = [p for p in products if p.get('featured', False)]
    return render_template('index.html', services=services, featured_products=featured[:4])


@app.route('/dropship')
def dropship():
    """Dropshipping store - For CUSTOMERS to buy products with category filter"""
    category = request.args.get('category', 'all')

    if category and category != 'all':
        filtered_products = [p for p in products if p['category_slug'] == category]
    else:
        filtered_products = products

    return render_template('dropship.html',
                           products=filtered_products,
                           categories=categories,
                           current_category=category)


@app.route('/product_details/<int:product_id>')
def product_details(product_id):
    """Product detail page - Customers can place order here with payment options"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product_details.html', product=product)
    return "Product not found", 404


@app.route('/service_details/<int:service_id>')
def service_details(service_id):
    """Service detail page - Shows complete information about the selected service"""
    service = next((s for s in services if s['id'] == service_id), None)
    if service:
        return render_template('service_details.html', service=service, services=services)
    return "Service not found", 404


@app.route('/about')
def about():
    """About us page"""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form handling"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        print("\n" + "=" * 50)
        print("📧 CONTACT FORM SUBMISSION")
        print("=" * 50)
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        print("=" * 50 + "\n")

        return jsonify({"success": True, "message": "Message sent successfully!"})
    return render_template('contact.html')


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    """Customer registration page"""
    if request.method == 'POST':
        return jsonify({"success": True, "message": "Registration successful!"})
    return render_template('customer_register.html')


@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    """Customer login page with redirect to previous page"""
    if request.method == 'POST':
        # In real app, verify credentials here
        session['user_id'] = 1
        session['username'] = request.form.get('username', 'Customer')

        # Get the page they came from
        next_page = request.form.get('next', '/dropship')

        return jsonify({
            "success": True,
            "message": "Login successful!",
            "redirect": next_page
        })

    # GET request - show login page
    next_page = request.args.get('next', '/dropship')
    return render_template('customer_login.html', next=next_page)


@app.route('/customer/logout')
def customer_logout():
    """Customer logout"""
    session.clear()
    return redirect(url_for('dropship'))


@app.route('/customer/dashboard')
def customer_dashboard():
    """Customer dashboard page"""
    if 'user_id' not in session:
        return redirect(url_for('customer_login', next=request.path))
    return render_template('customer_dashboard.html', username=session.get('username'))


@app.route('/place-order', methods=['POST'])
def place_order():
    """Customer places an order with payment method"""
    data = request.form

    # Generate order number
    order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Get product
    product = next((p for p in products if p['id'] == int(data.get('product_id'))), None)

    if not product:
        return jsonify({"success": False, "message": "Product not found"})

    quantity = int(data.get('quantity', 1))
    total = product['price'] * quantity
    supplier_total = product['supplier_price'] * quantity
    profit = total - supplier_total
    payment_method = data.get('payment_method', 'cod')

    # Create order
    order = {
        "order_number": order_number,
        "customer_name": data.get('name'),
        "customer_email": data.get('email'),
        "customer_phone": data.get('phone'),
        "shipping_address": f"{data.get('address')}, {data.get('city')}, {data.get('state')} - {data.get('pincode')}",
        "product": product['name'],
        "quantity": quantity,
        "customer_paid": total,
        "supplier_name": product['supplier_name'],
        "supplier_phone": product['supplier_phone'],
        "supplier_email": product['supplier_email'],
        "supplier_cost": supplier_total,
        "your_profit": profit,
        "payment_method": "Cash on Delivery" if payment_method == 'cod' else "Card Payment",
        "payment_status": "Pending" if payment_method == 'cod' else "Paid",
        "status": "pending",
        "date": datetime.now().strftime("%d %b %Y %H:%M")
    }

    # Save order
    orders.append(order)

    # PRINT ORDER DETAILS - YOU WILL SEE THIS IN TERMINAL
    print("\n" + "=" * 70)
    print("🔔 NEW CUSTOMER ORDER RECEIVED - ACTION REQUIRED! 🔔".center(70))
    print("=" * 70)
    print(f"ORDER NUMBER: {order_number}")
    print("-" * 70)
    print("👤 CUSTOMER DETAILS:")
    print(f"   Name: {data.get('name')}")
    print(f"   Phone: {data.get('phone')}")
    print(f"   Email: {data.get('email')}")
    print("-" * 70)
    print("📦 PRODUCT DETAILS:")
    print(f"   Product: {product['name']}")
    print(f"   Quantity: {quantity}")
    print(f"   Customer Paid: ₹{total}")
    print("-" * 70)
    print("💰 PAYMENT DETAILS:")
    print(f"   Payment Method: {'Cash on Delivery' if payment_method == 'cod' else 'Card Payment'}")
    print(f"   Payment Status: {'Pending' if payment_method == 'cod' else 'Paid'}")
    print("-" * 70)
    print("🏭 SUPPLIER DETAILS (FORWARD ORDER TO):")
    print(f"   Supplier: {product['supplier_name']}")
    print(f"   Phone: {product['supplier_phone']}")
    print(f"   Email: {product['supplier_email']}")
    print(f"   You Pay Supplier: ₹{supplier_total}")
    print(f"   Your Profit: ₹{profit}")
    print("-" * 70)
    print("📬 SHIPPING ADDRESS (GIVE THIS TO SUPPLIER):")
    print(f"   {data.get('address')}")
    print(f"   {data.get('city')}, {data.get('state')} - {data.get('pincode')}")
    print("=" * 70)
    print("✅ NEXT STEPS:")
    print("1. Contact supplier immediately")
    print("2. Forward order details to supplier")
    print("3. Supplier will ship directly to customer")
    print("4. Update order status to 'Forwarded to Supplier'")
    print("=" * 70 + "\n")

    return jsonify({
        "success": True,
        "message": "Order placed successfully!",
        "order_number": order_number,
        "total": total,
        "payment_method": "cod" if payment_method == 'cod' else "card"
    })


@app.route('/admin_orders')
def admin_orders():
    """Admin page - YOU can see all orders here"""
    return render_template('admin_orders.html', orders=orders)


if __name__ == '__main__':
    app.run(debug=True, port=5000)