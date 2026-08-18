import os
from dotenv import load_dotenv

load_dotenv()

# ==================================================
# LLM CONFIGURATION
# ==================================================

PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()

if PROVIDER == "gemini":

    from langchain_google_genai import ChatGoogleGenerativeAI

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        raise ValueError(
            "GOOGLE_API_KEY not found in environment variables"
        )

    llm = ChatGoogleGenerativeAI(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash"
        ),
        google_api_key=GOOGLE_API_KEY,
        temperature=0.7,
    )

else:

    from langchain_ollama import ChatOllama

    llm = ChatOllama(
        model=os.getenv(
            "OLLAMA_MODEL",
            "mistral:7b"
        ),
        temperature=0.7,
    )


# ==================================================
# COMPANY CONFIGURATION
# ==================================================

COMPANY_NAME = os.getenv(
    "COMPANY_NAME",
    "BlogGPT"
)

WEBSITE_URL = os.getenv(
    "WEBSITE_URL",
    "https://bloggpt.com"
)

LINKEDIN_URL = os.getenv(
    "LINKEDIN_URL",
    "https://linkedin.com/company/bloggpt"
)

TWITTER_URL = os.getenv(
    "TWITTER_URL",
    "https://x.com/bloggpt"
)

FACEBOOK_URL = os.getenv(
    "FACEBOOK_URL",
    "https://facebook.com/bloggpt"
)

UNSUBSCRIBE_URL = os.getenv(
    "UNSUBSCRIBE_URL",
    "https://bloggpt.com/unsubscribe"
)


# ==================================================
# GENERIC LLM CALL
# ==================================================

def ask(prompt: str) -> str:

    try:
        print("\nRunning prompt...")

        response = llm.invoke(prompt)

        if hasattr(response, "content"):
            return response.content

        return str(response)

    except Exception as e:
        return f"ERROR: {str(e)}"


# ==================================================
# SEO GENERATION
# ==================================================

def generate_seo(topic):

    return ask(
        f"""
Create a complete SEO package for:

{topic}

Include:

1. SEO Title
2. Meta Title
3. Meta Description
4. Primary Keyword
5. Secondary Keywords
6. URL Slug
7. Internal Linking Ideas
8. Image Alt Text Suggestions
9. Suggested Hashtags
"""
    )


# ==================================================
# OUTLINE GENERATION
# ==================================================

def generate_outline(topic, seo):

    return ask(
        f"""
Create a detailed SEO-friendly blog outline.

Topic:
{topic}

SEO Context:
{seo}

Include:

- Introduction
- H2 Sections
- H3 Sections
- FAQs
- Conclusion
"""
    )


# ==================================================
# BLOG GENERATION
# ==================================================

def generate_blog(topic, outline):

    return ask(
        f"""
Write a professional 2000-word blog.

Topic:
{topic}

Outline:
{outline}

Requirements:

- SEO optimized
- H2 and H3 headings
- Engaging introduction
- Actionable insights
- Real examples
- Bullet points
- Strong conclusion
- Call to action
"""
    )


# ==================================================
# FAQ GENERATION
# ==================================================

def generate_faq(blog):

    return ask(
        f"""
Create 10 FAQs and answers from:

{blog[:5000]}
"""
    )


# ==================================================
# LINKEDIN GENERATION
# ==================================================

def generate_linkedin(blog):

    return ask(
        f"""
Create a LinkedIn post from:

{blog[:5000]}

Include:

- Hook
- Key insights
- CTA
- Relevant hashtags
"""
    )


# ==================================================
# NEWSLETTER GENERATION
# ==================================================

def generate_newsletter(blog):

    newsletter = ask(
        f"""
Create a professional newsletter from:

{blog[:5000]}

Include:

- Subject Line
- Preview Text
- Executive Summary
- Key Takeaways
- Call To Action

Use markdown formatting.
"""
    )

    footer = f"""

---

### Connect With Us

💼 LinkedIn  
{LINKEDIN_URL}

🐦 X (Twitter)  
{TWITTER_URL}

📘 Facebook  
{FACEBOOK_URL}

🌐 Website  
{WEBSITE_URL}

📩 Unsubscribe  
{UNSUBSCRIBE_URL}

**The {COMPANY_NAME} Team**
"""

    return newsletter + footer


# ==================================================
# MAIN PIPELINE
# ==================================================

def run_pipeline(topic):

    print("Generating SEO...")
    seo = generate_seo(topic)

    print("Generating Outline...")
    outline = generate_outline(
        topic,
        seo
    )

    print("Generating Blog...")
    blog = generate_blog(
        topic,
        outline
    )

    print("Generating FAQ...")
    faq = generate_faq(blog)

    print("Generating LinkedIn...")
    linkedin = generate_linkedin(blog)

    print("Generating Newsletter...")
    newsletter = generate_newsletter(blog)

    return {
        "SEO": seo,
        "Outline": outline,
        "Blog": blog,
        "FAQ": faq,
        "LinkedIn": linkedin,
        "Newsletter": newsletter,
    }