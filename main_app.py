import streamlit as st
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from rembg import remove
import io

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="VisionCraft AI",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# PREMIUM UI
# =========================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, #172554 0%, transparent 30%),
        radial-gradient(circle at 100% 100%, #2e1065 0%, transparent 35%),
        #070a12;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}

.main-title {
    text-align: center;
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: 5px;
    background: linear-gradient(90deg, #00e5ff, #8b5cf6, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    color: #9ca3af;
    font-size: 1.1rem;
    margin-bottom: 35px;
}

.section-title {
    font-size: 1.6rem;
    font-weight: 800;
    margin-top: 28px;
    margin-bottom: 18px;
}

.tool-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 20px;
    text-align: center;
    min-height: 145px;
}

.tool-icon {
    font-size: 2.3rem;
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

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.04);
    border: 1px dashed #64748b;
    border-radius: 18px;
    padding: 12px;
}

div.stButton > button,
div.stDownloadButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 12px;
    font-weight: 700;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">VISIONCRAFT AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Transform • Enhance • Create — Powered by Artificial Intelligence</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🎨 VisionCraft AI")

    st.divider()

    selected_tool = st.selectbox(
        "🛠️ Select AI Tool",
        [
            "AI Background Remover",
            "Background Replacement",
            "Cartoon Converter",
            "Pencil Sketch",
            "Anime Style Filter",
            "HDR Enhancement",
            "Photo Enhancer",
            "Image Adjustments"
        ]
    )

    st.divider()

    st.markdown("### ✨ Features")

    st.markdown("""
    ✅ AI Background Removal  
    ✅ Custom Backgrounds  
    ✅ Cartoon Effects  
    ✅ Pencil Sketch  
    ✅ Anime Filter  
    ✅ HDR Enhancement  
    ✅ Photo Enhancement  
    ✅ Brightness & Contrast  
    ✅ Sharpening & Denoising  
    ✅ VisionCraft Watermark  
    """)

# =========================================================
# FEATURE CARDS
# =========================================================

st.markdown(
    '<div class="section-title">✨ AI Creative Studio</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">✂️</div>
        <div class="tool-title">Background Remover</div>
        <div class="tool-description">AI-powered segmentation</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">🎨</div>
        <div class="tool-title">Creative Filters</div>
        <div class="tool-description">Cartoon, anime and sketch</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">✨</div>
        <div class="tool-title">AI Enhancement</div>
        <div class="tool-description">Improve image quality</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="tool-card">
        <div class="tool-icon">⚡</div>
        <div class="tool-title">Image Control</div>
        <div class="tool-description">Adjust every detail</div>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# IMAGE UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">📤 Upload Image</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload your main image",
    type=["jpg", "jpeg", "png", "webp"]
)

# =========================================================
# FUNCTIONS
# =========================================================

def pil_to_cv(image):
    return cv2.cvtColor(
        np.array(image.convert("RGB")),
        cv2.COLOR_RGB2BGR
    )


def cv_to_pil(image):
    return Image.fromarray(
        cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    )


def background_removal(image):

    return remove(image)


def cartoon_effect(image):

    img = pil_to_cv(image)

    # Smooth image
    smooth = cv2.bilateralFilter(
        img,
        d=9,
        sigmaColor=75,
        sigmaSpace=75
    )

    # Edge detection
    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.adaptiveThreshold(
        cv2.medianBlur(gray, 7),
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        2
    )

    edges = cv2.cvtColor(
        edges,
        cv2.COLOR_GRAY2BGR
    )

    cartoon = cv2.bitwise_and(
        smooth,
        edges
    )

    return cv_to_pil(cartoon)


def pencil_sketch(image):

    img = pil_to_cv(image)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    inverted = 255 - gray

    blurred = cv2.GaussianBlur(
        inverted,
        (21, 21),
        0
    )

    sketch = cv2.divide(
        gray,
        255 - blurred,
        scale=256
    )

    return Image.fromarray(sketch)


