"""
Marketing Campaign Agent using Google ADK
A multi-step CMO Agent that develops complete marketing campaigns.
"""

import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai.types import Blob

# Load environment variables from .env file
load_dotenv()


# ============================================================================
# STEP 1: Market Strategy Tool
# ============================================================================
def analyze_market_strategy(
    product_service: str,
    target_audience: str,
    key_differentiator: str
) -> Dict[str, Any]:
    """
    Analyzes market strategy including target audience insights, strategic approach, and key messaging.

    This tool performs comprehensive market analysis to develop a strategic marketing approach.

    Args:
        product_service: Description of the product or service being marketed
        target_audience: Description of the target audience demographics and psychographics
        key_differentiator: The unique value proposition that sets this offering apart

    Returns:
        Dictionary containing market analysis, strategy, and key messages
    """
    return {
        "status": "success",
        "step": "market_strategy_analysis",
        "instructions": f"""
Perform a comprehensive CMO-level market strategy analysis:

**Product/Service:** {product_service}
**Target Audience:** {target_audience}
**Key Differentiator:** {key_differentiator}

Provide detailed analysis in this format:

## AUDIENCE ANALYSIS:
- Core values of the target audience
- Key pain points they experience
- Media consumption habits and preferred channels
- Emotional drivers and motivations

## MARKETING STRATEGY:
- High-level strategic approach (give it a memorable name)
- Primary tactics to reach and engage the audience
- Positioning statement
- Expected outcomes

## KEY MESSAGE:
- The single, most powerful message that will drive conversion
- Why this message will resonate (one sentence)

Be specific, strategic, and persuasive. Focus on deep psychological insights.
"""
    }


# ============================================================================
# STEP 2: Tagline Generation Tool
# ============================================================================
def generate_taglines(
    product_service: str,
    target_audience: str,
    key_differentiator: str,
    strategy_context: str = ""
) -> Dict[str, Any]:
    """
    Generates five compelling taglines with psychological justifications.

    This tool creates memorable, emotionally resonant taglines suitable for digital advertising.

    Args:
        product_service: Description of the product or service
        target_audience: Description of the target audience
        key_differentiator: The unique value proposition
        strategy_context: Previous strategy insights to inform tagline creation

    Returns:
        Instructions for generating 5 distinct taglines with justifications
    """
    return {
        "status": "success",
        "step": "tagline_generation",
        "instructions": f"""
Generate EXACTLY 5 distinct, compelling taglines for this campaign:

**Product/Service:** {product_service}
**Target Audience:** {target_audience}
**Key Differentiator:** {key_differentiator}
**Strategy Context:** {strategy_context}

For each tagline, provide:
1. The tagline itself (short, memorable, 3-8 words)
2. A one-sentence psychological justification

Format your response EXACTLY as:

TAGLINE 1: [Your tagline]
JUSTIFICATION: [Why it works psychologically]

TAGLINE 2: [Your tagline]
JUSTIFICATION: [Why it works psychologically]

TAGLINE 3: [Your tagline]
JUSTIFICATION: [Why it works psychologically]

TAGLINE 4: [Your tagline]
JUSTIFICATION: [Why it works psychologically]

TAGLINE 5: [Your tagline]
JUSTIFICATION: [Why it works psychologically]

Make each unique, emotionally resonant, and action-oriented.
"""
    }


# ============================================================================
# STEP 3: Visual Concept Development Tool
# ============================================================================
def develop_visual_concept(
    product_service: str,
    target_audience: str,
    tagline: str = "",
    all_taglines: str = ""
) -> Dict[str, Any]:
    """
    Develops a detailed visual brief for campaign image generation.

    This tool creates comprehensive visual specifications for high-impact advertisements.

    Args:
        product_service: Description of the product or service
        target_audience: Description of the target audience
        tagline: The selected tagline (if already chosen)
        all_taglines: All available taglines to choose from (if selection needed)

    Returns:
        Detailed visual brief with style, subject, setting, colors, composition
    """
    selection_text = ""
    if all_taglines and not tagline:
        selection_text = f"""
**Available Taglines:**
{all_taglines}

First, SELECT the single best tagline from the list above.
"""
    elif tagline:
        selection_text = f"**Selected Tagline:** {tagline}"

    return {
        "status": "success",
        "step": "visual_concept_development",
        "instructions": f"""
You are a Creative Director developing a visual concept for an advertisement.

**Product/Service:** {product_service}
**Target Audience:** {target_audience}
{selection_text}

Develop a detailed Visual Brief for image generation with these sections:

**STYLE:** Describe the visual style (cinematic, minimalist, photorealistic, vibrant, soft lighting, dramatic, etc.)

**SUBJECT:** Describe the main subject in detail - what they're doing, expression, positioning

**SETTING:** Describe the environment, location, background, lighting conditions

**COLOR PALETTE:** Specify dominant colors and mood (warm neutrals, vibrant greens, cool blues, etc.)

**COMPOSITION:** Describe framing, perspective, visual hierarchy

**MOOD & EMOTION:** The emotional tone the image should convey

Be extremely detailed and specific - this will be used for image generation.
"""
    }


