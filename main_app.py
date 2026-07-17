import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from rembg import remove
import io

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="VisionCraft AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM UI DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at top left, #18233d 0%, transparent 35%),
        radial-gradient(circle at bottom right, #24113d 0%, transparent 35%),
        #080b12;
    color: white;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.main-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: 4px;
    background: linear-gradient(90deg, #00e5ff, #7c4dff, #ff4fd8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 35px;
}

.card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 22px;
    margin-bottom: 20px;
    backdrop-filter: blur(12px);
}

.tool-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    min-height: 145px;
}

.tool-icon {
    font-size: 2.2rem;
}

.tool-title {
    font-size: 1rem;
    font-weight: 700;
    margin-top: 10px;
}

.tool-description {
    color: #9ca3af;
    font-size: 0.8rem;
    margin-top: 5px;
}

.section-title {
    font-size: 1.5rem;
    font-weight: 800;
    margin-top: 30px;
    margin-bottom: 18px;
}

div.stButton > button,
div.stDownloadButton > button {
    width: 100%;
    border-radius: 12px;
    min-height: 48px;
    font-weight: 700;
}

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border: 1px dashed #64748b;
    border-radius: 18px;
    padding: 15px;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================

st.markdown(
    '<div class="main-title">VISIONCRAFT AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Transform • Enhance • Create — Powered by Artificial Intelligence</div>',
    unsafe_allow_html=True
)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🎨 VisionCraft AI")

    st.markdown("---")

    selected_tool = st.selectbox(
        "🛠️ Select AI Tool",
        [
            "AI Background Remover",
            "Background Replacement",
            "Cartoon Converter",
            "Pencil Sketch",
            "Anime Style",
            "HDR Enhancement",
            "Photo Enhancer"
        ]
    )

    st.markdown("---")

    st.markdown("### ✨ Available Features")

    st.markdown("""
    ✅ AI Background Removal  
    ✅ Transparent PNG Output  
    ✅ Cartoon Effects  
    ✅ Anime Style  
    ✅ Pencil Sketch  
    ✅ HDR Enhancement  
    ✅ Photo Enhancement  
    ✅ VisionCraft Watermark  
    """)

# =====================================================
# FEATURE CARDS
# =====================================================

st.markdown(
    '<div class="section-title">✨ AI Creative Studio</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">✂️</div>
        <div class="tool-title">Background Remover</div>
        <div class="tool-description">Remove backgrounds using AI</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🎨</div>
        <div class="tool-title">Cartoon Converter</div>
        <div class="tool-description">Transform images into art</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">✨</div>
        <div class="tool-title">AI Enhancer</div>
        <div class="tool-description">Improve image quality</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🖌️</div>
        <div class="tool-title">Creative Filters</div>
        <div class="tool-description">Anime, sketch and HDR</div>
    </div>
    """, unsafe_allow_html=True)

# =====================================================
# IMAGE UPLOAD
# =====================================================

st.markdown(
    '<div class="section-title">📤 Upload Your Image</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload JPG, JPEG, PNG or WEBP image",
    type=["jpg", "jpeg", "png", "webp"]
)

# =====================================================
# WATERMARK FUNCTION
# =====================================================

def add_watermark(image):

    image = image.convert("RGBA")

    watermark_layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(watermark_layer)

    width, height = image.size

    watermark_text = "VISIONCRAFT AI"

    font_size = max(18, int(width * 0.025))

    try:

        font = ImageFont.truetype(
            "DejaVuSans-Bold.ttf",
            font_size
        )

    except:

        font = ImageFont.load_default()

    bbox = draw.textbbox(
        (0, 0),
        watermark_text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    margin = max(20, int(width * 0.025))

    x = width - text_width - margin
    y = height - text_height - margin

    # Watermark background
    draw.rounded_rectangle(
        (
            x - 15,
            y - 10,
            x + text_width + 15,
            y + text_height + 10
        ),
        radius=12,
        fill=(0, 0, 0, 130)
    )

    # Watermark text
    draw.text(
        (x, y),
        watermark_text,
        font=font,
        fill=(255, 255, 255, 220)
    )

    return Image.alpha_composite(
        image,
        watermark_layer
    )

# =====================================================
# IMAGE PROCESSING
# =====================================================

if uploaded_file:

    original_image = Image.open(uploaded_file).convert("RGBA")

    st.markdown(
        '<div class="section-title">🖼️ Image Comparison</div>',
        unsafe_allow_html=True
    )

    # ---------------- PROCESS IMAGE ----------------

    if selected_tool == "AI Background Remover":

        with st.spinner("🤖 AI is removing the background..."):

            processed_image = remove(original_image)

        st.success("✅ Background removed successfully!")

    else:

        processed_image = original_image

        st.info(
            f"🛠️ {selected_tool} will be added in the next development step."
        )

    # ---------------- SIDE BY SIDE DISPLAY ----------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🖼️ Original")

        st.image(
            original_image,
            use_container_width=True
        )

    with col2:

        st.markdown("### ✨ VisionCraft Result")

        st.image(
            processed_image,
            use_container_width=True
        )

    # =================================================
    # DOWNLOAD SECTION
    # =================================================

    st.markdown(
        '<div class="section-title">⬇️ Download Your Creation</div>',
        unsafe_allow_html=True
    )

    watermarked_image = add_watermark(processed_image)

    image_bytes = io.BytesIO()

    watermarked_image.save(
        image_bytes,
        format="PNG"
    )

    image_bytes.seek(0)

    st.download_button(
        label="⬇️ Download Image • Powered by VisionCraft AI",
        data=image_bytes,
        file_name="visioncraft_ai_result.png",
        mime="image/png",
        use_container_width=True
    )

else:

    st.info(
        "👆 Upload an image above to start creating with VisionCraft AI."
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

st.markdown(
    "<center>© 2026 VisionCraft AI • Create Without Limits</center>",
    unsafe_allow_html=True
)
