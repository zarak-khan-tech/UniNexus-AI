"""
English: Normalize the new backend error envelope {error: {message}} to the
legacy `detail` key so existing UI components don't break.
Roman Urdu: Naye backend error envelope {error: {message}} ko purane `detail` key
mein map karo taake frontend components break na hon.
"""
path = "src/api/client.js"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_interceptor = """      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);"""

new_interceptor = """      if (window.location.pathname !== '/login' && window.location.pathname !== '/register') {
        window.location.href = '/login';
      }
    }
    
    // English: Extract message from new error envelope to legacy `detail` for UI compatibility.
    // Roman Urdu: Naye error format se message nikal kar purane `detail` mein daalo taake UI break na ho.
    if (error.response?.data?.error?.message) {
      error.response.data.detail = error.response.data.error.message;
    }
    
    return Promise.reject(error);"""

if "error.response.data.detail = error.response.data.error.message" in content:
    print("SKIP: error normalization already present")
elif old_interceptor in content:
    content = content.replace(old_interceptor, new_interceptor, 1)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("FIXED: client.js updated to handle new error format")
else:
    print("ERROR: Axios interceptor anchor not found")
