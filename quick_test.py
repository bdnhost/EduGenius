"""Quick DeepSeek API test without dependencies."""
import os

# Read .env file manually
env_vars = {}
try:
    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_vars[key] = value
except FileNotFoundError:
    print("❌ .env file not found!")
    exit(1)

api_key = env_vars.get('DEEPSEEK_API_KEY', '')
api_base = env_vars.get('DEEPSEEK_API_BASE', 'https://api.deepseek.com')
model = env_vars.get('DEEPSEEK_MODEL', 'deepseek-chat')

print("="*60)
print("🔍 Quick Deep Seek API Test")
print("="*60)
print(f"API Key (last 4): ...{api_key[-4:] if len(api_key) > 4 else 'INVALID'}")
print(f"API Base: {api_base}")
print(f"Model: {model}")
print("="*60)

if not api_key or api_key == 'your_deepseek_api_key_here':
    print("\n❌ ERROR: Invalid API key in .env file!")
    print("Please edit .env and set: DEEPSEEK_API_KEY=sk-xxxxxxxxx")
    exit(1)

# Manual HTTP request without OpenAI client
import urllib.request
import json

configs_to_try = [
    ("https://api.deepseek.com", "deepseek-chat"),
    ("https://api.deepseek.com/v1", "deepseek-chat"),
    ("https://api.deepseek.com/v1", "deepseek-coder"),
]

print("\n🧪 Testing different configurations...\n")

for i, (base_url, model_name) in enumerate(configs_to_try, 1):
    endpoint = f"{base_url}/chat/completions" if not base_url.endswith('/v1') else f"{base_url}/chat/completions"

    print(f"Test {i}/{len(configs_to_try)}: {base_url} + {model_name}")

    data = {
        "model": model_name,
        "messages": [{"role": "user", "content": "Say hello"}],
        "max_tokens": 10
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        req = urllib.request.Request(
            endpoint,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            message = result.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')
            print(f"   ✅ SUCCESS! Response: {message}")
            print(f"\n{'='*60}")
            print(f"🎯 WORKING CONFIGURATION:")
            print(f"{'='*60}")
            print(f"DEEPSEEK_API_BASE={base_url}")
            print(f"DEEPSEEK_MODEL={model_name}")
            print(f"{'='*60}\n")
            print("✅ Your API key is valid! Update .env with the above values.")
            exit(0)

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"   ❌ HTTP {e.code}: {error_body[:150]}")
    except Exception as e:
        print(f"   ❌ ERROR: {str(e)[:100]}")

print(f"\n{'='*60}")
print("❌ ALL CONFIGURATIONS FAILED")
print(f"{'='*60}")
print("\nPossible issues:")
print("1. API key is invalid, expired, or not activated")
print("2. DeepSeek API endpoint has changed")
print("3. Network/firewall blocking the request")
print("\n📌 Visit https://platform.deepseek.com/ to:")
print("   - Check your API key status")
print("   - Generate a new API key")
print("   - Check API documentation")
