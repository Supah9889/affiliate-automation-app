import streamlit as st
import json
import csv
import random
from datetime import datetime, timedelta
import pandas as pd
import time
import re

# Configure Streamlit page
st.set_page_config(
    page_title="Affiliate Marketing Automation Hub",
    page_icon="💰",
    layout="wide"
)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = []
if 'email_list' not in st.session_state:
    st.session_state.email_list = []
if 'analytics_data' not in st.session_state:
    st.session_state.analytics_data = []

# Product database with affiliate niches
PRODUCT_NICHES = {
    "Health & Fitness": {
        "products": [
            "Resistance Bands Set", "Yoga Mat", "Protein Powder", "Fitness Tracker", 
            "Foam Roller", "Adjustable Dumbbells", "Meal Prep Containers"
        ],
        "keywords": ["fitness", "health", "workout", "wellness", "strength", "cardio"],
        "pain_points": ["weight loss", "muscle gain", "flexibility", "energy", "recovery"]
    },
    "Home & Kitchen": {
        "products": [
            "Air Fryer", "Instant Pot", "Coffee Maker", "Blender", "Kitchen Scale",
            "Storage Containers", "Non-stick Pan Set"
        ],
        "keywords": ["cooking", "kitchen", "recipes", "meal prep", "healthy eating"],
        "pain_points": ["save time", "eat healthy", "organize kitchen", "quick meals"]
    },
    "Tech & Gadgets": {
        "products": [
            "Wireless Earbuds", "Phone Stand", "Portable Charger", "Bluetooth Speaker",
            "Laptop Stand", "Cable Organizer", "Ring Light"
        ],
        "keywords": ["tech", "gadgets", "productivity", "work from home", "mobile"],
        "pain_points": ["productivity", "organization", "battery life", "convenience"]
    },
    "Beauty & Self Care": {
        "products": [
            "Skincare Set", "Hair Straightener", "Essential Oils", "Makeup Brushes",
            "Face Mask", "Nail Care Kit", "Aromatherapy Diffuser"
        ],
        "keywords": ["beauty", "skincare", "self care", "wellness", "relaxation"],
        "pain_points": ["aging", "stress", "confidence", "time-saving", "natural"]
    },
    "Pet Care": {
        "products": [
            "Pet Camera", "Automatic Feeder", "Pet Bed", "Grooming Kit",
            "Interactive Toy", "Pet Carrier", "Training Treats"
        ],
        "keywords": ["pets", "dogs", "cats", "training", "health", "comfort"],
        "pain_points": ["pet anxiety", "training", "health monitoring", "convenience"]
    }
}

# Content templates for different platforms
CONTENT_TEMPLATES = {
    "pinterest": {
        "title_templates": [
            "😍 {product} That Will Change Your {benefit}!",
            "🔥 This {product} is Going VIRAL for Good Reason",
            "✨ {number} Reasons Why {product} is a Game Changer",
            "💕 Found the Perfect {product} for {target_audience}",
            "🎯 {product}: The {benefit} Solution You've Been Looking For"
        ],
        "description_templates": [
            "This {product} has been a total game-changer for my {pain_point}! {benefit_detail} Perfect for anyone looking to {solution}. Save this pin and check it out! #affiliate #lifestyle #wellness",
            "Ladies, I found THE {product} that actually works! 🙌 After trying countless options, this one finally delivered {benefit}. Link in bio to grab yours! #productreview #lifestyle #musthave",
            "If you struggle with {pain_point}, you NEED this {product}! It's helped me {specific_benefit} and I can't recommend it enough. Swipe to see before/after! #affiliate #problemsolved"
        ]
    },
    "reddit": {
        "title_templates": [
            "Found a {product} that actually works for {pain_point}",
            "PSA: This {product} changed my {benefit_area} routine",
            "After trying dozens of {product_category}, this one finally delivered",
            "LPT: {product} that solved my {pain_point} problem",
            "Review: {product} - honest thoughts after {time_period}"
        ],
        "content_templates": [
            "I've been dealing with {pain_point} for months and tried everything. Finally found this {product} and it's been a game changer. {specific_benefit}. Thought I'd share in case anyone else is struggling with the same issue. Happy to answer questions!\n\n[Link if interested: {affiliate_link}]",
            "Not sponsored, just genuinely excited about this {product}. I was skeptical at first but decided to try it after reading reviews. {benefit_story}. Worth every penny IMO.\n\nEdit: Since people are asking, here's where I got it: {affiliate_link}"
        ]
    },
    "tiktok": {
        "script_templates": [
            "POV: You found the {product} that actually works ✨\n\n*shows before/after*\n\nThis {product} has been viral for a reason! It helps with {benefit} and honestly changed my {routine}. Link in bio if you want to try it! #affiliate #viral #musthave",
            "Tell me you need this {product} without telling me 👀\n\n*demonstrates problem*\n*shows product solving it*\n\nSeriously this {product} is a lifesaver for {pain_point}! Everyone needs one. Link in bio! #productreview #lifehack #affiliate",
            "Things that just make sense: Getting this {product} ✅\n\n*quick demo*\n\nBest {price_point} I've spent on {category}! Who else needs this? Link in bio! #budgetfriendly #musthave #affiliate"
        ]
    }
}