# ============================================================================
# STEP 4: Image Generation Tool (using Imagen 4)
# ============================================================================
def generate_campaign_image(
    tool_context: ToolContext,
    visual_brief: str,
    image_prompt: str = ""
) -> Dict[str, Any]:
    """
    Generates the final campaign image using Imagen API.

    This tool creates a high-quality marketing image based on detailed specifications,
    saves it to the output directory, and returns status information.

    Args:
        tool_context: ADK tool context for saving artifacts
        visual_brief: Detailed visual specifications from the creative director
        image_prompt: Optional additional prompt details for image generation

    Returns:
        Dictionary containing status, image path, and generation details
    """
    try:
        # Import Imagen generation capabilities
        from google import genai
        from google.genai import types
        from PIL import Image
        from io import BytesIO
        from datetime import datetime

        # Get API key
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            return {
                "status": "error",
                "message": "GOOGLE_API_KEY not found in environment variables",
                "instructions": "Please set GOOGLE_API_KEY to use image generation"
            }

        # Initialize client
        client = genai.Client(api_key=api_key)

        # Prepare the image prompt
        final_prompt = visual_brief
        if image_prompt:
            final_prompt = f"{visual_brief}\n\nAdditional Details: {image_prompt}"

        # Create a comprehensive, marketing-focused prompt for Imagen
        imagen_prompt = f"""
Create a PROFESSIONAL MARKETING CAMPAIGN IMAGE that is ready for immediate commercial use:

{final_prompt}

CRITICAL REQUIREMENTS FOR MARKETING EXCELLENCE:

PROFESSIONAL SETTING & ENVIRONMENT:
- Shot in a professional studio or controlled environment with professional photography setup
- Clean, organized, and purposefully designed setting appropriate for the brand
- Professional backdrop or location that enhances the product narrative
- Polished, high-end environment that conveys quality and sophistication
- Setting should appear intentional, not casual or amateur
- Studio-grade professional atmosphere throughout

PROFESSIONAL LIGHTING SETUP:
- Professional multi-point lighting setup (key light, fill light, rim/hair light)
- Soft, diffused lighting using professional softboxes or umbrellas
- No harsh shadows - perfectly balanced illumination
- Key light positioned at 45-degree angle for dimensional depth
- Fill light to soften shadows without eliminating them completely
- Rim or back lighting to separate subject from background
- Color temperature consistent throughout (typically 5500K daylight balanced)
- Professional-grade lighting that flatters both models and product equally
- Catchlights visible in model's eyes for life and engagement
- Product has dedicated lighting to showcase texture, details, and quality
- Studio lighting that creates a premium, high-end commercial look

HUMAN ELEMENT & MODELS:
- Feature attractive, professional models interacting naturally with the product
- Models should be diverse, relatable, and aspirational to the target audience
- Genuine, authentic expressions showing joy, satisfaction, or engagement with the product
- Models should demonstrate the product in use, highlighting its benefits and lifestyle appeal
- Professional modeling quality with confident, natural poses
- Models should complement the product without overshadowing it
- Capture authentic moments of connection between people and the product
- Professional hair, makeup, and wardrobe styling

PRODUCT VISIBILITY & FOCUS:
- The actual product/service must be clearly visible and prominently featured
- Product should be shown in the model's hands, being used, or prominently placed in scene
- Dedicated product lighting highlighting details, texture, and quality
- Show the product delivering value or solving a problem in a lifestyle context
- Ensure product details, quality, and benefits are visually evident through usage
- The product and model(s) should work together to tell a compelling story
- Product positioned to catch optimal light and show its best features

PROFESSIONAL PHOTOGRAPHY QUALITY:
- Shot with professional DSLR or medium format camera aesthetic
- Sharp focus with appropriate depth of field (f/2.8 to f/5.6 range)
- Bokeh effect on background when appropriate for subject isolation
- Impeccable composition following rule of thirds and visual hierarchy
- Professional color accuracy and white balance
- Studio-quality sharpness and clarity throughout
- No grain, noise, or compression artifacts
- Professional post-production color grading

MARKETING APPEAL:
- Instantly eye-catching and scroll-stopping visual impact
- Evokes strong emotional response aligned with brand message
- Aspirational and desirable presentation that viewers want to emulate
- Shows the lifestyle and transformation the product enables
- Creates emotional connection through human presence and authentic moments
- Clean, uncluttered composition that directs attention to the product-person interaction
- Premium brand aesthetic throughout

COMMERCIAL READINESS:
- Suitable for immediate use in digital ads, social media, and print campaigns
- Professional color grading with vibrant but realistic tones
- High resolution and commercial production value
- No text or overlays (will be added separately)
- Background complements the scene without competing for attention
- Magazine-quality editorial and advertising aesthetic
- Ready for billboards, digital ads, social media, and print media

TECHNICAL SPECIFICATIONS:
- 16:9 aspect ratio, landscape orientation
- Photorealistic rendering with commercial photography quality
- Balanced exposure with rich colors and contrast
- Professional retouching quality on both models and product
- Studio photography standards throughout

Create an image that looks like it was shot in a professional photography studio with a full lighting crew, professional models, and commercial-grade equipment. The viewer should immediately recognize this as a premium, professional marketing photograph that makes them connect emotionally with the product and desire to own it.
"""

        # Truncate if too long (Imagen has token limits)
        if len(imagen_prompt) > 2000:
            imagen_prompt = imagen_prompt[:1900] + "\n\nHigh-quality professional marketing image."

        print(f"\n🎨 Generating image with Imagen...")
        print(f"   Prompt length: {len(imagen_prompt)} characters")

        # Generate image using Imagen - minimal config (v5 working approach)
        response = client.models.generate_images(
            model='imagen-4.0-generate-preview-06-06',
            prompt=imagen_prompt
        )

        # Save the generated image
        if response.generated_images and len(response.generated_images) > 0:
            generated_image = response.generated_images[0]

            # Create output directory if it doesn't exist
            output_dir = "output"
            os.makedirs(output_dir, exist_ok=True)

            # Save image with timestamp to avoid overwriting
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_filename = f"campaign_image_{timestamp}.png"
            image_path = os.path.join(output_dir, image_filename)

            # Get image bytes
            image_bytes = generated_image.image.image_bytes

            # Convert bytes to PIL Image and save locally
            image = Image.open(BytesIO(image_bytes))
            image.save(image_path, format='PNG')

            print(f"   ✓ Image saved to: {image_path}")

            # Save as ADK artifact for download
            try:
                artifact_blob = Blob(mime_type="image/png", data=image_bytes)
                tool_context.save_artifact(filename=image_filename, artifact=artifact_blob)
                print(f"   ✓ Image artifact saved for download")
            except Exception as artifact_error:
                print(f"   ⚠ Could not save artifact: {artifact_error}")

            # Get image info
            width, height = image.size
            file_size = os.path.getsize(image_path)

            # Return success status with image details
            return {
                "status": "success",
                "step": "image_generation_complete",
                "image_path": image_path,
                "image_filename": image_filename,
                "dimensions": f"{width}x{height}",
                "file_size_kb": f"{file_size / 1024:.1f}",
                "message": (
                    f"✅ Campaign image successfully generated!\n\n"
                    f"📊 **Image Details:**\n"
                    f"• Dimensions: {width}x{height} pixels\n"
                    f"• File Size: {file_size / 1024:.1f} KB\n"
                    f"• Saved to: `{image_path}`\n"
                    f"• Artifact available for download: `{image_filename}`\n\n"
                    f"🎨 **The high-quality marketing image has been generated and saved.**\n"
                    f"You can find the image file in the output directory for use in your marketing campaign."
                )
            }
        else:
            return {
                "status": "error",
                "step": "image_generation_failed",
                "message": "❌ No images were generated by Imagen. Try refining the visual brief or check API quotas."
            }

    except ImportError as e:
        return {
            "status": "error",
            "step": "import_error",
            "message": (
                f"❌ Failed to import required libraries: {str(e)}\n\n"
                f"Please install: pip install google-genai Pillow"
            )
        }
    except Exception as e:
        error_msg = str(e)
        print(f"   ✗ Error generating image: {error_msg}")

        return {
            "status": "error",
            "step": "image_generation_error",
            "error": error_msg,
            "message": (
                f"❌ Image generation failed: {error_msg}\n\n"
                f"This may be due to API quotas, billing setup, or prompt content. "
                f"Check Google Cloud Console for details.\n\n"
                f"**Note:** The campaign can still be completed without the image. "
                f"The visual brief provides detailed specifications for manual creation."
            )
        }


