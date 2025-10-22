# 🍕 Meal Mate - Modern Food Delivery App

A beautiful, modern Django-based food delivery application with a stunning UI/UX design, secure authentication, and mobile-responsive layout.

![Meal Mate](https://images.unsplash.com/photo-1504674900247-0877df9cc836?w=800&h=400&fit=crop)

## ✨ Features

### 🎨 Modern UI/UX
- **Beautiful Design**: Purple gradient theme with modern card layouts
- **Responsive**: Works perfectly on mobile, tablet, and desktop
- **Smooth Animations**: Fade-in effects and hover animations
- **Font Awesome Icons**: Beautiful icons throughout the app
- **Clean Typography**: Modern fonts and perfect spacing

### 🔐 Security & Authentication
- **Secure Login**: Proper Django authentication with password hashing
- **CSRF Protection**: All forms are protected against CSRF attacks
- **Input Validation**: Comprehensive form validation and error handling
- **User Management**: Secure user registration and login system

### 🛒 E-commerce Features
- **Restaurant Browsing**: Beautiful grid layout of restaurants
- **Menu Management**: Clean menu item display with images
- **Shopping Cart**: Interactive cart with quantity controls
- **Order Processing**: Complete order flow with confirmation
- **Payment Integration**: Razorpay payment gateway integration

### 👨‍💼 Admin Features
- **Admin Dashboard**: Clean admin interface for management
- **Restaurant Management**: Add, edit, and delete restaurants
- **Menu Management**: Manage menu items for each restaurant
- **User Management**: View and manage customer accounts

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd meal-mate
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup database**
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. **Create sample data (optional)**
```bash
python create_sample_data.py
```

6. **Run the development server**
```bash
python manage.py runserver
```

7. **Open your browser**
Navigate to `http://127.0.0.1:8000`

## 🎯 Default Credentials

### Admin Access
- **Username**: admin
- **Password**: admin
- **Email**: admin@mealmate.com

### Test Customer
Create a new account through the signup page or use the admin panel.

## 📱 Screenshots

### Home Page
Beautiful landing page with modern design and call-to-action buttons.

### Restaurant Grid
Responsive grid layout showing restaurants with ratings and cuisine types.

### Menu Items
Clean card-based layout for menu items with vegetarian indicators.

### Shopping Cart
Interactive cart with quantity controls and real-time total calculation.

### Order Confirmation
Beautiful order confirmation page with delivery details.

## 🛠️ Technology Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite (easily switchable to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.0
- **Payment**: Razorpay Integration
- **Deployment**: Railway/Render/Heroku ready

## 🎨 Design Features

### Color Palette
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Secondary**: Pink gradient (#f093fb → #f5576c)
- **Success**: Blue gradient (#4facfe → #00f2fe)
- **Background**: Dynamic gradients
- **Cards**: Clean white with subtle shadows

### Typography
- **Font Family**: Segoe UI, Tahoma, Geneva, Verdana, sans-serif
- **Responsive Text**: Scales beautifully across devices
- **Proper Hierarchy**: Clear heading and text structure

### Layout
- **Grid System**: CSS Grid for responsive layouts
- **Card Design**: Modern card-based components
- **Navigation**: Sticky navigation with backdrop blur
- **Mobile First**: Responsive design approach

## 🚀 Deployment

### Free Deployment Options

1. **Railway** (Recommended)
   - Push to GitHub
   - Connect Railway to your repo
   - Automatic deployment
   - Free `.railway.app` domain

2. **Render**
   - GitHub integration
   - Automatic builds
   - Free SSL certificates

3. **PythonAnywhere**
   - Easy Django hosting
   - Free tier available

See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## 📂 Project Structure

```
meal-mate/
├── delivery/                 # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # URL routing
│   ├── templates/           # HTML templates
│   └── static/              # CSS, JS, images
├── meal_mate/               # Django project settings
├── requirements.txt         # Python dependencies
├── Procfile                 # Deployment configuration
├── create_sample_data.py    # Sample data script
└── README.md               # This file
```

## 🔧 Configuration

### Environment Variables
For production deployment, set these environment variables:

```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
```

### Database Configuration
The app uses SQLite by default. For production, you can switch to PostgreSQL:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Django**: Amazing web framework
- **Font Awesome**: Beautiful icons
- **Unsplash**: High-quality images
- **Razorpay**: Payment processing
- **Railway**: Easy deployment platform

## 📞 Support

If you have any questions or need help with deployment, please create an issue in the repository.

---

**Made with ❤️ using Django and modern web technologies**

🌟 **Star this repository if you found it helpful!** 🌟