# Viral content triggers
VIRAL_TRIGGERS = [
    "This changed my life", "Going viral for a reason", "Everyone needs this",
    "Can't believe this works", "Life hack alert", "Game changer",
    "Total transformation", "Before vs after", "Secret weapon",
    "Mind blown", "Obsessed with this", "Holy grail product"
]

def generate_affiliate_content(niche, product, platform, affiliate_link=""):
    """Generate platform-specific affiliate content"""
    niche_data = PRODUCT_NICHES[niche]
    pain_point = random.choice(niche_data["pain_points"])
    keyword = random.choice(niche_data["keywords"])
    trigger = random.choice(VIRAL_TRIGGERS)
    
    if platform == "pinterest":
        title_template = random.choice(CONTENT_TEMPLATES["pinterest"]["title_templates"])
        desc_template = random.choice(CONTENT_TEMPLATES["pinterest"]["description_templates"])
        
        title = title_template.format(
            product=product,
            benefit=pain_point,
            number=random.randint(3, 10),
            target_audience="busy moms" if niche == "Home & Kitchen" else "everyone"
        )
        
        description = desc_template.format(
            product=product,
            pain_point=pain_point,
            benefit=f"improved {keyword}",
            benefit_detail=trigger,
            solution=f"improve their {keyword}",
            specific_benefit=f"reduced {pain_point} by 80%"
        )
        
        return {
            "platform": "Pinterest",
            "title": title,
            "description": description,
            "hashtags": f"#{keyword} #affiliate #lifestyle #musthave #{niche.lower().replace(' ', '')}"
        }
    
    elif platform == "reddit":
        title_template = random.choice(CONTENT_TEMPLATES["reddit"]["title_templates"])
        content_template = random.choice(CONTENT_TEMPLATES["reddit"]["content_templates"])
        
        title = title_template.format(
            product=product,
            pain_point=pain_point,
            benefit_area=keyword,
            product_category=f"{product.lower()}s",
            time_period="3 months"
        )
        
        content = content_template.format(
            pain_point=pain_point,
            product=product,
            specific_benefit=f"It's helped reduce my {pain_point} significantly",
            benefit_story=f"Within a week I noticed {trigger.lower()}",
            affiliate_link=affiliate_link or "[Your affiliate link here]"
        )
        
        return {
            "platform": "Reddit",
            "title": title,
            "content": content,
            "suggested_subreddits": [f"r/{keyword}", f"r/{niche.split()[0].lower()}", "r/BuyItForLife"]
        }
    
    elif platform == "tiktok":
        script_template = random.choice(CONTENT_TEMPLATES["tiktok"]["script_templates"])
        
        script = script_template.format(
            product=product,
            benefit=f"solving {pain_point}",
            routine=f"{keyword} routine",
            pain_point=pain_point,
            price_point="$30",
            category=niche.split()[0].lower()
        )
        
        return {
            "platform": "TikTok",
            "script": script,
            "hashtags": f"#{keyword} #affiliate #viral #musthave #{product.lower().replace(' ', '')}"
        }

