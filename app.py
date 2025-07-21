# app.py
import streamlit as st
from src.agents.query_analysis import classify_query_type
from src.agents.vector_query import query_chromadb
from src.agents.graph_query import query_neo4j
from src.agents.response_synthesis import synthesize_response
import time
from pymongo import MongoClient
import os
import json
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="PDF Query System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "name"
COLLECTION_NAME = "chat_history"

# Initialize MongoDB client and collection
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.server_info()
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
except Exception as e:
    st.error(f"MongoDB connection failed: {e}")
    collection = None

# Initialize session state
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "last_query" not in st.session_state:
    st.session_state.last_query = None
if "processing_index" not in st.session_state:
    st.session_state.processing_index = -1

# Function to export conversation data
def export_conversation_data(format_type):
    data = []
    # session data
    for q, r in st.session_state.conversation:
        if r != "Processing...":
            data.append({
                "query": q,
                "response": r,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "source": "Session"
            })
    # database data
    if collection is not None:
        for entry in collection.find().sort("timestamp", -1):
            data.append({
                "query": entry["query"],
                "response": entry["response"],
                "timestamp": entry["timestamp"],
                "source": "Database"
            })
    if format_type == "JSON":
        return json.dumps(data, indent=2)
    elif format_type == "CSV":
        if not data:
            return ""
        lines = ["Query,Response,Timestamp,Source"]
        for item in data:
            q = item["query"].replace('"', '""').replace("\n", " ")
            r = item["response"].replace('"', '""').replace("\n", " ")
            lines.append(f'"{q}","{r}","{item["timestamp"]}","{item["source"]}"')
        return "\n".join(lines)
    return ""