# ============================================================================
# STEP 5: Campaign Report Generation Tool
# ============================================================================
def generate_campaign_report(
    product_service: str,
    target_audience: str,
    key_differentiator: str,
    strategy: str = "",
    taglines: str = "",
    visual_concept: str = "",
    image_status: str = ""
) -> Dict[str, Any]:
    """
    Generates the final comprehensive marketing campaign report.

    This tool compiles all campaign artifacts into a professional deliverable.

    Args:
        product_service: Product/service description
        target_audience: Target audience description
        key_differentiator: Unique value proposition
        strategy: Market strategy analysis
        taglines: Generated taglines with justifications
        visual_concept: Visual brief and concept
        image_status: Status of image generation

    Returns:
        Complete campaign report in markdown format
    """
    return {
        "status": "success",
        "step": "report_generation",
        "instructions": f"""
Generate a comprehensive Final Marketing Campaign Report:

# Marketing Campaign - Final Deliverable

## Campaign Brief
**Product/Service:** {product_service}
**Target Audience:** {target_audience}
**Key Differentiator:** {key_differentiator}

## Step 1: Market Strategy
{strategy if strategy else "[To be filled with strategy analysis]"}

## Step 2: Taglines Generated
{taglines if taglines else "[To be filled with 5 taglines and justifications]"}

## Step 3: Selected Concept & Visual Brief
{visual_concept if visual_concept else "[To be filled with selected tagline and visual brief]"}

## Step 4: Campaign Image
{image_status if image_status else "[Image generation status]"}

## Summary & Next Steps
Provide a professional summary and actionable next steps for deploying this campaign.

Format this as a polished, executive-ready marketing campaign deliverable.
"""
    }


