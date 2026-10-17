import streamlit as st
from google import genai

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – Gemini 3.8 will answer! "
    "To use this app, you need to provide a Google Gemini API key, which you can get "
    "[here](https://aistudio.google.com/). "
)

# Ask user for their Gemini API key via `st.text_input`.
gemini_api_key = st.text_input("Gemini API Key", type="password")
if not gemini_api_key:
    st.info("Please add your Gemini API key to continue.", icon="🗝️")
else:

    # Configure the client standard for the modern SDK framework
    try:
        client = genai.Client(api_key=gemini_api_key)
    except Exception as e:
        st.error(f"Failed to initialize client: {e}")
        client = None

    if client:
        # Let the user upload a file via `st.file_uploader`.
        uploaded_file = st.file_uploader(
            "Upload a document (.txt or .md)", type=("txt", "md")
        )

        # Ask the user for a question via `st.text_area`.
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

            # Stream the response natively to the app interface using the modern model API structures
            try:
                response_stream = client.models.generate_content_stream(
                    model="gemini-3.8-flash",
                    contents=prompt,
                )

                # Helper generator function to yield text chunks out of the stream object
                def stream_chunks(stream):
                    for chunk in stream:
                        if chunk.text:
                            yield chunk.text

                st.write_stream(stream_chunks(response_stream))
                
            except Exception as api_err:
                st.error(f"Gemini API request failed: {api_err}")