# Custom CSS for Sidebar UI
st.markdown("""
    <style>
    /* Shrink DB status badge */
    .db-status-indicator { font-size: 0.7rem !important; padding: 0.2rem 0.5rem !important; }
    /* Shrink all sidebar buttons */
    .stSidebar .stButton > button { padding: 0.4rem 0.6rem; font-size: 0.8rem; }
    /* Clear History button color */
    .clear-history-container .stButton > button { background: linear-gradient(135deg, #f97316 0%, #ea580c 100%) !important; }
    </style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:1rem; border-radius:12px; text-align:center; margin-bottom:1rem;">
  <h1 style="color:white; margin:0;">📚 PDF Query System</h1>
  <p style="color:rgba(255,255,255,0.9); margin:0;">Intelligent Document Analysis with Vector & Graph Search</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.markdown(
    '<h3 style="text-align:center; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color:white; padding:0.6rem; border-radius:8px; margin-bottom:1rem;">Control Panel</h3>',
    unsafe_allow_html=True
)

# Database Status
db_text = "🟢 Connected" if collection is not None else "🔴 Disconnected"
st.sidebar.markdown(f"""
    <div style="border:1px solid #e2e8f0; padding:0.6rem; border-radius:8px; text-align:center; margin-bottom:1rem;">
      <div style="font-size:0.85rem; font-weight:600; color:#4a5568; margin-bottom:0.3rem;">Database Status</div>
      <span class="db-status-indicator">{db_text}</span>
    </div>
""", unsafe_allow_html=True)

# Export Conversations
export_format = st.sidebar.selectbox("Choose format:", ["JSON", "CSV"], help="Select export format")
if st.sidebar.button("Export Conversations", use_container_width=True):
    out = export_conversation_data(export_format)
    if out:
        st.sidebar.download_button(
            label=f"Download {export_format}",
            data=out,
            file_name=f"conversations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{export_format.lower()}",
            mime="application/json" if export_format == "JSON" else "text/csv",
            use_container_width=True
        )
        st.sidebar.success("✅ Ready to download!")
    else:
        st.sidebar.warning("⚠️ No data to export")

# Search + Recent Conversations (latest first)
if collection is not None:
    term = st.sidebar.text_input("🔍 Search History", placeholder="Enter search term...")
    with st.sidebar.expander("📚 Recent Conversations", expanded=True):
        # Separate session and database records
        session_recs = [(q, r, "Session") for q, r in reversed(st.session_state.conversation) if r != "Processing..."]
        db_recs = []
        for e in collection.find().sort("timestamp", -1).limit(8):
            if not any(q == e["query"] for q, _, _ in session_recs):
                db_recs.append((e["query"], e["response"], e["timestamp"]))
        # Combine with session first (newest on top)
        combined = session_recs + db_recs
        # Apply filter
        if term:
            combined = [(q, r, t) for q, r, t in combined if term.lower() in q.lower() or term.lower() in r.lower()]
        if combined:
            for q, r, t in combined:
                st.sidebar.markdown(f"**Q:** {q[:30]}...<br>**A:** {r[:30]}...<br><small>{t}</small><hr>", unsafe_allow_html=True)
        else:
            st.sidebar.markdown("📝 No conversations found.")
else:
    st.sidebar.error("❌ MongoDB not connected. History unavailable.")

# Clear History Button at bottom
st.sidebar.markdown('<div class="clear-history-container" style="margin-top:1rem;">', unsafe_allow_html=True)
if st.sidebar.button("Clear History", key="clear_history", use_container_width=True):
    st.session_state.conversation = []
    st.session_state.last_query = None
    st.session_state.processing_index = -1
    if collection is not None:
        collection.delete_many({})
    st.sidebar.success("✅ History cleared!")
    time.sleep(1)
    st.rerun()
st.sidebar.markdown('</div>', unsafe_allow_html=True)

# MAIN CONTENT
col1, col2 = st.columns([2, 1])
with col1:
    if st.session_state.conversation:
        total = len(st.session_state.conversation)
        processing = sum(1 for _, r in st.session_state.conversation if r == "Processing...")
        if processing:
            st.markdown(f"<div style='display:flex; gap:0.5rem;'><div style='flex:1;text-align:center;padding:0.3rem;border:1px solid #e2e8f0;border-radius:6px;'>📊 Total: {total}</div><div style='flex:1;text-align:center;padding:0.3rem;border:1px solid #e2e8f0;border-radius:6px;'>⏳ Processing: {processing}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='display:flex; gap:0.5rem;'><div style='flex:1;text-align:center;padding:0.3rem;border:1px solid #e2e8f0;border-radius:6px;'>📊 Total: {total}</div><div style='flex:1;text-align:center;padding:0.3rem;border:1px solid #e2e8f0;border-radius:6px;'>✅ Complete: {total}</div></div>", unsafe_allow_html=True)
        for i, (q, r) in enumerate(st.session_state.conversation):
            if r == "Processing..." and i == st.session_state.processing_index:
                st.markdown(f"<div style='padding:1rem;border:1px solid #e2e8f0;border-radius:12px;margin-bottom:0.75rem;'><strong>💭 {q}</strong><div style='font-style:italic;margin-top:0.5rem;'>⏳ Processing your request...</div></div>", unsafe_allow_html=True)
                pb = st.progress(0)
                statuses = ["🔍 Analyzing...", "📚 Vector DB...", "🕸️ Graph DB...", "🤖 Synthesizing..."]
                for pct in range(100):
                    time.sleep(0.01)
                    pb.progress(pct + 1)
                    if pct % 25 == 0:
                        st.write(statuses[pct // 25])
            else:
                st.markdown(f"<div style='padding:1rem;border:1px solid #e2e8f0;border-radius:12px;margin-bottom:0.75rem;'><strong>💭 {q}</strong><div style='margin-top:0.5rem;'>🤖 {r}</div></div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='text-align:center;padding:2rem;color:#4a5568;'>🤖 Ready to Answer Your Questions!<br>Start by entering a query on the right.</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div style='padding:0.6rem;border:1px solid #e2e8f0;border-radius:12px;margin-bottom:1rem;'><h4 style='text-align:center;background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;'>✨ Ask Your Question</h4></div>", unsafe_allow_html=True)
    with st.form(key="query_form", clear_on_submit=True):
        query = st.text_input("Enter your query:", key="query_input", placeholder="What would you like to know?")
        submitted = st.form_submit_button("🚀 Submit Query", type="primary", use_container_width=True)
        if submitted and query and query != st.session_state.last_query:
            st.session_state.conversation.append((query, "Processing..."))
            st.session_state.last_query = query
            st.session_state.processing_index = len(st.session_state.conversation) - 1
            st.rerun()

# PROCESSING LOGIC
if st.session_state.conversation and st.session_state.processing_index >= 0:
    last_q, _ = st.session_state.conversation[st.session_state.processing_index]
    if st.session_state.conversation[st.session_state.processing_index][1] == "Processing...":
        try:
            classify = classify_query_type(last_q)
            vec_results = query_chromadb(last_q)[:3]
            graph_results = query_neo4j(last_q)[:5]
            resp = synthesize_response(last_q, vec_results, graph_results)
            if collection is not None:
                collection.insert_one({"query": last_q, "response": resp, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        except Exception as e:
            resp = f"❌ Error: {e}"
            if collection is not None:
                collection.insert_one({"query": last_q, "response": resp, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        st.session_state.conversation[st.session_state.processing_index] = (last_q, resp)
        st.session_state.processing_index = -1
        st.rerun()

# FOOTER
st.markdown("---")
st.markdown("<div style='text-align:center;color:#64748b;font-size:0.8rem;padding:0.5rem;'>🚀 Powered by Advanced RAG Technology | 📊 Vector + Graph Search</div>", unsafe_allow_html=True)