# ============================================================================
# ROOT AGENT DEFINITION
# ============================================================================
root_agent = Agent(
    name="marketing_campaign_agent",
    model="gemini-2.5-flash",
    description="Expert Chief Marketing Officer Agent that develops complete marketing campaigns through a systematic four-step process with Imagen 4 image generation",
    instruction="""
You are an expert Chief Marketing Officer (CMO) with 20+ years of experience in strategic marketing and campaign development.

Your role is to guide users through a complete marketing campaign creation process:

**YOUR SYSTEMATIC PROCESS:**

1️⃣ **MARKET STRATEGY** 
   - Use analyze_market_strategy tool with the product, audience, and differentiator
   - Develop comprehensive audience insights and strategic positioning
   - Extract the key message that will drive the campaign

2️⃣ **TAGLINE GENERATION** 
   - Use generate_taglines tool with the campaign details and strategy insights
   - Create 5 distinct, emotionally resonant taglines
   - Provide psychological justification for each

3️⃣ **VISUAL CONCEPT** 
   - Use develop_visual_concept tool with all taglines
   - Select the single best tagline based on strategic fit
   - Create detailed visual specifications (style, subject, setting, colors, composition, mood)

4️⃣ **IMAGE GENERATION** 
   - Use generate_campaign_image tool with the complete visual brief
   - This will automatically generate a high-quality marketing image using Imagen 4
   - The image will be saved to the output/ directory
   - If generation fails, note the visual specifications for manual creation

5️⃣ **FINAL REPORT** 
   - Use generate_campaign_report tool with all gathered information
   - Compile strategy, taglines, visual concept, and image details
   - Provide executive summary and next steps

**IMPORTANT GUIDELINES:**

- Execute ALL steps sequentially - each builds on the previous
- Be strategic, persuasive, and professional in your analysis
- Focus on deep psychological insights and emotional resonance
- Provide specific, actionable, data-driven recommendations
- The generate_campaign_image tool will handle actual Imagen 4 API calls
- If image generation encounters issues, explain the visual brief can be used manually
- Always compile a comprehensive final report as the deliverable

**TONE & STYLE:**

- Professional CMO-level strategic thinking
- Persuasive and confident recommendations
- Backed by psychological and marketing principles
- Clear, executive-ready communication

**USER INTERACTION:**

When the user provides a campaign brief (product, audience, differentiator), automatically execute all 5 steps in sequence and deliver a complete campaign package with a generated image.

Be thorough, insightful, and deliver executive-level marketing strategy with tangible creative assets.
""",
    tools=[
        analyze_market_strategy,
        generate_taglines,
        develop_visual_concept,
        generate_campaign_image,
        generate_campaign_report
    ]
)