def create_tracking_link(original_link, source, campaign=""):
    """Create UTM tracking parameters for analytics"""
    if "?" in original_link:
        separator = "&"
    else:
        separator = "?"
    
    utm_params = f"utm_source={source}&utm_medium=affiliate&utm_campaign={campaign or 'content_marketing'}"
    return f"{original_link}{separator}{utm_params}"

def export_to_csv(data, filename):
    """Export data to CSV for download"""
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    return csv

# Streamlit UI
st.title("💰 Affiliate Marketing Automation Hub")
st.markdown("Generate viral-ready content for your affiliate marketing campaigns across Pinterest, Reddit, and TikTok!")

# Sidebar for configuration
st.sidebar.header("⚙️ Configuration")
selected_niches = st.sidebar.multiselect(
    "Select Niches",
    list(PRODUCT_NICHES.keys()),
    default=["Health & Fitness", "Tech & Gadgets"]
)

platforms = st.sidebar.multiselect(
    "Select Platforms",
    ["Pinterest", "Reddit", "TikTok"],
    default=["Pinterest", "Reddit", "TikTok"]
)

content_count = st.sidebar.slider("Content Pieces to Generate", 1, 50, 10)

# Main content area with tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🚀 Generate Content", "📊 Analytics", "📧 Email Collection", "💡 Product Research", "📁 Export Data"])

