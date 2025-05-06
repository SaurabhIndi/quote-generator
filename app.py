import streamlit as st
import torch
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import re

def load_model():
    """Load the pre-trained GPT-2 model and tokenizer."""
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    return tokenizer, model

# Load model and tokenizer once at startup
@st.cache_resource
def get_model():
    return load_model()

tokenizer, model = get_model()

def generate_quote(theme, max_length=60):
    """Generate an inspirational quote based on the given theme with a placeholder author."""
    prompt = f"An inspirational quote about {theme}:"
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    
    outputs = model.generate(
        inputs,
        max_length=max_length,
        num_return_sequences=1,
        no_repeat_ngram_size=2,
        do_sample=True,
        top_k=50,
        top_p=0.95,
        temperature=0.7,
        pad_token_id=tokenizer.eos_token_id
    )
    
    quote = tokenizer.decode(outputs[0], skip_special_tokens=True)
    quote = re.sub(r"An inspirational quote about .+?:", "", quote).strip()
    quote = quote.replace("\n", " ").strip()
    
    if not quote.endswith(('.', '!', '?')):
        quote += '.'
    
    author = "AI Sage"
    
    return quote, author

def save_quote(theme, quote, author, filename="quotes.txt"):
    """Save the generated quote with its theme and author to a file."""
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"Theme: {theme} | Quote: {quote} — {author}\n")

def get_theme_image(theme):
    """Return an Unsplash image URL and caption based on the theme."""
    theme_images = {
        "hope": {
            "url": "https://images.unsplash.com/photo-1519681393784-d120267933ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
            "caption": "Hope rises like a mountain under the stars"
        },
        "success": {
            "url": "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
            "caption": "Success is the peak of hard work"
        },
        "fire in the belly": {
            "url": "https://images.unsplash.com/photo-1515405295579-ba7b45403062?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
            "caption": "Fire in the belly ignites unstoppable passion"
        },
        "inner peace": {
            "url": "https://images.unsplash.com/photo-1508672019048-805c376b67e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
            "caption": "Inner peace flows like a serene river"
        },
        "personal growth": {
            "url": "https://images.unsplash.com/photo-1501555088652-021faa106b9b?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
            "caption": "Personal growth is a journey through nature"
        },
        "love": {
            "url": "https://images.unsplash.com/photo-1517686469429-8bdb88b9f907?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
            "caption": "Love blooms in every heart"
        }
    }
    default_image = {
        "url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1350&q=80",
        "caption": "Find inspiration in every moment"
    }
    
    theme = theme.lower().strip()
    for key in theme_images:
        if key in theme or theme in key:
            return theme_images[key]["url"], theme_images[key]["caption"]
    
    return default_image["url"], default_image["caption"]

def main():
    """Main function to run the Streamlit app."""
    # Custom CSS for styling
    st.markdown("""
        <style>
        .main {
            background-color: #f0f4f8;
            font-family: 'Arial', sans-serif;
        }
        .title {
            color: #1e3a8a;
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            margin-bottom: 1rem;
        }
        .subtitle {
            color: #4b5563;
            font-size: 1.2rem;
            text-align: center;
            margin-bottom: 2rem;
        }
        .quote-card {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 1.5rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .quote-text {
            font-size: 1.1rem;
            color: #1f2937;
            font-style: italic;
        }
        .quote-author {
            font-size: 1rem;
            color: #6b7280;
            text-align: right;
            margin-top: 0.5rem;
        }
        .stButton>button {
            background-color: #1e3a8a;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #3b82f6;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }
        .stSelectbox>div>div {
            border-radius: 8px;
            border: 1px solid #d1d5db;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header
    with st.container():
        st.markdown('<div class="title">Inspirational Quote Generator</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">Create inspiring quotes for any theme, separated by commas (e.g., success, inner peace)</div>', unsafe_allow_html=True)
        
        # Get image based on the first valid theme
        theme_input = st.session_state.get("theme_input", "")
        if theme_input:
            themes = [theme.strip().lower() for theme in theme_input.split(",") if theme.strip()]
            first_theme = themes[0] if themes else ""
            image_url, image_caption = get_theme_image(first_theme)
        else:
            image_url, image_caption = get_theme_image("")
        st.image(image_url, caption=image_caption)

    # Input form
    with st.container():
        st.markdown("### Enter Your Themes")
        with st.form(key="quote_form"):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                theme_input = st.text_input("Themes (e.g., hope, new hope, success,fire in the belly)", value="", placeholder="Enter themes separated by commas", key="theme_input")
            with col2:
                num_quotes = st.selectbox("Quotes per Theme", options=[1, 2, 3, 4, 5], index=0)
            with col3:
                quote_length = st.selectbox("Quote Length", options=["Short", "Medium", "Long"], index=1)
            submit_button = st.form_submit_button(label="Generate Quotes")

    # Results
    if submit_button:
        if not theme_input.strip():
            st.error("Please enter at least one theme.")
            return
        
        if num_quotes < 1 or num_quotes > 5:
            st.error("Please select a number between 1 and 5.")
            return

        themes = [theme.strip().lower() for theme in theme_input.split(",") if theme.strip()]
        if not themes:
            st.error("No valid themes provided.")
            return

        # Map quote length to max_length
        length_map = {
            "Short": 40,
            "Medium": 60,
            "Long": 80
        }
        max_length = length_map[quote_length]

        with st.container():
            st.markdown("### Your Generated Quotes")
            try:
                for theme in themes:
                    st.markdown(f"#### Quotes for '{theme}'")
                    quotes = []
                    for i in range(num_quotes):
                        quote, author = generate_quote(theme, max_length=max_length)
                        quotes.append((quote, author))
                        save_quote(theme, quote, author)
                        st.markdown(
                            f"""
                            <div class="quote-card">
                                <div class="quote-text">"{quote}"</div>
                                <div class="quote-author">— {author}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                
                st.success("Quotes generated")
            except Exception as e:
                st.error(f"Error generating quotes: {str(e)}")

if __name__ == "__main__":
    main()