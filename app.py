import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. GLOBAL PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Netflix Clone - Premium Edition",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. SENIOR-LEVEL CUSTOM CSS INJECTION
# ==========================================
# Overriding Streamlit's default UI to match Netflix's dark, cinematic branding
st.markdown("""
    <style>
    /* Import Netflix Font */
    @import url('https://fonts.googleapis.com/css2?family=Netflix+Sans:wght@300;400;700&display=swap');
    
    * {
        font-family: 'Netflix Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    /* Background and global theme override */
    .stApp {
        background-color: #141414;
        color: #FFFFFF;
    }
    
    /* Hide top header and default hamburger menu for immersion */
    header, footer, #MainMenu {
        visibility: hidden !important;
    }
    
    /* Custom Styling for Title/Headers */
    .netflix-logo {
        color: #E50914;
        font-size: 45px;
        font-weight: bold;
        letter-spacing: -1px;
        margin-bottom: 20px;
    }
    
    .row-title {
        color: #E5E5E5;
        font-size: 22px;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 15px;
        padding-left: 5px;
    }

    /* Hero Banner styling */
    .hero-container {
        position: relative;
        background: linear-gradient(rgba(0,0,0,0.1), rgba(20,20,20,1)), 
                    url('https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=1964&auto=format&fit=crop');
        background-size: cover;
        background-position: center;
        height: 70vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        padding: 60px;
        border-radius: 8px;
        margin-bottom: -50px;
    }
    
    .hero-title {
        font-size: 64px;
        font-weight: 800;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.8);
    }
    
    .hero-desc {
        font-size: 18px;
        max-width: 600px;
        margin-bottom: 20px;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
        line-height: 1.4;
    }

    /* Custom Streamlit Button Styling to match Netflix Design Language */
    div.stButton > button {
        background-color: rgba(109, 109, 110, 0.7);
        color: white;
        border: none;
        padding: 10px 24px;
        font-size: 16px;
        font-weight: bold;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    
    div.stButton > button:hover {
        background-color: #FFFFFF;
        color: #000000;
        transform: scale(1.05);
    }

    /* Special rule for the Play Button */
    div.play-btn > div > div > button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    div.play-btn > div > div > button:hover {
        background-color: rgba(255, 255, 255, 0.75) !important;
    }

    /* Movie Card Hover Animations */
    .movie-card {
        border-radius: 4px;
        overflow: hidden;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    
    .movie-card:hover {
        transform: scale(1.08);
        box-shadow: 0px 10px 20px rgba(0,0,0,0.6);
        z-index: 10;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MOCK DATA ENGINE (Catalog & Metadata)
# ==========================================
MOVIES_DATABASE = {
    "Trending Now": [
        {"id": "t1", "title": "Stranger Things", "img": "https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/b9EkMc79ZSU"},
        {"id": "t2", "title": "The Crown", "img": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/JWtnJjn6ng0"},
        {"id": "t3", "title": "Ozark", "img": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/5hAXVqrljbs"},
        {"id": "t4", "title": "Black Mirror", "img": "https://images.unsplash.com/photo-1535016120720-40c646be5580?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/V0XRbkIcg74"},
    ],
    "Action & Sci-Fi Thrillers": [
        {"id": "a1", "title": "Blade Runner", "img": "https://images.unsplash.com/photo-1614850523459-c2f4c699c52e?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/gCcx85zbxz4"},
        {"id": "a2", "title": "Cyberpunk", "img": "https://images.unsplash.com/photo-1542751371-adc38448a05e?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/JqgConP7uUo"},
        {"id": "a3", "title": "Interstellar", "img": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/zSWdZVtXT7E"},
        {"id": "a4", "title": "The Matrix", "img": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=400&auto=format&fit=crop&q=60", "video_url": "https://www.youtube.com/embed/vKQi3bBA1y8"},
    ]
}

# ==========================================
# 4. SESSION STATE MANAGEMENT
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "active_video" not in st.session_state:
    st.session_state.active_video = None

# ==========================================
# 5. VIEW CONTROLLER (Auth vs Dashboard)
# ==========================================
if not st.session_state.logged_in:
    # --------------------------------------
    # AUTHENTICATION SCREEN
    # --------------------------------------
    st.markdown('<div class="netflix-logo">NETFLIX</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
            <div style="background-color: rgba(0,0,0,0.75); padding: 40px; border-radius: 8px;">
                <h2 style="margin-bottom: 20px;">Sign In</h2>
            </div>
        """, unsafe_allow_html=True)
        
        email = st.text_input("Email or phone number")
        password = st.text_input("Password", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Sign In", use_container_width=True):
            if email and password:  # Basic check for simulation
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Please enter valid credentials.")
else:
    # --------------------------------------
    # PREMIUM OTT DASHBOARD
    # --------------------------------------
    
    # Navigation Bar Header
    nav_col1, nav_col2 = st.columns([8, 1])
    with nav_col1:
        st.markdown('<div class="netflix-logo" style="font-size: 35px; margin:0;">NETFLIX</div>', unsafe_allow_html=True)
    with nav_col2:
        if st.button("Sign Out"):
            st.session_state.logged_in = False
            st.session_state.active_video = None
            st.rerun()

    # --- HERO BANNER ---
    st.markdown("""
        <div class="hero-container">
            <div class="hero-title">ECHOES OF THE COSMOS</div>
            <div class="hero-desc">When a deep-space transmission cuts out midway through an interstellar research voyage, a solo pilot risks everything to travel to the edge of a black hole to find the truth.</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Hero Call To Actions
    btn_col1, btn_col2, _ = st.columns([1.2, 1.5, 6])
    with btn_col1:
        # Wrap button in a specialized div for target styling
        st.markdown('<div class="play-btn">', unsafe_allow_html=True)
        if st.button("▶ Play", key="hero_play"):
            st.session_state.active_video = "https://www.youtube.com/embed/zSWdZVtXT7E"
        st.markdown('</div>', unsafe_allow_html=True)
    with btn_col2:
        if st.button("ⓘ More Info", key="hero_info"):
            st.toast("⚡ Produced in 4K Ultra HD. Starring Amrit Pathak.")

    # --- VIDEO MODAL INTERPOLATION ---
    # When a movie state is active, render an ultra-responsive video player container
    if st.session_state.active_video:
        st.markdown("---")
        modal_col1, modal_col2 = st.columns([7, 1])
        with modal_col1:
            st.markdown("### 🎬 Now Playing")
        with modal_col2:
            if st.button("✕ Close Player", use_container_width=True):
                st.session_state.active_video = None
                st.rerun()
                
        # Embedded H-Definition Video Player Component
        components.iframe(st.session_state.active_video, height=500, scrolling=False)
        st.markdown("---")

    # --- DYNAMIC ROW CAROUSELS ---
    for genre, movies in MOVIES_DATABASE.items():
        st.markdown(f'<div class="row-title">{genre}</div>', unsafe_allow_html=True)
        
        # Split row grid evenly using structural columns
        cols = st.columns(len(movies))
        
        for idx, movie in enumerate(movies):
            with cols[idx]:
                # Render UI card with hover framework via CSS
                st.markdown(f"""
                    <div class="movie-card">
                        <img src="{movie['img']}" style="width: 100%; aspect-ratio: 16/9; object-fit: cover; border-radius: 4px; margin-bottom: 8px;">
                        <div style="font-weight: bold; font-size: 14px; color: #E5E5E5;">{movie['title']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Invisible/Seamless click layer right under the card
                if st.button("Watch Trailer", key=f"btn_{movie['id']}", use_container_width=True):
                    st.session_state.active_video = movie['video_url']
                    st.rerun()
