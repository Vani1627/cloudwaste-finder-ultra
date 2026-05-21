import streamlit as st
import boto3
import pandas as pd
import requests

# ----------------------------------------------------
# 1. CORE CONFIGURATION & STYLING OVERRIDES
# ----------------------------------------------------
st.set_page_config(
    page_title="CloudWaste Finder Ultra", 
    page_icon="💸", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End SaaS Styling Overrides
st.markdown("""
    <style>
        /* Modern soft background gradient for the main workspace */
        .stApp {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        }
        
        /* Sidebar Obsidian Theme & Explicit Text Overrides */
        section[data-testid="stSidebar"] {
            background-color: #0f172a !important;
            border-right: 1px solid #334155;
        }
        section[data-testid="stSidebar"] .stMarkdown, 
        section[data-testid="stSidebar"] h3, 
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] label {
            color: #f8fafc !important;
        }
        div[data-testid="stSidebar"] div[role="radiogroup"] label p {
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* Premium Linear Gradient Heading */
        .premium-title {
            font-family: 'Inter', sans-serif;
            font-size: 42px;
            font-weight: 800;
            background: linear-gradient(135deg, #0f172a 0%, #0284c7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2px;
        }
        
        /* Metric Styling Overrides */
        div[data-testid="stMetricSimple"] {
            background: #ffffff !important;
            border: 1px solid #e2e8f0 !important;
            padding: 24px !important;
            border-radius: 16px !important;
            box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.04) !important;
            border-left: 6px solid #0284c7 !important;
        }
        div[data-testid="stMetricValue"] { font-size: 36px !important; font-weight: 700 !important; color: #0f172a !important; }
        div[data-testid="stMetricLabel"] { font-size: 12px !important; text-transform: uppercase !important; color: #64748b !important; }
        
        /* Clean Card Wrappers for Content Blocks */
        .dashboard-panel {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
            margin-bottom: 20px;
        }
        
        /* Centralized Login Container Card */
        .login-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05);
            max-width: 600px;
            margin: 40px auto;
        }
    </style>
""", unsafe_allow_html=True)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1242398457012355152/bA8x8Z9_fake_testing_url_for_demo_purposes"

# Initialize our page router session states if they don't exist yet
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'aws_keys' not in st.session_state:
    st.session_state.aws_keys = {}

# ----------------------------------------------------
# PAGE 1: THE GATEWAY SETUP SCREEN (AUTHENTICATION LOCKED)
# ----------------------------------------------------
if not st.session_state.authenticated:
    
    st.markdown("<div style='text-align: center; margin-top: 50px;'>", unsafe_allow_html=True)
    st.markdown('<h1 class="premium-title">CloudWaste Finder Ultra</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 16px;'>Welcome to the Enterprise FinOps System. Provide your isolated scope session credentials to begin scanning tracks.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Render centralized secure card configuration fields
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.subheader("🔐 Initialize Session Identity Track")
    
    auth_mode = st.radio(
        "Choose Infrastructure Access Path:",
        ["🔬 Use Sandbox Mock Data Mode", "🌐 Connect Live AWS Cloud Account"]
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Hide input text bars if user picks local simulation sandbox mode
    if auth_mode == "🌐 Connect Live AWS Cloud Account":
        access_id = st.text_input("AWS Access Key ID", type="password")
        secret_id = st.text_input("AWS Secret Access Key", type="password")
        token_id = st.text_input("AWS Session Token (Optional)", type="password")
    else:
        access_id, secret_id, token_id = "SANDBOX", "SANDBOX", ""

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Initialize Secure Scanner Connection", type="primary", use_container_width=True):
        if auth_mode == "🌐 Connect Live AWS Cloud Account" and (not access_id or not secret_id):
            st.error("❌ Configuration Error: Both Access Key and Secret Key components must be specified.")
        else:
            # Commit identity pointers to active browser session ram
            st.session_state.aws_keys = {
                'access': access_id,
                'secret': secret_id,
                'token': token_id,
                'mode': auth_mode
            }
            st.session_state.authenticated = True
            # Force trigger instantaneous screen router change execution
            st.rerun()
            
    st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------
# PAGE 2: THE MAIN ENTERPRISE ANALYTICS DASHBOARD
# ----------------------------------------------------
else:
    # Sidebar control elements panel block
    with st.sidebar:
        st.markdown("### 🛠️ Runtime Controls")
        st.caption(f"**Scope Path:** {st.session_state.aws_keys['mode']}")
        
        force_rescan = st.button("🔄 Trigger Real-time Cloud Query", type="primary", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Disconnect Action resets router state parameters back to blank login screens
        if st.button("🔒 Close Connected Session", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.aws_keys = {}
            if 'global_aws_db' in st.session_state:
                del st.session_state.global_aws_db
            st.rerun()

    # Dynamic Data Engine Sync Pipeline
    if 'global_aws_db' not in st.session_state or force_rescan:
        if st.session_state.aws_keys['mode'] == "🔬 Use Sandbox Mock Data Mode":
            st.session_state.global_aws_db = {
                'us-east-1 (N. Virginia)': [
                    {'Resource ID': 'vol-01a23bc45de678f90', 'Type': 'EBS Volume', 'Details': '100 GB', 'Monthly Waste ($)': 8.00},
                    {'Resource ID': 'i-0abcd1234efgh5678', 'Type': 'Zombie EC2 Server', 'Details': '0.8% Avg CPU', 'Monthly Waste ($)': 30.00},
                    {'Resource ID': 'snap-055de678f901a23bc', 'Type': 'Orphaned Snapshot', 'Details': '500 GB Backup', 'Monthly Waste ($)': 25.00}
                ],
                'eu-west-1 (Ireland)': [
                    {'Resource ID': 'vol-099999999ffffffaa', 'Type': 'EBS Volume', 'Details': '200 GB', 'Monthly Waste ($)': 16.00},
                    {'Resource ID': 'snap-088888888bbbbbbcc', 'Type': 'Orphaned Snapshot', 'Details': '1000 GB Backup', 'Monthly Waste ($)': 50.00}
                ]
            }
        else:
            status_container = st.sidebar.container()
            status_container.warning("🔄 Interrogating global cluster tracks...")
            
            live_scanned_data = {}
            try:
                base_ec2 = boto3.client(
                    'ec2', 
                    region_name='us-east-1',
                    aws_access_key_id=st.session_state.aws_keys['access'],
                    aws_secret_access_key=st.session_state.aws_keys['secret'],
                    aws_session_token=st.session_state.aws_keys['token'] if st.session_state.aws_keys['token'] else None
                )
                region_response = base_ec2.describe_regions()
                all_regions = [r['RegionName'] for r in region_response.get('Regions', [])]
                
                progress_bar = st.sidebar.progress(0.0)
                
                for index, region_code in enumerate(all_regions):
                    display_name = f"{region_code}"
                    live_scanned_data[display_name] = []
                    progress_bar.progress((index + 1) / len(all_regions))
                    
                    try:
                        ec2 = boto3.client(
                            'ec2', 
                            region_name=region_code,
                            aws_access_key_id=st.session_state.aws_keys['access'],
                            aws_secret_access_key=st.session_state.aws_keys['secret'],
                            aws_session_token=st.session_state.aws_keys['token'] if st.session_state.aws_keys['token'] else None
                        )
                        
                        real_vols = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
                        for v in real_vols.get('Volumes', []):
                            live_scanned_data[display_name].append({
                                'Resource ID': v['VolumeId'], 'Type': 'EBS Volume', 'Details': f"{v['Size']} GB", 'Monthly Waste ($)': float(v['Size'] * 0.08)
                            })
                        
                        real_snaps = ec2.describe_snapshots(OwnerIds=['self'])
                        for snap in real_snaps.get('Snapshots', []):
                            live_scanned_data[display_name].append({
                                'Resource ID': snap['SnapshotId'], 'Type': 'Orphaned Snapshot', 'Details': f"{snap['VolumeSize']} GB Backup", 'Monthly Waste ($)': float(snap['VolumeSize'] * 0.05)
                            })
                    except Exception:
                        del live_scanned_data[display_name]
                        continue
                
                status_container.empty()
                st.sidebar.success("🚀 Optimization scan complete.")
            except Exception as e:
                st.sidebar.error(f"Global Connection Failure: {str(e)}")
                live_scanned_data = {'us-east-1 (N. Virginia)': []}
                
            st.session_state.global_aws_db = live_scanned_data

    # Main Workspace Metrics Rendering Frame
    st.markdown('<h1 class="premium-title">💸 FinOps Insights Center</h1>', unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; font-size: 16px; margin-top: -5px;'>Active multi-region architecture cost leakage mapping metrics console.</p>", unsafe_allow_html=True)
    st.markdown("---")

    if not st.session_state.global_aws_db:
        st.warning("No tracking records returned. Check configuration roles and rerun scanner diagnostics.")
    else:
        sorted_regions = sorted(list(st.session_state.global_aws_db.keys()))
        col_select, col_empty = st.columns([2, 2])
        with col_select:
            selected_region = st.selectbox("🎯 Target Availability Zone Track:", sorted_regions)
        
        active_region_assets = st.session_state.global_aws_db[selected_region]

        if len(active_region_assets) > 0:
            df = pd.DataFrame(active_region_assets)
            total_waste = df['Monthly Waste ($)'].sum()
            yearly_waste = total_waste * 12
            asset_count = len(df)
            is_optimized = False
        else:
            total_waste, yearly_waste, asset_count = 0.0, 0.0, 0
            is_optimized = True

        # KPIs Grid Rows
        m_col1, m_col2, m_col3 = st.columns(3)
        with m_col1: st.metric(label="Monthly Burn Leakage", value=f"${total_waste:.2f}")
        with m_col2: st.metric(label="Annual Loss Trajectory", value=f"${yearly_waste:.2f}")
        with m_col3: st.metric(label="Identified Cost Anomalies", value=str(asset_count))
            
        st.markdown("<br>", unsafe_allow_html=True)

        if not is_optimized:
            chart_col, table_col = st.columns([2, 2], gap="large")
            with chart_col:
                st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
                st.markdown("<h4 style='margin-top:0; color:#0f172a;'>📊 Cost Weight Vectors</h4>", unsafe_allow_html=True)
                st.bar_chart(data=df, x="Resource ID", y="Monthly Waste ($)", color="#0284c7", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with table_col:
                st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
                st.markdown("<h4 style='margin-top:0; color:#0f172a;'>📋 Target Telemetry Logs</h4>", unsafe_allow_html=True)
                st.dataframe(df, use_container_width=True, hide_index=True)
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success(f"🎉 Core Victory! Availability node '{selected_region}' has no waste leaks.")

        # Lower Operations Command Module Panel
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("⚙️ Control Plane Console", divider="grey")
        action_col1, action_col2 = st.columns(2, gap="large")
        
        with action_col1:
            st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
            st.markdown("<h5 style='margin-top:0; color:#0f172a;'>🚀 Broadcast Incident Alerts</h5>", unsafe_allow_html=True)
            if st.button("📟 Broadcast Chat-Ops Payload Alert", use_container_width=True):
                if not is_optimized:
                    payload = {"content": f"🚨 **FinOps Alert!** Region: `{selected_region}` | Cost Trajectory: ${total_waste:.2f}/mo"}
                    try:
                        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=5)
                        st.success(f"✅ Transmitted. Code ({response.status_code}).")
                    except Exception:
                        st.info(f"📟 Mock Sent:\n```json\n{payload}\n```")
                else:
                    st.info("System optimized. Incident logs bypassed.")
            st.markdown('</div>', unsafe_allow_html=True)
                    
        with action_col2:
            st.markdown('<div class="dashboard-panel">', unsafe_allow_html=True)
            st.markdown("<h5 style='margin-top:0; color:#0f172a;'>🔥 Destructive API Purge Commands</h5>", unsafe_allow_html=True)
            if not is_optimized:
                target_to_purge = st.selectbox("Select Target Node for Complete Destruction:", df['Resource ID'].tolist())
                confirm_input = st.text_input("Verify clearance parameter by typing 'PURGE':")
                if st.button("🔥 Confirm Infrastructure Teardown Execution", type="primary", use_container_width=True):
                    if confirm_input == "PURGE":
                        st.session_state.global_aws_db[selected_region] = [i for i in active_region_assets if i['Resource ID'] != target_to_purge]
                        st.error(f"💥 Destroyed node: `{target_to_purge}`.")
                        st.rerun()
                    else:
                        st.warning("⚠️ Access Denied: Validation token input invalid.")
            else:
                st.info("🔒 Purge locks engaged. Operational profiles are clean.")
            st.markdown('</div>', unsafe_allow_html=True)