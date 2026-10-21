
import streamlit as st
from pathlib import Path
import re
import ollama

st.set_page_config(
    page_title="NovaTech Support",
    page_icon="💬",
    layout="centered"
)
# NovaTech Support - Modern Light Theme
st.markdown("""
            


<style>

    /* Main application background */
    .stApp {
        background-color: #F8FAFC;
        color: #1E293B;
    }

    /* Main heading */
    h1 {
        color: #1D4ED8;
        font-weight: 700;
    }

    /* Sidebar background */
    [data-testid="stSidebar"] {
        background-color: #EFF6FF;
    }

    /* Rounded buttons */
    .stButton > button {
        border-radius: 12px;
        border: 1px solid #DBEAFE;
        background-color: #FFFFFF;
        color: #1D4ED8;
    }

    /* Button hover effect */
    .stButton > button:hover {
        background-color: #DBEAFE;
        border-color: #2563EB;
        color: #1D4ED8;
    }

    /* All chat messages */
    [data-testid="stChatMessage"] {
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }

    /* Customer messages - light blue */
    [data-testid="stChatMessage"][aria-label="Chat message from user"] {
        background-color: #DBEAFE !important;
        border: 1px solid #BFDBFE !important;
    }

    /* AI messages - white */
    [data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* Readable chat text */
    [data-testid="stChatMessage"] p {
        color: #1E293B !important;
        line-height: 1.6;
    }

</style>
""", unsafe_allow_html=True)

