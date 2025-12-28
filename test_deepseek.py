"""Test DeepSeek API connection."""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from openai import OpenAI

print("=" * 60)
print("🔍 DeepSeek API Connection Test")
print("=" * 60)
print(f"API Key (last 4 chars): ...{settings.deepseek_api_key[-4:] if settings.deepseek_api_key else 'NOT SET'}")
print(f"API Base: {settings.deepseek_api_base}")
print(f"Model: {settings.deepseek_model}")
print("=" * 60)

if not settings.deepseek_api_key or settings.deepseek_api_key == "your_deepseek_api_key_here":
    print("❌ ERROR: DEEPSEEK_API_KEY not set in .env file!")
    print("\nPlease edit the .env file and add your DeepSeek API key:")
    print("DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx")
    sys.exit(1)

# Try different configurations
configs = [
    {"base": "https://api.deepseek.com", "model": "deepseek-chat"},
    {"base": "https://api.deepseek.com/v1", "model": "deepseek-chat"},
    {"base": "https://api.deepseek.com/beta", "model": "deepseek-chat"},
]

print(f"\n🧪 Testing {len(configs)} different configurations...\n")

for i, config in enumerate(configs, 1):
    print(f"Test {i}/{len(configs)}: {config['base']} + {config['model']}")
    try:
        client = OpenAI(
            api_key=settings.deepseek_api_key,
            base_url=config["base"]
        )

        response = client.chat.completions.create(
            model=config["model"],
            messages=[
                {"role": "user", "content": "Say hello in one word"}
            ],
            max_tokens=10,
            temperature=0.7
        )

        result = response.choices[0].message.content
        print(f"   ✅ SUCCESS! Response: {result}")
        print(f"\n{'='*60}")
        print(f"🎯 WORKING CONFIGURATION FOUND:")
        print(f"{'='*60}")
        print(f"DEEPSEEK_API_BASE={config['base']}")
        print(f"DEEPSEEK_MODEL={config['model']}")
        print(f"{'='*60}")
        print(f"\nUpdate your .env file with these values!")
        sys.exit(0)

    except Exception as e:
        error_msg = str(e)
        print(f"   ❌ FAILED: {error_msg[:100]}...")

print(f"\n{'='*60}")
print("❌ ALL TESTS FAILED")
print("{'='*60}")
print("\nPossible issues:")
print("1. The API key is invalid or expired")
print("2. The API key doesn't have proper permissions")
print("3. You need to activate your DeepSeek account")
print("\nVisit: https://platform.deepseek.com/ to check your API key")