def anime_effect(image):

    img = pil_to_cv(image)

    smooth = cv2.bilateralFilter(
        img,
        9,
        150,
        150
    )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    edges = cv2.Canny(
        gray,
        80,
        150
    )

    edges = cv2.cvtColor(
        edges,
        cv2.COLOR_GRAY2BGR
    )

    anime = cv2.bitwise_and(
        smooth,
        255 - edges
    )

    return cv_to_pil(anime)


def hdr_effect(image):

    img = pil_to_cv(image)

    lab = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2LAB
    )

    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=3.0,
        tileGridSize=(8, 8)
    )

    enhanced_l = clahe.apply(l)

    enhanced = cv2.merge(
        (enhanced_l, a, b)
    )

    enhanced = cv2.cvtColor(
        enhanced,
        cv2.COLOR_LAB2BGR
    )

    return cv_to_pil(enhanced)


def enhance_image(image):

    image = ImageEnhance.Sharpness(image).enhance(1.8)
    image = ImageEnhance.Contrast(image).enhance(1.2)
    image = ImageEnhance.Color(image).enhance(1.15)

    return image


def denoise_image(image):

    img = pil_to_cv(image)

    denoised = cv2.fastNlMeansDenoisingColored(
        img,
        None,
        10,
        10,
        7,
        21
    )

    return cv_to_pil(denoised)


def sharpen_image(image):

    return image.filter(
        ImageFilter.UnsharpMask(
            radius=2,
            percent=180,
            threshold=3
        )
    )


def replace_background(subject_image, background_image):

    subject = remove(subject_image)

    subject = subject.convert("RGBA")
    background = background_image.convert("RGBA")

    background = background.resize(
        subject.size
    )

    return Image.alpha_composite(
        background,
        subject
    )


def add_watermark(image):

    image = image.convert("RGBA")

    layer = Image.new(
        "RGBA",
        image.size,
        (0, 0, 0, 0)
    )

    draw = ImageDraw.Draw(layer)

    width, height = image.size

    text = "VISIONCRAFT AI"

    font_size = max(
        18,
        int(width * 0.025)
    )

    try:

        font = ImageFont.truetype(
            "DejaVuSans-Bold.ttf",
            font_size
        )

    except:

        font = ImageFont.load_default()

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    margin = max(
        20,
        int(width * 0.025)
    )

    x = width - text_width - margin
    y = height - text_height - margin

    draw.rounded_rectangle(
        (
            x - 15,
            y - 10,
            x + text_width + 15,
            y + text_height + 10
        ),
        radius=12,
        fill=(0, 0, 0, 135)
    )

    draw.text(
        (x, y),
        text,
        font=font,
        fill=(255, 255, 255, 225)
    )

    return Image.alpha_composite(
        image,
        layer
    )


# =========================================================
# MAIN PROCESSING
# =========================================================

