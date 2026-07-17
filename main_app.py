import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="VisionCraft AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b0f19, #111827, #0b0f19);
        color: white;
    }

    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00d4ff, #7c3aed, #ff4ecd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .subtitle {
        text-align: center;
        color: #aab3c5;
        font-size: 1.1rem;
        margin-bottom: 35px;
    }

    .feature-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        height: 150px;
        transition: 0.3s;
    }

    .feature-card:hover {
        border-color: #00d4ff;
        transform: translateY(-4px);
    }

    .feature-icon {
        font-size: 2rem;
    }

    .feature-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: 10px;
    }

    .upload-box {
        padding: 25px;
        border-radius: 20px;
        border: 1px dashed #475569;
        background: rgba(255,255,255,0.03);
    }

    .section-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown(
    '<div class="main-title">VISIONCRAFT AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Transform • Enhance • Create — Powered by Artificial Intelligence</div>',
    unsafe_allow_html=True
)

# ---------------- FEATURES ----------------
st.markdown('<div class="section-title">✨ AI Creative Tools</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">✂️</div>
        <div class="feature-title">Background Remover</div>
        <small>Remove backgrounds with AI</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🎨</div>
        <div class="feature-title">Cartoon Converter</div>
        <small>Turn photos into artwork</small>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">✨</div>
        <div class="feature-title">Photo Enhancer</div>
        <small>Improve image quality</small>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🖌️</div>
        <div class="feature-title">Creative Filters</div>
        <small>Anime, sketch & HDR effects</small>
    </div>
    """, unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ VisionCraft Tools")

    tool = st.selectbox(
        "Select a Tool",
        [
            "AI Background Remover",
            "Background Replacement",
            "Cartoon Effect",
            "Pencil Sketch",
            "Anime Style",
            "HDR Enhancement",
            "Photo Enhancement"
        ]
    )

    st.divider()

    st.info(
        "Upload your image and transform it using VisionCraft AI."
    )

# ---------------- UPLOAD ----------------
st.markdown('<div class="section-title">📤 Upload Your Image</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)

# ---------------- IMAGE DISPLAY ----------------
if uploaded_file:
from rembg import remove
    original_image = Image.open(uploaded_file).convert("RGBA")

    st.markdown('<div class="section-title">🖼️ Image Preview</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Image")
        st.image(
            original_image,
            use_container_width=True
        )

    with col2:
        st.subheader("Processed Image")
        st.image(
            original_image,
            use_container_width=True
        )

    # ---------------- DOWNLOAD WITH WATERMARK ----------------
    st.divider()

    st.subheader("⬇️ Download Your Creation")

    def add_watermark(image):
        """
        Adds VisionCraft watermark to the downloaded image.
        """
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

        margin = int(width * 0.025)

        x = width - text_width - margin
        y = height - text_height - margin

        # Semi-transparent watermark
        draw.rounded_rectangle(
            (
                x - 15,
                y - 10,
                x + text_width + 15,
                y + text_height + 10
            ),
            radius=12,
            fill=(0, 0, 0, 120)
        )

        draw.text(
            (x, y),
            watermark_text,
            font=font,
            fill=(255, 255, 255, 210)
        )

        return Image.alpha_composite(
            image,
            watermark_layer
        )

    watermarked_image = add_watermark(original_image)

    image_bytes = io.BytesIO()

    watermarked_image.save(
        image_bytes,
        format="PNG"
    )

    image_bytes.seek(0)

    st.download_button(
        label="⬇️ Download Image with VisionCraft Watermark",
        data=image_bytes,
        file_name="visioncraft_ai_result.png",
        mime="image/png",
        use_container_width=True
    )

else:

    st.info(
        "👆 Upload an image above to start creating with VisionCraft AI."
    )

# ---------------- FOOTER ----------------
st.divider()

st.markdown(
    "<center>© 2026 VisionCraft AI • Create Without Limits</center>",
    unsafe_allow_html=True
)