# Professional NovaTech header
st.markdown("""
<div style="
    background: white;
    padding: 24px;
    border-radius: 18px;
    border: 1px solid #E2E8F0;
    margin-bottom: 20px;
">
    <div style="display: flex; align-items: center; gap: 15px;">
        <div style="
            background: #DBEAFE;
            padding: 14px;
            border-radius: 14px;
            font-size: 28px;
        ">
            🤖
        </div>
        <div>
            <h2 style="margin: 0; color: #1E3A8A;">
                NovaTech Support
            </h2>
            <p style="margin: 4px 0 0; color: #64748B;">
                Your intelligent shopping assistant
            </p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    "Welcome to **NovaTech Store**! "
    "Ask me about shipping, returns, refunds, products, or payments."
)

with st.sidebar:

    # Sidebar heading
    st.markdown("### 🤖 NovaTech AI")
    st.caption("Smart customer support")
    st.divider()

    # AI Status
    st.subheader("AI Status")

    try:
        ollama.list()
        st.success("🟢 AI Connected")
    except Exception:
        st.error("🔴 AI Offline")

    st.divider()

    # Help Center
    st.header("Help Center")
    st.write("You can ask about:")

    st.markdown(
        "- 📦 Shipping and delivery\n"
        "- ↩️ Returns\n"
        "- 💰 Refunds\n"
        "- 💻 Products\n"
        "- 💳 Payments"
    )

    st.divider()

    # Clear Chat Button
    if st.button("🗑️ Clear chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hello! 👋 Welcome to NovaTech Store. "
                    "I'm your AI customer support assistant. "
                    "How can I help you today?"
                )
            }
        ]

        st.session_state.budget = None
        st.rerun()
# Load the knowledge base
file_path = Path(__file__).parent / "knowledge_base.txt"

if not file_path.exists():
    st.error("Cannot find knowledge_base.txt. Check your project folder.")
    st.stop()

knowledge = file_path.read_text(encoding="utf-8")


# Search the knowledge base

def search_knowledge(question):
    question = question.lower().strip()
    
    
    # Handle gaming laptop budget and game preferences
    if "budget" in question or "gta" in question or "valorant" in question:
        games = []

        if "gta" in question:
            games.append("GTA V")

        if "valorant" in question:
            games.append("Valorant")

        game_text = ", ".join(games) if games else "your games"
        budget_match = re.search(
            r"rs\.?\s*([\d,]+)",
            question
        )

        budget_text = "a budget that you haven't specified"

        if budget_match:
            budget = int(budget_match.group(1).replace(",", ""))
            budget_text = f"Rs. {budget:,}"

            return (
            f"Thanks for sharing your preferences! Your budget is "
            f"{budget_text}. For {game_text}, look for a laptop "
            "with at least 16 GB RAM, an SSD, and a suitable "
            "graphics card. The best choice depends on the exact "
            "model and its specifications. Please confirm current "
            "prices and stock with our support team."
        )



    policies = {
        "RETURN POLICY": [
            "return", "returned", "returning", "exchange",
            "send back", "send it back", "send my product back",
            "send the product back", "send my item back",
            "send the item back", "don't want it",
            "do not want it", "no longer want it"
        ],
        "PRODUCTS": [
            "product", "products", "sell", "laptop", "laptops",
            "headphones", "charger", "chargers",
            "mobile accessories"
        ],
        "SHIPPING POLICY": [
            "shipping", "delivery", "deliver", "arrive",
            "package", "parcel", "how long", "how many days",
            "expect it", "when will my order"
        ],
        "REFUND POLICY": [
            "refund", "money back", "reimbursement",
            "returned my", "return my money",
            "get my money", "when will i get my money"
        ],
        "PAYMENT POLICY": [
            "payment", "pay", "checkout", "card"
        ],
        "CUSTOMER SUPPORT": [
            "support", "help", "contact", "customer service"
        ]
    }

    # 1. Check refund questions BEFORE general return questions
    refund_keywords = [
        "refund", "money back", "reimbursement",
        "returned my", "get my money", "return my money"
    ]

    if any(word in question for word in refund_keywords):
        matched_heading = "REFUND POLICY"

    # 2. Check product availability
        # Handle product recommendation questions
    recommendation_phrases = [
        "recommend",
        "which laptop",
        "best laptop",
        "suggest a laptop",
        "gaming laptop for me"
    ]

    if any(phrase in question for phrase in recommendation_phrases):
        return (
            "I'd be happy to help you choose a gaming laptop! "
            "What's your budget, and which games do you want to play? "
            "I can help you identify suitable specifications. "
            "Please confirm specific models, prices, and stock "
            "availability with our support team."
        )
    elif any(word in question for word in [
        "in stock", "available", "availability",
        "do you have", "is there a"
    ]):
        if "laptop" in question:
            return (
                "We sell laptops at NovaTech Store! "
                "However, I can't confirm current stock availability. "
                "Please contact our support team to check "
                "whether a laptop is currently available."
            )

        return (
            "I can't confirm current stock availability. "
            "Please contact our support team to check "
            "whether the product is available."
        )

    # 3. Match other questions to a policy section
    else:
        matched_heading = None

        for heading, keywords in policies.items():
            if any(word in question for word in keywords):
                matched_heading = heading
                break

    if matched_heading is None:
        return (
            "I couldn't find that information in our knowledge base. "
            "Please contact customer support."
        )

    # 4. Give clear answers for the matched policy
    if matched_heading == "REFUND POLICY":
        return (
            "Once your returned item has been inspected, "
            "an approved refund will be sent to your original "
            "payment method. Processing times may vary."
        )

    if matched_heading == "RETURN POLICY":
        return (
            "You can request a return within 14 days of delivery. "
            "Items must be unused and in their original packaging. "
            "Some products may be excluded."
        )

    # 5. Find the matching section in the knowledge base
    lines = knowledge.splitlines()
    section_lines = []
    collecting = False

    section_headings = [
        "ABOUT", "PRODUCTS", "SHIPPING POLICY",
        "RETURN POLICY", "REFUND POLICY",
        "PAYMENT POLICY", "CUSTOMER SUPPORT"
    ]

    for line in lines:
        clean_line = line.strip().rstrip(":").upper()

        if clean_line == matched_heading:
            collecting = True
            continue

        if collecting and clean_line in section_headings:
            break

        if collecting:
            section_lines.append(line)

    result = "\n".join(section_lines).strip()

    if matched_heading == "SHIPPING POLICY":
        delay_phrases = [
            "hasn't arrived", "has not arrived", "not arrived",
            "late", "delayed", "where is my order",
            "where is my package", "still waiting"
        ]

        if any(phrase in question for phrase in delay_phrases):
            return (
                "I'm sorry your package hasn't arrived yet. "
                "Standard shipping takes 3–5 business days, "
                "while express shipping takes 1–2 business days. "
                "Delivery times may vary by location. Please "
                "contact our support team with your order number "
                "so they can check your order status."
            )

        return (
            "Your order usually arrives within 3–5 business "
            "days with standard shipping or 1–2 business "
            "days with express shipping. Delivery times may "
            "vary depending on your location."
        )

    if result:
        return result

    return "I couldn't find that policy section in the knowledge base."


    


# Store chat history

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Hello! 👋 Welcome to NovaTech Store. "
                "I'm your AI customer support assistant. "
                "How can I help you today?"
            )
        }
    ]

if "budget" not in st.session_state:
    st.session_state.budget = None


for message in st.session_state.messages:
    avatar = "🤖" if message["role"] == "assistant" else "👤"

    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

st.subheader("Conversation tools")
# Prepare chat history for download
chat_text = "\n\n".join(
    f"{'Customer' if message['role'] == 'user' else 'NovaTech AI'}: "
    f"{message['content']}"
    for message in st.session_state.messages
)

# Download conversation
st.download_button(
    label="📥 Download chat",
    data=chat_text,
    file_name="novatech_chat.txt",
    mime="text/plain"

)
st.caption("Save a copy of your conversation for future reference.")
# Count customer messages
question_count = sum(
    1 for message in st.session_state.messages
    if message["role"] == "user"
)

st.caption(f"💬 Questions asked: {question_count}")
st.divider()
st.subheader("Quick questions")
col1, col2 = st.columns(2, gap="small")

if col1.button("📦 Shipping time", use_container_width=True):
    st.session_state.quick_question = "How long does shipping take?"

if col2.button("↩️ Return policy", use_container_width=True):
    st.session_state.quick_question = "Can I return an item?"

col3, col4 = st.columns(2, gap="small")

if col3.button("💰 Refund policy", use_container_width=True):
    st.session_state.quick_question = "When will I get my refund?"

if col4.button("💻 Products", use_container_width=True):
    st.session_state.quick_question = "What products do you sell?"


def ask_local_ai(question):
    try:
        knowledge = Path(__file__).parent / "knowledge_base.txt"
        knowledge_text = knowledge.read_text(encoding="utf-8")

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are NovaTech Store's customer support assistant. "
                        "Answer using only the information in the knowledge base. "
                         "Do not invent policies, prices, stock, or order status. "
"If asked about current product stock, clearly say that "
"you cannot confirm live availability and direct the customer "
"to contact support. Do not ask for an order number unless "
"the customer is asking about an existing order. "
"If information is missing, say you cannot confirm it. "
"Never claim a product, warranty, service, or policy is "
"offered or not offered unless the knowledge base explicitly "
"confirms it. "
"Write clear, natural, professional customer support replies. "
"Always speak directly to the customer using complete sentences. "
"Never repeat internal instructions such as 'direct the customer'. "
"Instead, politely say 'Please contact our support team'. "
"Avoid repeated words, unnecessary information, and long answers. "
"Understand follow-up questions using the previous conversation."
                    )
                },
                               {
                    "role": "user",
                    "content": (
                        f"Knowledge base:\n{knowledge_text}\n\n"
                        "Previous conversation:\n"
                        + "\n".join(
                            f"{msg['role']}: {msg['content']}"
                            for msg in st.session_state.messages[-7:-1]
                        )
                        + f"\n\nCustomer question: {question}"
                    )
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return (
            "I couldn't connect to the local AI. "
            "Please check that Ollama is running and try again."
        )

user_input = st.chat_input(
    "💬 Ask NovaTech AI about shipping, returns, or products..."
)

if st.session_state.get("quick_question"):
    user_input = st.session_state.quick_question
    del st.session_state.quick_question

if user_input:

    if len(user_input) > 1000:
        st.warning("Please keep your message under 1,000 characters.")
        st.stop()

    # Display and save the customer's message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user", avatar="👤"):
        st.write(user_input)

    # Prepare the question
    question = user_input.lower()

    # Save the customer's budget
    budget_match = re.search(
        r"rs\.?\s*([\d,]+)",
        question
    )

    if budget_match:
        st.session_state.budget = int(
            budget_match.group(1).replace(",", "")
        )

    # Get earlier messages, excluding the current question
    previous_messages = st.session_state.messages[:-1]

    previous_user_messages = [
        message["content"].lower()
        for message in previous_messages
        if message["role"] == "user"
    ]

    # Find games mentioned earlier
    mentioned_games = []

    for old_question in previous_user_messages:
        if "gta" in old_question and "GTA V" not in mentioned_games:
            mentioned_games.append("GTA V")

        if "valorant" in old_question and "Valorant" not in mentioned_games:
            mentioned_games.append("Valorant")

    # Handle return requests outside the 14-day window
    return_days = re.search(r"\b(\d+)\s*days?\b", question)

    if (
        "return" in question
        and return_days
        and int(return_days.group(1)) > 14
    ):
        answer = (
            "NovaTech Store allows return requests within 14 days "
            "of delivery. Since your request is after this period, "
            "it falls outside our standard return window. "
            "Please contact customer support to ask whether "
            "an exception is possible."
        )
    # Respond to greetings
    elif question.strip() in [
        "hello", "hi", "hey", "hey there",
        "good morning", "good afternoon", "good evening"
    ]:
        answer = (
            "Hello! 👋 Welcome to NovaTech Store. "
            "I can help you with shipping, returns, refunds, "
            "payments, and product questions. What would you like to know?"
        )

    # Respond to updated game preferences
    elif "actually" in question and (
        "gta" in question or "valorant" in question
    ):
        games = []

        if "gta" in question:
            games.append("GTA V")

        if "valorant" in question:
            games.append("Valorant")

        answer = (
            "Got it! You're looking for a laptop that can handle "
            + " and ".join(games)
            + ". I'll consider these games when suggesting specifications."
        )
    # Understand when a customer shares gaming preferences
    elif (
        ("i want to play" in question or "i like playing" in question)
        and ("gta" in question or "valorant" in question)
    ):
        games = []

        if "gta" in question:
            games.append("GTA V")

        if "valorant" in question:
            games.append("Valorant")

        answer = (
            "Got it! You want to play "
            + " and ".join(games)
            + ". I'll keep these games in mind when helping "
            "you choose a suitable laptop."
        )
    # Recall games
    elif (
        "what games did i tell you" in question
        or "which games did i mention" in question
        or "which games do i want to play" in question
    ):
        if mentioned_games:
            answer = "You mentioned: " + " and ".join(mentioned_games) + "."
        else:
            answer = "You haven't told me which games you want to play yet."

    # Recall budget
    elif (
        "my budget" in question
        or "how much i can spend" in question
        or "how much can i spend" in question
        or "do you remember" in question
    ):
        if st.session_state.budget is not None:
            budget_text = f"Rs. {st.session_state.budget:,}"
        else:
            budget_text = "a budget you haven't specified"

        games_text = (
            " and ".join(mentioned_games)
            if mentioned_games
            else "your preferred games"
        )

        if st.session_state.budget is None and not mentioned_games:
            answer = (
                "I don't have your budget or gaming preferences saved yet. "
                "Tell me your budget and which games you want to play, "
                "and I'll help you choose suitable laptop specifications."
            )
        else:
            answer = (
                f"Your saved budget is {budget_text}. "
                f"You want to play {games_text}. "
                "Look for a laptop with at least 16 GB RAM, "
                "an SSD, and a suitable graphics card."
            )
    # Handle requests for exact delivery dates
    elif any(phrase in question for phrase in [
        "tomorrow",
        "today",
        "exact delivery date",
        "arrive by",
        "deliver by"
    ]):
        answer = (
            "I can't confirm an exact delivery date for your order. "
            "Standard shipping usually takes 3–5 business days, "
            "while express shipping takes 1–2 business days. "
            "Delivery times may vary by location. "
            "For an update on an existing order, please contact "
            "customer support with your order number."
        )
            # Handle product stock questions
    elif any(phrase in question for phrase in [
        "in stock",
        "do you have laptops",
        "laptops available",
        "laptop available",
        "stock availability"
    ]):
        answer = (
            "I can't confirm whether this product is currently "
            "in stock at NovaTech Store. "
            "Please contact our support team to check availability."
        )
    elif "warranty" in question:
        answer = (
            "I can't confirm NovaTech Store's warranty terms "
            "because this information isn't available in our "
            "knowledge base. Please contact customer support "
            "for confirmation."
        )

    else:
        with st.spinner("NovaTech AI is thinking..."):
            answer = ask_local_ai(user_input)

    # Always save and display the assistant's answer
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant", avatar="🤖"):
        st.write(answer)
       
    