if uploaded_file:

    original_image = Image.open(
        uploaded_file
    ).convert("RGBA")

    processed_image = original_image

    background_file = None

    # -----------------------------------------------------
    # BACKGROUND REPLACEMENT
    # -----------------------------------------------------

    if selected_tool == "Background Replacement":

        st.markdown(
            '<div class="section-title">🌄 Upload New Background</div>',
            unsafe_allow_html=True
        )

        background_file = st.file_uploader(
            "Upload background image",
            type=["jpg", "jpeg", "png", "webp"],
            key="background_upload"
        )

        if background_file:

            background_image = Image.open(
                background_file
            ).convert("RGBA")

            with st.spinner(
                "🤖 Removing subject background and replacing it..."
            ):

                processed_image = replace_background(
                    original_image,
                    background_image
                )

            st.success(
                "✅ Background replaced successfully!"
            )

        else:

            st.info(
                "Upload a second image to replace the background."
            )

    # -----------------------------------------------------
    # BACKGROUND REMOVER
    # -----------------------------------------------------

    elif selected_tool == "AI Background Remover":

        with st.spinner(
            "🤖 AI is removing the background..."
        ):

            processed_image = background_removal(
                original_image
            )

        st.success(
            "✅ Background removed successfully!"
        )

    # -----------------------------------------------------
    # CARTOON
    # -----------------------------------------------------

    elif selected_tool == "Cartoon Converter":

        with st.spinner(
            "🎨 Creating cartoon effect..."
        ):

            processed_image = cartoon_effect(
                original_image
            )

        st.success(
            "✅ Cartoon effect created!"
        )

    # -----------------------------------------------------
    # PENCIL SKETCH
    # -----------------------------------------------------

    elif selected_tool == "Pencil Sketch":

        with st.spinner(
            "✏️ Creating pencil sketch..."
        ):

            processed_image = pencil_sketch(
                original_image
            )

        st.success(
            "✅ Pencil sketch created!"
        )

    # -----------------------------------------------------
    # ANIME
    # -----------------------------------------------------

    elif selected_tool == "Anime Style Filter":

        with st.spinner(
            "🌟 Applying anime style..."
        ):

            processed_image = anime_effect(
                original_image
            )

        st.success(
            "✅ Anime-style filter applied!"
        )

    # -----------------------------------------------------
    # HDR
    # -----------------------------------------------------

    elif selected_tool == "HDR Enhancement":

        with st.spinner(
            "🔥 Enhancing dynamic range..."
        ):

            processed_image = hdr_effect(
                original_image
            )

        st.success(
            "✅ HDR enhancement completed!"
        )

    # -----------------------------------------------------
    # PHOTO ENHANCER
    # -----------------------------------------------------

    elif selected_tool == "Photo Enhancer":

        with st.spinner(
            "✨ Enhancing your photo..."
        ):

            processed_image = enhance_image(
                original_image
            )

        st.success(
            "✅ Photo enhanced successfully!"
        )

    # -----------------------------------------------------
    # IMAGE ADJUSTMENTS
    # -----------------------------------------------------

    elif selected_tool == "Image Adjustments":

        st.markdown(
            '<div class="section-title">🎚️ Adjust Image</div>',
            unsafe_allow_html=True
        )

        brightness = st.slider(
            "☀️ Brightness",
            0.1,
            3.0,
            1.0,
            0.1
        )

        contrast = st.slider(
            "🎚️ Contrast",
            0.1,
            3.0,
            1.0,
            0.1
        )

        saturation = st.slider(
            "🌈 Color Saturation",
            0.0,
            3.0,
            1.0,
            0.1
        )

        sharpness = st.slider(
            "🔍 Sharpness",
            0.0,
            3.0,
            1.0,
            0.1
        )

        denoise = st.checkbox(
            "🧹 Apply Denoising"
        )

        processed_image = ImageEnhance.Brightness(
            original_image
        ).enhance(brightness)

        processed_image = ImageEnhance.Contrast(
            processed_image
        ).enhance(contrast)

        processed_image = ImageEnhance.Color(
            processed_image
        ).enhance(saturation)

        processed_image = ImageEnhance.Sharpness(
            processed_image
        ).enhance(sharpness)

        if denoise:

            processed_image = denoise_image(
                processed_image
            )

        st.success(
            "✅ Image adjustments applied!"
        )

    # =====================================================
    # COMPARISON
    # =====================================================

    st.markdown(
        '<div class="section-title">🖼️ Before & After</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Original Image")

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

    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.markdown(
        '<div class="section-title">⬇️ Download Your Creation</div>',
        unsafe_allow_html=True
    )

    watermarked_image = add_watermark(
        processed_image
    )

    image_bytes = io.BytesIO()

    watermarked_image.save(
        image_bytes,
        format="PNG"
    )

    image_bytes.seek(0)

    st.download_button(
        label="⬇️ Download Image with VisionCraft AI Watermark",
        data=image_bytes,
        file_name="visioncraft_ai_result.png",
        mime="image/png",
        use_container_width=True
    )

else:

    st.info(
        "👆 Upload an image above to start creating with VisionCraft AI."
    )

# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    "<center>© 2026 VisionCraft AI • Create Without Limits 🎨</center>",
    unsafe_allow_html=True
)
