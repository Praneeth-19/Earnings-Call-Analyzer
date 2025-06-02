import streamlit as st
import requests
st.title("📈 Earnings Call Analyzer")
call_text = st.text_area("Paste earnings call transcript here:", height=300)
if st.button("Analyze"):
    try:
        res = requests.post("http://localhost:8000/analyze/", data={"text": call_text})
        res.raise_for_status()  # Raise exception for HTTP errors
        
        output = res.json()
        st.subheader("📝 Summary")
        st.write(output.get("summary", "No summary available"))
        st.subheader("📊 Sentiment")
        st.write(output.get("sentiment", "No sentiment analysis available"))
        st.subheader("💡 Key Insights")
        st.write(output.get("insights", "No insights available"))
    except requests.exceptions.RequestException as e:
        st.error(f"Error communicating with backend server: {e}")
    except ValueError as e:  # Includes JSONDecodeError
        st.error(f"Error processing response from server: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")