import streamlit as st
import google.generativeai as genai

# Show title and description.
st.title("Quranic AI assistant")
st.write(
    "Upload a document below and ask a question about it – Gemini will answer! "
    "To use this app, you need to provide a Google Gemini API key, which you can get "
    "[here](https://google.com). "
)

# Ask user for their Gemini API key via st.text_input.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:

    # Configure the Gemini SDK client using the stable method
    genai.configure(api_key=gemini_api_key)

    # Let the user upload a file via st.file_uploader.
    uploaded_file = st.file_uploader(
        "Upload a document (.txt or .md)", type=("txt", "md")
    )

    # Ask the user for a question via st.text_area.
    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Process the uploaded file and question.
        document = uploaded_file.read().decode()
        
        # Format the combined prompt context for Gemini
        prompt = f"Here's a document: {document} \n\n---\n\n {question}"

        # Switched to the production-supported stable standard model
        model = genai.GenerativeModel("gemini-3.8-flash")

        # Generate a streaming answer using the Gemini API.
        try:
            response = model.generate_content(prompt, stream=True)

            # Helper function to yield text chunks out of the Gemini object stream
            def stream_chunks(response_stream):
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text

            # Stream the response natively to the app interface.
            st.write_stream(stream_chunks(response))
            
        except Exception as api_err:
            st.error(f"Gemini API request failed: {api_err}")