with tab1:
    st.header("Content Generation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🎯 Generate Affiliate Content", type="primary"):
            with st.spinner("Generating viral content..."):
                generated_content = []
                
                for i in range(content_count):
                    niche = random.choice(selected_niches)
                    product = random.choice(PRODUCT_NICHES[niche]["products"])
                    platform = random.choice([p.lower() for p in platforms])
                    
                    content = generate_affiliate_content(niche, product, platform)
                    content['niche'] = niche
                    content['product'] = product
                    content['generated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M")
                    content['id'] = f"{platform}_{i}_{int(time.time())}"
                    
                    generated_content.append(content)
                
                st.session_state.generated_content.extend(generated_content)
                st.success(f"✅ Generated {len(generated_content)} pieces of content!")
    
    with col2:
        if st.button("🔄 Clear All Content"):
            st.session_state.generated_content = []
            st.success("Content cleared!")
    
    # Display generated content
    if st.session_state.generated_content:
        st.subheader("📝 Generated Content Preview")
        
        for i, content in enumerate(st.session_state.generated_content[-10:]):  # Show last 10
            with st.expander(f"{content['platform']} - {content['product']} ({content['niche']})"):
                if content['platform'] == 'Pinterest':
                    st.write(f"**Title:** {content['title']}")
                    st.write(f"**Description:** {content['description']}")
                    st.write(f"**Hashtags:** {content['hashtags']}")
                elif content['platform'] == 'Reddit':
                    st.write(f"**Title:** {content['title']}")
                    st.write(f"**Content:** {content['content']}")
                    st.write(f"**Suggested Subreddits:** {', '.join(content['suggested_subreddits'])}")
                elif content['platform'] == 'TikTok':
                    st.write(f"**Script:** {content['script']}")
                    st.write(f"**Hashtags:** {content['hashtags']}")
                
                # Add affiliate link input
                affiliate_link = st.text_input(f"Add affiliate link for {content['id']}", key=f"link_{i}")
                if affiliate_link:
                    tracked_link = create_tracking_link(affiliate_link, content['platform'].lower(), content['niche'])
                    st.code(tracked_link, language=None)

with tab2:
    st.header("📊 Analytics Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Content Generated", len(st.session_state.generated_content))
    
    with col2:
        platforms_count = {}
        for content in st.session_state.generated_content:
            platform = content['platform']
            platforms_count[platform] = platforms_count.get(platform, 0) + 1
        
        if platforms_count:
            top_platform = max(platforms_count, key=platforms_count.get)
            st.metric("Top Platform", f"{top_platform} ({platforms_count[top_platform]})")
    
    with col3:
        niches_count = {}
        for content in st.session_state.generated_content:
            niche = content['niche']
            niches_count[niche] = niches_count.get(niche, 0) + 1
        
        if niches_count:
            top_niche = max(niches_count, key=niches_count.get)
            st.metric("Top Niche", f"{top_niche} ({niches_count[top_niche]})")
    
    # Platform distribution chart
    if st.session_state.generated_content:
        platform_df = pd.DataFrame(list(platforms_count.items()), columns=['Platform', 'Count'])
        st.bar_chart(platform_df.set_index('Platform'))
    
    # UTM Tracking Setup
    st.subheader("🔗 UTM Link Generator")
    original_url = st.text_input("Original Affiliate URL")
    source = st.selectbox("Traffic Source", ["pinterest", "reddit", "tiktok", "instagram", "other"])
    campaign = st.text_input("Campaign Name (optional)")
    
    if original_url:
        tracked_url = create_tracking_link(original_url, source, campaign)
        st.code(tracked_url)
        st.info("💡 Use this tracked link to monitor performance in Google Analytics!")

with tab3:
    st.header("📧 Email Collection")
    
    st.markdown("Collect emails from interested visitors:")
    
    with st.form("email_collection"):
        st.write("**Get exclusive affiliate deals and product recommendations!**")
        email = st.text_input("Enter your email address")
        interests = st.multiselect("What interests you?", list(PRODUCT_NICHES.keys()))
        submitted = st.form_submit_button("Subscribe")
        
        if submitted and email:
            if "@" in email:
                st.session_state.email_list.append({
                    "email": email,
                    "interests": interests,
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "streamlit_app"
                })
                st.success("✅ Thanks for subscribing!")
            else:
                st.error("Please enter a valid email address")
    
    # Display email stats
    if st.session_state.email_list:
        st.subheader("📈 Email List Stats")
        st.metric("Total Subscribers", len(st.session_state.email_list))
        
        # Show recent subscribers
        if len(st.session_state.email_list) > 0:
            recent_df = pd.DataFrame(st.session_state.email_list[-5:])
            st.dataframe(recent_df)

with tab4:
    st.header("💡 Product Research")
    
    st.markdown("**Trending Product Ideas by Niche:**")
    
    for niche, data in PRODUCT_NICHES.items():
        with st.expander(f"{niche} - High Converting Products"):
            st.write("**Popular Products:**")
            for product in data['products']:
                st.write(f"• {product}")
            
            st.write("**Keywords to Target:**")
            st.write(", ".join(data['keywords']))
            
            st.write("**Pain Points to Address:**")
            st.write(", ".join(data['pain_points']))
            
            st.write("**Content Ideas:**")
            st.write(f"• '{product} review after 30 days'")
            st.write(f"• 'How {product} solved my {data['pain_points'][0]} problem'")
            st.write(f"• 'Before vs After: {product} transformation'")

with tab5:
    st.header("📁 Export Data")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Export Content to CSV") and st.session_state.generated_content:
            csv_data = export_to_csv(st.session_state.generated_content, "affiliate_content.csv")
            st.download_button(
                label="Download Content CSV",
                data=csv_data,
                file_name=f"affiliate_content_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📥 Export Email List to CSV") and st.session_state.email_list:
            csv_data = export_to_csv(st.session_state.email_list, "email_list.csv")
            st.download_button(
                label="Download Email List CSV",
                data=csv_data,
                file_name=f"email_list_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )

# Footer with tips
st.markdown("---")
st.markdown("""
### 🚀 Quick Start Tips:
1. **Generate 20-30 pieces** of content daily across all platforms
2. **Post consistently** - 5-10 pieces per platform daily  
3. **Track everything** - use UTM links to see what converts
4. **Focus on pain points** - people buy solutions, not products
5. **Engage authentically** - respond to comments and questions

### 📱 Posting Schedule:
- **Pinterest**: 15-20 pins daily, focus on lifestyle boards
- **Reddit**: 3-5 posts daily, different subreddits, be helpful first
- **TikTok**: 1-3 videos daily, trending sounds + your content

### 💰 Revenue Optimization:
- Test different affiliate programs (Amazon, ClickBank, ShareASale)
- Focus on products with 30%+ commission rates
- Create urgency with limited-time offers
- Build trust with honest reviews and comparisons
""")